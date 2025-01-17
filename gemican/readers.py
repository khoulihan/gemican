import datetime
import logging
import os
import re
from collections import OrderedDict
from urllib.parse import unquote

from gemican.cache import FileStampDataCacher
from gemican.contents import Author, Category, Page, Tag
from gemican.plugins import signals
from gemican.utils import get_date, posixize_path

try:
    from md2gemini import md2gemini
except ImportError:
    md2gemini = False  # NOQA

# Metadata processors have no way to discard an unwanted value, so we have
# them return this value instead to signal that it should be discarded later.
# This means that _filter_discardable_metadata() must be called on processed
# metadata dicts before use, to remove the items with the special value.
_DISCARD = object()

DUPLICATES_DEFINITIONS_ALLOWED = {
    'tags': False,
    'date': False,
    'modified': False,
    'status': False,
    'category': False,
    'author': False,
    'save_as': False,
    'url': False,
    'authors': True,  # TODO: Changed this because list format authors were being
                      # rejected. Unclear how the Markdown reader was dealing
                      # with these...
    'slug': False
}

METADATA_PROCESSORS = {
    'tags': lambda x, y: ([
        Tag(tag, y)
        for tag in ensure_metadata_list(x)
    ] or _DISCARD),
    'date': lambda x, y: get_date(x.replace('_', ' ')),
    'modified': lambda x, y: get_date(x),
    'status': lambda x, y: x.strip() or _DISCARD,
    'category': lambda x, y: _process_if_nonempty(Category, x, y),
    'author': lambda x, y: _process_if_nonempty(Author, x, y),
    'authors': lambda x, y: ([
        Author(strip_list_markup(author), y)
        for author in ensure_metadata_list(x)
    ] or _DISCARD),
    'slug': lambda x, y: x.strip() or _DISCARD,
}

logger = logging.getLogger(__name__)


def ensure_metadata_list(text):
    """Canonicalize the format of a list of authors or tags.  This works
       the same way as Docutils' "authors" field: if it's already a list,
       those boundaries are preserved; otherwise, it must be a string;
       if the string contains semicolons, it is split on semicolons;
       otherwise, it is split on commas.  This allows you to write
       author lists in either "Jane Doe, John Doe" or "Doe, Jane; Doe, John"
       format.

       Regardless, all list items undergo .strip() before returning, and
       empty items are discarded.
    """
    if isinstance(text, str):
        if ';' in text:
            text = text.split(';')
        else:
            text = text.split(',')

    return list(OrderedDict.fromkeys(
        [v for v in (w.strip() for w in text) if v]
    ))


def strip_list_markup(value):
    if value.startswith('- '):
        return value[2:]
    return value


def _process_if_nonempty(processor, name, settings):
    """Removes extra whitespace from name and applies a metadata processor.
    If name is empty or all whitespace, returns _DISCARD instead.
    """
    name = name.strip()
    return processor(name, settings) if name else _DISCARD


def _filter_discardable_metadata(metadata):
    """Return a copy of a dict, minus any items marked as discardable."""
    return {name: val for name, val in metadata.items() if val is not _DISCARD}


class BaseReader:
    """Base class to read files.

    This class is used to process static files, and it can be inherited for
    other types of file. A Reader class must have the following attributes:

    - enabled: (boolean) tell if the Reader class is enabled. It
      generally depends on the import of some dependency.
    - file_extensions: a list of file extensions that the Reader will process.
    - extensions: a list of extensions to use in the reader (typical use is
      Markdown).

    """
    enabled = True
    file_extensions = ['static']
    extensions = None

    def __init__(self, settings):
        self.settings = settings

    def process_metadata(self, name, value):
        if name in METADATA_PROCESSORS:
            return METADATA_PROCESSORS[name](value, self.settings)
        return value

    def read(self, source_path):
        "No-op parser"
        content = None
        metadata = {}
        return content, metadata


