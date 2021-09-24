import os
# from unittest.mock import patch

from gemican import readers
from gemican.tests.support import get_settings, unittest
from gemican.utils import SafeDatetime


CUR_DIR = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(CUR_DIR, 'content')


def _path(*args):
    return os.path.join(CONTENT_PATH, *args)


class ReaderTest(unittest.TestCase):

    def read_file(self, path, **kwargs):
        # Isolate from future API changes to readers.read_file
        r = readers.Readers(settings=get_settings(**kwargs))
        return r.read_file(base_path=CONTENT_PATH, path=path)

    def assertDictHasSubset(self, dictionary, subset):
        for key, value in subset.items():
            if key in dictionary:
                real_value = dictionary.get(key)
                self.assertEqual(
                    value,
                    real_value,
                    'Expected %s to have value %s, but was %s' %
                    (key, value, real_value))
            else:
                self.fail(
                    'Expected %s to have value %s, but was not in Dict' %
                    (key, value))


class TestAssertDictHasSubset(ReaderTest):
    def setUp(self):
        self.dictionary = {
            'key-a': 'val-a',
            'key-b': 'val-b'
        }

    def tearDown(self):
        self.dictionary = None

    def test_subset(self):
        self.assertDictHasSubset(self.dictionary, {'key-a': 'val-a'})

    def test_equal(self):
        self.assertDictHasSubset(self.dictionary, self.dictionary)

    def test_fail_not_set(self):
        self.assertRaisesRegex(
            AssertionError,
            r'Expected.*key-c.*to have value.*val-c.*but was not in Dict',
            self.assertDictHasSubset,
            self.dictionary,
            {'key-c': 'val-c'})

    def test_fail_wrong_val(self):
        self.assertRaisesRegex(
            AssertionError,
            r'Expected .*key-a.* to have value .*val-b.* but was .*val-a.*',
            self.assertDictHasSubset,
            self.dictionary,
            {'key-a': 'val-b'})


# Only seems to be concerned with html
"""
class DefaultReaderTest(ReaderTest):

    def test_readfile_unknown_extension(self):
        with self.assertRaises(TypeError):
            self.read_file(path='article_with_metadata.unknownextension')

    def test_readfile_path_metadata_implicit_dates(self):
        test_file = 'article_with_metadata_implicit_dates.html'
        page = self.read_file(path=test_file, DEFAULT_DATE='fs')
        expected = {
            'date': SafeDatetime.fromtimestamp(
                os.stat(_path(test_file)).st_mtime),
            'modified': SafeDatetime.fromtimestamp(
                os.stat(_path(test_file)).st_mtime)
        }

        self.assertDictHasSubset(page.metadata, expected)

    def test_readfile_path_metadata_explicit_dates(self):
        test_file = 'article_with_metadata_explicit_dates.html'
        page = self.read_file(path=test_file, DEFAULT_DATE='fs')
        expected = {
            'date': SafeDatetime(2010, 12, 2, 10, 14),
            'modified': SafeDatetime(2010, 12, 31, 23, 59)
        }

        self.assertDictHasSubset(page.metadata, expected)

    def test_readfile_path_metadata_implicit_date_explicit_modified(self):
        test_file = 'article_with_metadata_implicit_date_explicit_modified.html'
        page = self.read_file(path=test_file, DEFAULT_DATE='fs')
        expected = {
            'date': SafeDatetime.fromtimestamp(
                os.stat(_path(test_file)).st_mtime),
            'modified': SafeDatetime(2010, 12, 2, 10, 14),
        }

        self.assertDictHasSubset(page.metadata, expected)

    def test_readfile_path_metadata_explicit_date_implicit_modified(self):
        test_file = 'article_with_metadata_explicit_date_implicit_modified.html'
        page = self.read_file(path=test_file, DEFAULT_DATE='fs')
        expected = {
            'date': SafeDatetime(2010, 12, 2, 10, 14),
            'modified': SafeDatetime.fromtimestamp(
                os.stat(_path(test_file)).st_mtime)
        }

        self.assertDictHasSubset(page.metadata, expected)

    def test_find_empty_alt(self):
        with patch('gemican.readers.logger') as log_mock:
            content = ['<img alt="" src="test-image.png" width="300px" />',
                       '<img src="test-image.png"  width="300px" alt="" />']

            for tag in content:
                readers.find_empty_alt(tag, '/test/path')
                log_mock.warning.assert_called_with(
                    'Empty alt attribute for image %s in %s',
                    'test-image.png',
                    '/test/path',
                    extra={'limit_msg':
                           'Other images have empty alt attributes'}
                )
"""