class MarkdownMetaDataReader(BaseReader):
    """Base class for readers with Markdown-style metadata

    Content is not parsed in any way.
    """

    enabled = False
    file_extensions = []
    extensions = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._source_path = None

    def _parse_metadata(self, meta):
        """Return a dict containing document metadata"""
        formatted_fields = self.settings['FORMATTED_FIELDS']

        output = {}
        for name, value in meta.items():
            name = name.lower()
            if name in formatted_fields:
                # Formatted metadata is special case and join all list values
                # But for Gemtext, we don't actually format anything
                formatted_values = "\n".join(value) + '\n'
                output[name] = self.process_metadata(name, formatted_values)
            elif not DUPLICATES_DEFINITIONS_ALLOWED.get(name, True):
                if len(value) > 1:
                    logger.warning(
                        'Duplicate definition of `%s` '
                        'for %s. Using first one.',
                        name, self._source_path)
                output[name] = self.process_metadata(name, value[0])
            elif len(value) > 1:
                # Handle list metadata as list of string
                output[name] = self.process_metadata(name, value)
            else:
                # Otherwise, handle metadata as single string
                output[name] = self.process_metadata(name, value[0])
        return output

    def read(self, filename):
        self._source_path = filename
        metadata = {}
        content = ""
        key = None
        # TODO: This is supposed to support multi-line strings
        # for certain keys at least.
        # TODO: This code also has trouble with files that have no metadata
        # TODO: Also blank lines seem to be permitted before the metadata
        # TODO: Authors need to be supported when specified in markdown list format
        with open(filename, mode='r') as f:
            end_of_meta = False
            while not end_of_meta:
                current = f.readline()
                if current == '\n':
                    if not key:
                        # Blank lines at start of file
                        continue
                    end_of_meta = True
                    continue
                elif current == '':
                    end_of_meta = True
                    continue

                # TODO: This is apparently supposed to be 4 or more spaces, but
                # it has to catch tabs as well. For now, accepting any whitespace
                if len(current) > 0 and current[0].isspace():
                    if key:
                        metadata[key].append(current.strip())
                else:
                    split = current.split(':', 1)
                    if len(split) == 2:
                        key = split[0]
                        if key not in metadata:
                            metadata[key] = []
                        value = split[1].strip()
                        if value != '':
                            metadata[key].append(value)
                    else:
                        # File without metadata
                        content = current
                        end_of_meta = True
            # After the first blank line, the rest is content.
            content = content + f.read()

        parsed = self._parse_metadata(metadata)

        return content, parsed


class GeminiReader(MarkdownMetaDataReader):
    """
    Parses gemtext files as input.
    """
    enabled = True
    file_extensions = ['gmi', 'gemini']


def _markdown_link_func(link):
    """Link func that undoes the url-encoding that md2gemini has done"""
    return unquote(link)


class MarkdownReader(MarkdownMetaDataReader):
    """Reader for Markdown files"""

    enabled = bool(md2gemini)
    file_extensions = ['md', 'markdown', 'mkd', 'mdown']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.markdown_settings = self.settings['MARKDOWN']
        if 'link_func' not in self.markdown_settings:
            self.markdown_settings['link_func'] = _markdown_link_func

    def read(self, source_path):
        """Parse content and metadata of markdown files"""

        text, meta = super().read(source_path)

        self._source_path = source_path
        content = md2gemini(text, **self.markdown_settings).rstrip('\ufeff')
        # md2gemini does not include a newline at the end even if one
        # was present in the content.
        if len(content) > 0:
            content += '\r\n'
        return content, meta


class Readers(FileStampDataCacher):
    """Interface for all readers.

    This class contains a mapping of file extensions / Reader classes, to know
    which Reader class must be used to read a file (based on its extension).
    This is customizable both with the 'READERS' setting, and with the
    'readers_init' signall for plugins.

    """

    def __init__(self, settings=None, cache_name=''):
        self.settings = settings or {}
        self.readers = {}
        self.reader_classes = {}

        reader_classes = [BaseReader]
        reader_classes.extend(BaseReader.__subclasses__())
        reader_classes.extend(MarkdownMetaDataReader.__subclasses__())

        for cls in reader_classes:

            if not cls.enabled:
                logger.debug('Missing dependencies for %s',
                             ', '.join(cls.file_extensions))
                continue

            for ext in cls.file_extensions:
                self.reader_classes[ext] = cls

        if self.settings['READERS']:
            self.reader_classes.update(self.settings['READERS'])

        signals.readers_init.send(self)

        for fmt, reader_class in self.reader_classes.items():
            if not reader_class:
                continue

            self.readers[fmt] = reader_class(self.settings)

        # set up caching
        cache_this_level = (cache_name != '' and
                            self.settings['CONTENT_CACHING_LAYER'] == 'reader')
        caching_policy = cache_this_level and self.settings['CACHE_CONTENT']
        load_policy = cache_this_level and self.settings['LOAD_CONTENT_CACHE']
        super().__init__(settings, cache_name, caching_policy, load_policy)

    @property
    def extensions(self):
        return self.readers.keys()

    def read_file(self, base_path, path, content_class=Page, fmt=None,
                  context=None, preread_signal=None, preread_sender=None,
                  context_signal=None, context_sender=None):
        """Return a content object parsed with the given format."""

        path = os.path.abspath(os.path.join(base_path, path))
        source_path = posixize_path(os.path.relpath(path, base_path))
        logger.debug(
            'Read file %s -> %s',
            source_path, content_class.__name__)

        if not fmt:
            _, ext = os.path.splitext(os.path.basename(path))
            fmt = ext[1:]

        if fmt not in self.readers:
            raise TypeError(
                'Gemican does not know how to parse %s', path)

        if preread_signal:
            logger.debug(
                'Signal %s.send(%s)',
                preread_signal.name, preread_sender)
            preread_signal.send(preread_sender)

        reader = self.readers[fmt]

        metadata = _filter_discardable_metadata(default_metadata(
            settings=self.settings, process=reader.process_metadata))
        metadata.update(path_metadata(
            full_path=path, source_path=source_path,
            settings=self.settings))
        metadata.update(_filter_discardable_metadata(parse_path_metadata(
            source_path=source_path, settings=self.settings,
            process=reader.process_metadata)))
        reader_name = reader.__class__.__name__
        metadata['reader'] = reader_name.replace('Reader', '').lower()

        content, reader_metadata = self.get_cached_data(path, (None, None))
        if content is None:
            content, reader_metadata = reader.read(path)
            self.cache_data(path, (content, reader_metadata))
        metadata.update(_filter_discardable_metadata(reader_metadata))

        if content:
            # find images with empty alt
            find_empty_alt(content, path)

        if context_signal:
            logger.debug(
                'Signal %s.send(%s, <metadata>)',
                context_signal.name,
                context_sender)
            context_signal.send(context_sender, metadata=metadata)

        return content_class(content=content, metadata=metadata,
                             settings=self.settings, source_path=path,
                             context=context)


def find_empty_alt(content, path):
    """Find images with empty alt

    Create warnings for all images with empty alt (up to a certain number),
    as they are really likely to be accessibility flaws.

    """
    imgs = re.compile(r"""
        (?:
            # src before alt
            <img
            [^\>]*
            src=(['"])(.*?)\1
            [^\>]*
            alt=(['"])\3
        )|(?:
            # alt before src
            <img
            [^\>]*
            alt=(['"])\4
            [^\>]*
            src=(['"])(.*?)\5
        )
        """, re.X)
    for match in re.findall(imgs, content):
        logger.warning(
            'Empty alt attribute for image %s in %s',
            os.path.basename(match[1] + match[5]), path,
            extra={'limit_msg': 'Other images have empty alt attributes'})


def default_metadata(settings=None, process=None):
    metadata = {}
    if settings:
        for name, value in dict(settings.get('DEFAULT_METADATA', {})).items():
            if process:
                value = process(name, value)
            metadata[name] = value
        if 'DEFAULT_CATEGORY' in settings:
            value = settings['DEFAULT_CATEGORY']
            if process:
                value = process('category', value)
            metadata['category'] = value
        if settings.get('DEFAULT_DATE', None) and \
           settings['DEFAULT_DATE'] != 'fs':
            if isinstance(settings['DEFAULT_DATE'], str):
                metadata['date'] = get_date(settings['DEFAULT_DATE'])
            else:
                metadata['date'] = datetime.datetime(*settings['DEFAULT_DATE'])
    return metadata


def path_metadata(full_path, source_path, settings=None):
    metadata = {}
    if settings:
        if settings.get('DEFAULT_DATE', None) == 'fs':
            metadata['date'] = datetime.datetime.fromtimestamp(
                os.stat(full_path).st_mtime)
            metadata['modified'] = metadata['date']

        # Apply EXTRA_PATH_METADATA for the source path and the paths of any
        # parent directories. Sorting EPM first ensures that the most specific
        # path wins conflicts.

        epm = settings.get('EXTRA_PATH_METADATA', {})
        for path, meta in sorted(epm.items()):
            # Enforce a trailing slash when checking for parent directories.
            # This prevents false positives when one file or directory's name
            # is a prefix of another's.
            dirpath = posixize_path(os.path.join(path, ''))
            if source_path == path or source_path.startswith(dirpath):
                metadata.update(meta)

    return metadata


def parse_path_metadata(source_path, settings=None, process=None):
    r"""Extract a metadata dictionary from a file's path

    >>> import pprint
    >>> settings = {
    ...     'FILENAME_METADATA': r'(?P<slug>[^.]*).*',
    ...     'PATH_METADATA':
    ...         r'(?P<category>[^/]*)/(?P<date>\d{4}-\d{2}-\d{2})/.*',
    ...     }
    >>> reader = BaseReader(settings=settings)
    >>> metadata = parse_path_metadata(
    ...     source_path='my-cat/2013-01-01/my-slug.html',
    ...     settings=settings,
    ...     process=reader.process_metadata)
    >>> pprint.pprint(metadata)  # doctest: +ELLIPSIS
    {'category': <gemican.urlwrappers.Category object at ...>,
     'date': datetime.datetime(2013, 1, 1, 0, 0),
     'slug': 'my-slug'}
    """
    metadata = {}
    dirname, basename = os.path.split(source_path)
    base, ext = os.path.splitext(basename)
    subdir = os.path.basename(dirname)
    if settings:
        checks = []
        for key, data in [('FILENAME_METADATA', base),
                          ('PATH_METADATA', source_path)]:
            checks.append((settings.get(key, None), data))
        if settings.get('USE_FOLDER_AS_CATEGORY', None):
            checks.append(('(?P<category>.*)', subdir))
        for regexp, data in checks:
            if regexp and data:
                match = re.match(regexp, data)
                if match:
                    # .items() for py3k compat.
                    for k, v in match.groupdict().items():
                        k = k.lower()  # metadata must be lowercase
                        if v is not None and k not in metadata:
                            if process:
                                v = process(k, v)
                            metadata[k] = v
    return metadata