class GemtextReaderTest(ReaderTest):

    def test_article_with_metadata(self):
        page = self.read_file(path='article_with_metadata.gmi')
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'title': 'This is a super article !',
            'summary': 'Multi-line metadata should be'
                       ' supported\nas well as **inline'
                       ' markup** and stuff to "typogrify'
                       '"...\n',
            'date': SafeDatetime(2010, 12, 2, 10, 14),
            'modified': SafeDatetime(2010, 12, 2, 10, 20),
            'tags': ['foo', 'bar', 'foobar'],
            'custom_field': 'http://notmyidea.org',
        }

        self.assertDictHasSubset(page.metadata, expected)

    def test_article_with_capitalized_metadata(self):
        page = self.read_file(path='article_with_capitalized_metadata.gmi')
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'title': 'This is a super article !',
            'summary': 'Multi-line metadata should be'
                       ' supported\nas well as **inline'
                       ' markup** and stuff to "typogrify'
                       '"...\n',
            'date': SafeDatetime(2010, 12, 2, 10, 14),
            'modified': SafeDatetime(2010, 12, 2, 10, 20),
            'tags': ['foo', 'bar', 'foobar'],
            'custom_field': 'http://notmyidea.org',
        }

        self.assertDictHasSubset(page.metadata, expected)

    def test_article_with_filename_metadata(self):
        page = self.read_file(
            path='2012-11-29_gmi_w_filename_meta#foo-bar.gmi',
            FILENAME_METADATA=None)
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'title': 'Gemtext with filename metadata',
            'reader': 'gemini',
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(
            path='2012-11-29_gmi_w_filename_meta#foo-bar.gmi',
            FILENAME_METADATA=r'(?P<date>\d{4}-\d{2}-\d{2}).*')
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'title': 'Gemtext with filename metadata',
            'date': SafeDatetime(2012, 11, 29),
            'reader': 'gemini',
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(
            path='2012-11-29_gmi_w_filename_meta#foo-bar.gmi',
            FILENAME_METADATA=(
                r'(?P<date>\d{4}-\d{2}-\d{2})'
                r'_(?P<Slug>.*)'
                r'#(?P<MyMeta>.*)-(?P<author>.*)'))
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'title': 'Gemtext with filename metadata',
            'date': SafeDatetime(2012, 11, 29),
            'slug': 'gmi_w_filename_meta',
            'mymeta': 'foo',
            'reader': 'gemini',
        }
        self.assertDictHasSubset(page.metadata, expected)

    def test_article_with_optional_filename_metadata(self):
        page = self.read_file(
            path='2012-11-29_gmi_w_filename_meta#foo-bar.gmi',
            FILENAME_METADATA=r'(?P<date>\d{4}-\d{2}-\d{2})?')
        expected = {
            'date': SafeDatetime(2012, 11, 29),
            'reader': 'gemini',
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(
            path='article.gmi',
            FILENAME_METADATA=r'(?P<date>\d{4}-\d{2}-\d{2})?')
        expected = {
            'reader': 'gemini',
        }
        self.assertDictHasSubset(page.metadata, expected)
        self.assertNotIn('date', page.metadata, 'Date should not be set.')

    def test_article_metadata_key_lowercase(self):
        # Keys of metadata should be lowercase.
        reader = readers.GeminiReader(settings=get_settings())
        content, metadata = reader.read(
            _path('article_with_uppercase_metadata.gmi'))

        self.assertIn('category', metadata, 'Key should be lowercase.')
        self.assertEqual('Yeah', metadata.get('category'),
                         'Value keeps case.')

    def test_article_extra_path_metadata(self):
        input_with_metadata = '2012-11-29_gmi_w_filename_meta#foo-bar.gmi'
        page_metadata = self.read_file(
            path=input_with_metadata,
            FILENAME_METADATA=(
                r'(?P<date>\d{4}-\d{2}-\d{2})'
                r'_(?P<Slug>.*)'
                r'#(?P<MyMeta>.*)-(?P<author>.*)'
            ),
            EXTRA_PATH_METADATA={
                input_with_metadata: {
                    'key-1a': 'value-1a',
                    'key-1b': 'value-1b'
                }
            }
        )
        expected_metadata = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'title': 'Gemtext with filename metadata',
            'date': SafeDatetime(2012, 11, 29),
            'slug': 'gmi_w_filename_meta',
            'mymeta': 'foo',
            'reader': 'gemini',
            'key-1a': 'value-1a',
            'key-1b': 'value-1b'
        }
        self.assertDictHasSubset(page_metadata.metadata, expected_metadata)

        input_file_path_without_metadata = 'article.gmi'
        page_without_metadata = self.read_file(
            path=input_file_path_without_metadata,
            EXTRA_PATH_METADATA={
                input_file_path_without_metadata: {
                    'author': 'Charlès Overwrite'
                }
            }
        )
        expected_without_metadata = {
            'category': 'misc',
            'author': 'Charlès Overwrite',
            'title': 'Article title',
            'reader': 'gemini',
        }
        self.assertDictHasSubset(
            page_without_metadata.metadata,
            expected_without_metadata)

    def test_article_extra_path_metadata_dont_overwrite(self):
        # EXTRA_PATH_METADATA['author'] should get ignored
        # since we don't overwrite already set values
        input_file_path = '2012-11-29_gmi_w_filename_meta#foo-bar.gmi'
        page = self.read_file(
            path=input_file_path,
            FILENAME_METADATA=(
                r'(?P<date>\d{4}-\d{2}-\d{2})'
                r'_(?P<Slug>.*)'
                r'#(?P<MyMeta>.*)-(?P<orginalauthor>.*)'
            ),
            EXTRA_PATH_METADATA={
                input_file_path: {
                    'author': 'Charlès Overwrite',
                    'key-1b': 'value-1b'
                }
            }
        )
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'title': 'Gemtext with filename metadata',
            'date': SafeDatetime(2012, 11, 29),
            'slug': 'gmi_w_filename_meta',
            'mymeta': 'foo',
            'reader': 'gemini',
            'key-1b': 'value-1b'
        }
        self.assertDictHasSubset(page.metadata, expected)

    def test_article_extra_path_metadata_recurse(self):
        parent = "TestCategory"
        notparent = "TestCategory/article"
        path = "TestCategory/article_without_category.gmi"

        epm = {
            parent: {'epmr_inherit': parent,
                     'epmr_override': parent, },
            notparent: {'epmr_bogus': notparent},
            path:   {'epmr_override': path, },
            }
        expected_metadata = {
            'epmr_inherit': parent,
            'epmr_override': path,
            }

        page = self.read_file(path=path, EXTRA_PATH_METADATA=epm)
        self.assertDictHasSubset(page.metadata, expected_metadata)

        # Make sure vars aren't getting "inherited" by mistake...
        path = "article.gmi"
        page = self.read_file(path=path, EXTRA_PATH_METADATA=epm)
        for k in expected_metadata.keys():
            self.assertNotIn(k, page.metadata)

        # Same, but for edge cases where one file's name is a prefix of
        # another.
        path = "TestCategory/article_without_category.gmi"
        page = self.read_file(path=path, EXTRA_PATH_METADATA=epm)
        for k in epm[notparent].keys():
            self.assertNotIn(k, page.metadata)

    def test_article_with_multiple_authors(self):
        page = self.read_file(path='article_with_multiple_authors.gmi')
        expected = {
            'authors': ['First Author', 'Second Author']
        }

        self.assertDictHasSubset(page.metadata, expected)

    def test_article_with_multiple_authors_semicolon(self):
        page = self.read_file(
            path='article_with_multiple_authors_semicolon.gmi')
        expected = {
            'authors': ['Author, First', 'Author, Second']
        }

        self.assertDictHasSubset(page.metadata, expected)

    def test_article_with_multiple_authors_list(self):
        page = self.read_file(path='article_with_multiple_authors_list.gmi')
        expected = {
            'authors': ['Author, First', 'Author, Second']
        }

        self.assertDictHasSubset(page.metadata, expected)

    def test_default_date_formats(self):
        tuple_date = self.read_file(path='article.gmi',
                                    DEFAULT_DATE=(2012, 5, 1))
        string_date = self.read_file(path='article.gmi',
                                     DEFAULT_DATE='2012-05-01')

        self.assertEqual(tuple_date.metadata['date'],
                         string_date.metadata['date'])

    # TODO: Gemtext is not as fussy as rst, so not sure how to fail here
    # def test_parse_error(self):
    #     # Verify that it raises an Exception, not nothing and not SystemExit or
    #     # some such
    #     with self.assertRaisesRegex(Exception, "underline too short"):
    #         self.read_file(path='../parse_error/parse_error.gmi')


@unittest.skipUnless(readers.MarkdownReader, "markdown isn't installed")
class MarkdownReaderTest(ReaderTest):

    def test_article_with_metadata(self):
        page = self.read_file(path='article_with_md_extension.md')
        expected = {
            'category': 'test',
            'title': 'Test md File',
            'summary': 'I have a lot to test\n',
            'date': SafeDatetime(2010, 12, 2, 10, 14),
            'modified': SafeDatetime(2010, 12, 2, 10, 20),
            'tags': ['foo', 'bar', 'foobar'],
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(path='article_with_markdown_and_nonascii_summary.md')
        expected = {
            'title': 'マックOS X 10.8でパイソンとVirtualenvをインストールと設定',
            'summary': 'パイソンとVirtualenvをまっくでインストールする方法について明確に説明します。\n',
            'category': '指導書',
            'date': SafeDatetime(2012, 12, 20),
            'modified': SafeDatetime(2012, 12, 22),
            'tags': ['パイソン', 'マック'],
            'slug': 'python-virtualenv-on-mac-osx-mountain-lion-10.8',
        }
        self.assertDictHasSubset(page.metadata, expected)

    def test_article_with_file_extensions(self):
        # test to ensure the md file extension is being processed by the
        # correct reader
        page = self.read_file(path='article_with_md_extension.md')
        expected = (
            "# Test Markdown File Header\r\n\r\n"
            "## Used for gemican test\r\n\r\n"
            "The quick brown fox jumped over the lazy dog's back.\r\n")
        self.assertEqual(page.content, expected)
        # test to ensure the mkd file extension is being processed by the
        # correct reader
        page = self.read_file(path='article_with_mkd_extension.mkd')
        expected = ("## Test Markdown File Header\r\n\r\n### Used for gemican"
                    " test\r\n\r\nThis is another markdown test file.  Uses"
                    " the mkd extension.\r\n")
        self.assertEqual(page.content, expected)
        # test to ensure the markdown file extension is being processed by the
        # correct reader
        page = self.read_file(path='article_with_markdown_extension.markdown')
        expected = ("## Test Markdown File Header\r\n\r\n### Used for gemican"
                    " test\r\n\r\nThis is another markdown test file.  Uses"
                    " the markdown extension.\r\n")
        self.assertEqual(page.content, expected)
        # test to ensure the mdown file extension is being processed by the
        # correct reader
        page = self.read_file(path='article_with_mdown_extension.mdown')
        expected = ("# Test Markdown File Header\r\n\r\n## Used for gemican"
                    " test\r\n\r\nThis is another markdown test file.  Uses"
                    " the mdown extension.\r\n")
        self.assertEqual(page.content, expected)

    def test_article_with_filename_metadata(self):
        page = self.read_file(
            path='2012-11-30_md_w_filename_meta#foo-bar.md',
            FILENAME_METADATA=None)
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(
            path='2012-11-30_md_w_filename_meta#foo-bar.md',
            FILENAME_METADATA=r'(?P<date>\d{4}-\d{2}-\d{2}).*')
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'date': SafeDatetime(2012, 11, 30),
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(
            path='2012-11-30_md_w_filename_meta#foo-bar.md',
            FILENAME_METADATA=(
                r'(?P<date>\d{4}-\d{2}-\d{2})'
                r'_(?P<Slug>.*)'
                r'#(?P<MyMeta>.*)-(?P<author>.*)'))
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'date': SafeDatetime(2012, 11, 30),
            'slug': 'md_w_filename_meta',
            'mymeta': 'foo',
        }
        self.assertDictHasSubset(page.metadata, expected)

    def test_article_with_optional_filename_metadata(self):
        page = self.read_file(
            path='2012-11-30_md_w_filename_meta#foo-bar.md',
            FILENAME_METADATA=r'(?P<date>\d{4}-\d{2}-\d{2})?')
        expected = {
            'date': SafeDatetime(2012, 11, 30),
            'reader': 'markdown',
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(
            path='empty.md',
            FILENAME_METADATA=r'(?P<date>\d{4}-\d{2}-\d{2})?')
        expected = {
            'reader': 'markdown',
        }
        self.assertDictHasSubset(page.metadata, expected)
        self.assertNotIn('date', page.metadata, 'Date should not be set.')

    def test_duplicate_tags_or_authors_are_removed(self):
        reader = readers.MarkdownReader(settings=get_settings())
        content, metadata = reader.read(
            _path('article_with_duplicate_tags_authors.md'))
        expected = {
            'tags': ['foo', 'bar', 'foobar'],
            'authors': ['Author, First', 'Author, Second'],
        }
        self.assertDictHasSubset(metadata, expected)

    def test_metadata_not_parsed_for_metadata(self):
        settings = get_settings()
        settings['FORMATTED_FIELDS'] = ['summary']

        reader = readers.MarkdownReader(settings=settings)
        content, metadata = reader.read(
            _path('article_with_markdown_and_nested_metadata.md'))
        expected = {
            'title': 'Article with markdown and nested summary metadata',
            'summary': 'Test: This metadata value looks like metadata\n',
        }
        self.assertDictHasSubset(metadata, expected)

    def test_empty_file(self):
        reader = readers.MarkdownReader(settings=get_settings())
        content, metadata = reader.read(
            _path('empty.md'))

        self.assertEqual(metadata, {})
        self.assertEqual(content, '')

    def test_empty_file_with_bom(self):
        reader = readers.MarkdownReader(settings=get_settings())
        content, metadata = reader.read(
            _path('empty_with_bom.md'))

        self.assertEqual(metadata, {})
        self.assertEqual(content, '')
