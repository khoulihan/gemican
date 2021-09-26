Title: Settings
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Settings

Gemican is configurable thanks to a settings file you can pass to the
command line:

    gemican content -s path/to/your/gemicanconf.py

If you used the `gemican-quickstart` command, your primary settings file
will be named `gemicanconf.py` by default.

You can also specify extra settings via `-e` / `--extra-settings` option
flags, which will override default settings as well as any defined
within settings files:

    gemican content -e DELETE_OUTPUT_DIRECTORY=true

When experimenting with different settings (especially the metadata
ones) caching may interfere and the changes may not be visible. In such
cases disable caching with `LOAD_CONTENT_CACHE = False` or use the
`--ignore-cache` command-line switch.

Settings are configured in the form of a Python module (a file). There
is an [example settings
file](https://github.com/khoulihan/gemican/raw/master/samples/gemican.conf.py)
available for reference.

To see a list of current settings in your environment, including both
default and any customized values, run the following command (append one
or more specific setting names as arguments to see values for those
settings only):

    gemican --print-settings

All the setting identifiers must be set in all-caps, otherwise they will
not be processed. Setting values that are numbers (5, 20, etc.),
booleans (True, False, None, etc.), dictionaries, or tuples should *not*
be enclosed in quotation marks. All other values (i.e., strings) *must*
be enclosed in quotation marks.

Unless otherwise specified, settings that refer to paths can be either
absolute or relative to the configuration file. The settings you define
in the configuration file will be passed to the templates, which allows
you to use your settings to add site-wide content.

Here is a list of settings for Gemican:

## Basic settings

### USE_FOLDER_AS_CATEGORY = True

When you don't specify a category in your post metadata, set this setting to
`True`, and organize your articles in subfolders, the subfolder will
become the category of your post. If set to `False`, `DEFAULT_CATEGORY`
will be used as a fallback.

### DEFAULT_CATEGORY = 'misc'

The default category to fall back on.

### DISPLAY_PAGES_ON_MENU = True

Whether to display pages on the menu of the template. Templates may or may
not honor this setting.

### DISPLAY_CATEGORIES_ON_MENU = True

Whether to display categories on the menu of the template. Templates may or
not honor this setting.

### DELETE_OUTPUT_DIRECTORY = False

Delete the output directory, and **all** of its contents, before generating
new files. This can be useful in preventing older, unnecessary files from
persisting in your output. However, **this is a destructive setting and
should be handled with extreme care.**

### OUTPUT_RETENTION = []

A list of filenames that should be retained and not deleted from the output
directory. One use case would be the preservation of version control data.

Example:

    OUTPUT_RETENTION = [".hg", ".git", ".bzr"]

### JINJA_ENVIRONMENT = {'trim_blocks': True, 'lstrip_blocks': True}

   A dictionary of custom Jinja2 environment variables you want to use. This
   also includes a list of extensions you may want to include. See [Jinja Environment documentation](https://jinja.palletsprojects.com/en/latest/api/#jinja2.Environment).

### JINJA_FILTERS = {}

   A dictionary of custom Jinja2 filters you want to use.  The dictionary
   should map the filtername to the filter function.

   Example:

    import sys
    sys.path.append('to/your/path')

    from custom_filter import urlencode_filter
    JINJA_FILTERS = {'urlencode': urlencode_filter}

   See: [Jinja custom filters documentation](https://jinja.palletsprojects.com/en/latest/api/#custom-filters).

### JINJA_GLOBALS = {}

   A dictionary of custom objects to map into the Jinja2 global environment
   namespace. The dictionary should map the global name to the global
   variable/function. See: [Jinja global namespace documentation](https://jinja.palletsprojects.com/en/latest/api/#the-global-namespace).

### JINJA_TESTS = {}

   A dictionary of custom Jinja2 tests you want to use. The dictionary should
   map test names to test functions. See: [Jinja custom tests documentation](https://jinja.palletsprojects.com/en/latest/api/#custom-tests).

### LOG_FILTER = []

   A list of tuples containing the logging level (up to `warning`) and the
   message to be ignored.

   Example:

      LOG_FILTER = [(logging.WARN, 'TAG_SAVE_AS is set to False')]

### READERS = {}

   A dictionary of file extensions / Reader classes for Gemican to process or
   ignore.

   For example, to avoid processing .md files, set:

      READERS = {'md': None}

   To add a custom reader for the `foo` extension, set:

      READERS = {'foo': FooReader}

### IGNORE_FILES = ['.#*']

   A list of glob patterns.  Files and directories matching any of these
   patterns will be ignored by the processor. For example, the default
   `['.#*']` will ignore emacs lock files, and `['__pycache__']` would
   ignore Python 3's bytecode caches.

### MARKDOWN = {...}

   Extra configuration settings for the Markdown processor. Refer to the md2gemini documentation's [In Python](https://github.com/makeworld-the-better-one/md2gemini#in-python) section for a complete
   list of supported options.

   Defaults to:

        MARKDOWN = {
            'strip_html': True,
            'plain': False,
            'code_tag': "",
            'links': 'paragraph',
        }

   Note:
      The dictionary defined in your settings file will replace this default
      one.

### OUTPUT_PATH = 'output/'

   Where to output the generated files. This should correspond to your web
   server's virtual host root directory.

### PATH

   Path to content directory to be processed by Gemican. If undefined, and
   content path is not specified via an argument to the `gemican` command,
   Gemican will use the current working directory.

### PAGE_PATHS = ['pages']

   A list of directories and files to look at for pages, relative to `PATH`.

### PAGE_EXCLUDES = []

   A list of directories to exclude when looking for pages in addition to
   `ARTICLE_PATHS`.

### ARTICLE_PATHS = ['']

   A list of directories and files to look at for articles, relative to
   `PATH`.

### ARTICLE_EXCLUDES = []

   A list of directories to exclude when looking for articles in addition to
   `PAGE_PATHS`.

### OUTPUT_SOURCES = False

   Set to True if you want to copy the articles and pages in their original
   format (e.g. Markdown or reStructuredText) to the specified `OUTPUT_PATH`.

### OUTPUT_SOURCES_EXTENSION = '.text'

   Controls the extension that will be used by the SourcesGenerator.  Defaults
   to `.text`. If not a valid string the default value will be used.

### PLUGINS = None

   The list of plugins to load. See [plugins]({filename}/pages/plugins.md).

### PLUGIN_PATHS = []

   A list of directories where to look for plugins. See [plugins]({filename}/pages/plugins.md).

### SITENAME = 'A Gemican Blog'

   Your site name

### SITEURL

   Base URL of your web site. Not defined by default, so it is best to specify
   your SITEURL; if you do not, feeds will not be generated with
   properly-formed URLs. This setting
   should begin with gemini://. Then append your
   domain, with no trailing slash at the end. Example: `SITEURL =
   'gemini://example.com'`

### STATIC_PATHS = ['images']

   A list of directories (relative to `PATH`) in which to look for static
   files. Such files will be copied to the output directory without
   modification. Articles, pages, and other content source files will normally
   be skipped, so it is safe for a directory to appear both here and in
   `PAGE_PATHS` or `ARTICLE_PATHS`.  Gemican's default settings include the
   "images" directory here.

### STATIC_EXCLUDES = []

   A list of directories to exclude when looking for static files.

### STATIC_EXCLUDE_SOURCES = True

   If set to False, content source files will not be skipped when copying files
   found in `STATIC_PATHS`. It has no effect unless
   `STATIC_PATHS` contains a directory that is also in `ARTICLE_PATHS` or
   `PAGE_PATHS`. If you are trying to publish your site's source files,
   consider using the `OUTPUT_SOURCES` setting instead.

### STATIC_CREATE_LINKS = False

   Create links instead of copying files. If the content and output directories
   are on the same device, then create hard links.  Falls back to symbolic
   links if the output directory is on a different filesystem. If symlinks are
   created, don't forget to add the `-L` or `--copy-links` option to rsync
   when uploading your site.

### STATIC_CHECK_IF_MODIFIED = False

   If set to `True`, and `STATIC_CREATE_LINKS` is `False`, compare mtimes
   of content and output files, and only copy content files that are newer than
   existing output files.

### SUMMARY_MAX_LENGTH = 50

   When creating a short summary of an article, this will be the default length
   (measured in words) of the text created.  This only applies if your content
   does not otherwise specify a summary. Setting to `None` will cause the
   summary to be a copy of the original content.

### SUMMARY_END_SUFFIX = '…'

   When creating a short summary of an article and the result was truncated to
   match the required word length, this will be used as the truncation suffix.

### WITH_FUTURE_DATES = True

   If disabled, content with dates in the future will get a default status of
   `draft`. See `Reading only modified content` below for caveats.

### INTRASITE_LINK_REGEX

   Default:

    '[{|](?P<what>.*?)[|}]'

   Regular expression that is used to parse internal links. Default syntax when
   linking to internal files, tags, etc., is to enclose the identifier, say
   `filename`, in `{}` or `||`. Identifier between `{` and `}` goes
   into the `what` capturing group.

### CACHE_CONTENT = False

   If `True`, saves content in caches.  See
   `Reading only modified content` below for details about caching.

### CONTENT_CACHING_LAYER = 'reader'

   If set to `'reader'`, save only the raw content and metadata returned by
   readers. If set to `'generator'`, save processed content objects.

### CACHE_PATH = 'cache'

   Directory in which to store cache files.

### GZIP_CACHE = True

   If `True`, use gzip to (de)compress the cache files.

### CHECK_MODIFIED_METHOD = 'mtime'

   Controls how files are checked for modifications.

### LOAD_CONTENT_CACHE = False

   If `True`, load unmodified content from caches.

### WRITE_SELECTED = []

   If this list is not empty, **only** output files with their paths in this
   list are written. Paths should be either absolute or relative to the current
   Gemican working directory. For possible use cases see
   `Writing only selected content` below.

### FORMATTED_FIELDS = ['summary']

   A list of metadata fields containing Gemtext/Markdown content. This allows multi-line metadata. I tis up to templates whether to use the metadata in the provided form.

### PORT = 1966

   The TCP port to serve content from the output folder via gemini when gemican
   is run with --listen

### BIND = ''

   The IP to which to bind the gemini server. This setting currently has no effect, but may in the future.

### SSL_PRIVATE_KEY_FILE = 'key.pem'

   The path to the SSL private key.

### SSL_CERTIFICATE_FILE = 'cert.pem'

   The path to the SSL certificate.

## URL settings

The first thing to understand is that there are currently two supported
methods for URL formation: *relative* and *absolute*. Relative URLs are
useful when testing locally, and absolute URLs are reliable and most
useful when publishing. One method of supporting both is to have one
Gemican configuration file for local development and another for
publishing. To see an example of this type of setup, use the
`gemican-quickstart` script as described in the
[Installation]({filename}/pages/install.md) section, which will produce two separate
configuration files for local development and publishing, respectively.

You can customize the URLs and locations where files will be saved. The
`*_URL` and `*_SAVE_AS` variables use Python's format strings. These
variables allow you to place your articles in a location such as
`{slug}/index.gmi` and link to them as `{slug}` for clean URLs (see
example below). These settings give you the flexibility to place your
articles and pages anywhere you want.

Note:

> If a `*_SAVE_AS` setting contains a parent directory that doesn't match the parent directory inside the corresponding `*_URL` setting, this may cause Gemican to generate unexpected URLs in a few cases, such as when using the `{attach}` syntax.

If you don't want that flexibility and instead prefer that your
generated output paths mirror your source content's filesystem path
hierarchy, try the following settings:

    PATH_METADATA = '(?P<path_no_ext>.*)\..*'
    ARTICLE_URL = ARTICLE_SAVE_AS = PAGE_URL = PAGE_SAVE_AS = '{path_no_ext}.gmi'

Otherwise, you can use a variety of file metadata attributes within
URL-related settings:

-   slug
-   date
-   lang
-   author
-   category

Example usage:

    ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/'
    ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.gmi'
    PAGE_URL = 'pages/{slug}/'
    PAGE_SAVE_AS = 'pages/{slug}/index.gmi'

This would save your articles into something like
`/posts/2011/Aug/07/sample-post/index.gmi`, save your pages into
`/pages/about/index.gmi`, and render them available at URLs of
`/posts/2011/Aug/07/sample-post/` and `/pages/about/`, respectively.

Note:

> If you specify a `datetime` directive, it will be substituted using the input files' date metadata attribute. If the date is not specified for a particular file, Gemican will rely on the file's `mtime` timestamp. Check the [Python datetime documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) for more information.

### RELATIVE_URLS = False

   Defines whether Gemican should use document-relative URLs or not. Only set
   this to `True` when developing/testing and only if you fully understand
   the effect it can have on links/feeds.

### ARTICLE_URL = '{slug}.gmi'

   The URL to refer to an article.

### ARTICLE_SAVE_AS = '{slug}.gmi'

   The place where we will save an article.

### ARTICLE_LANG_URL = '{slug}-{lang}.gmi'

   The URL to refer to an article which doesn't use the default language.

### ARTICLE_LANG_SAVE_AS = '{slug}-{lang}.gmi'

   The place where we will save an article which doesn't use the default
   language.

### DRAFT_URL = 'drafts/{slug}.gmi'

   The URL to refer to an article draft.

### DRAFT_SAVE_AS = 'drafts/{slug}.gmi'

   The place where we will save an article draft.

### DRAFT_LANG_URL = 'drafts/{slug}-{lang}.gmi'

   The URL to refer to an article draft which doesn't use the default language.

### DRAFT_LANG_SAVE_AS = 'drafts/{slug}-{lang}.gmi'

   The place where we will save an article draft which doesn't use the default
   language.

### PAGE_URL = 'pages/{slug}.gmi'

   The URL we will use to link to a page.

### PAGE_SAVE_AS = 'pages/{slug}.gmi'

   The location we will save the page. This value has to be the same as
   PAGE_URL or you need to use a rewrite in your server config.

### PAGE_LANG_URL = 'pages/{slug}-{lang}.gmi'

   The URL we will use to link to a page which doesn't use the default
   language.

### PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}.gmi'

   The location we will save the page which doesn't use the default language.

### DRAFT_PAGE_URL = 'drafts/pages/{slug}.gmi'

   The URL used to link to a page draft.

### DRAFT_PAGE_SAVE_AS = 'drafts/pages/{slug}.gmi'

   The actual location a page draft is saved at.

### DRAFT_PAGE_LANG_URL = 'drafts/pages/{slug}-{lang}.gmi'

   The URL used to link to a page draft which doesn't use the default
   language.

### DRAFT_PAGE_LANG_SAVE_AS = 'drafts/pages/{slug}-{lang}.gmi'

   The actual location a page draft which doesn't use the default language is
   saved at.

### AUTHOR_URL = 'author/{slug}.gmi'

   The URL to use for an author.

### AUTHOR_SAVE_AS = 'author/{slug}.gmi'

   The location to save an author.

### CATEGORY_URL = 'category/{slug}.gmi'

   The URL to use for a category.

### CATEGORY_SAVE_AS = 'category/{slug}.gmi'

   The location to save a category.

### TAG_URL = 'tag/{slug}.gmi'

   The URL to use for a tag.

### TAG_SAVE_AS = 'tag/{slug}.gmi'

   The location to save the tag page.

Note:

>If you do not want one or more of the default pages to be created (e.g. you are the only author on your site and thus do not need an Authors page), set the corresponding `*_SAVE_AS` setting to `''` to prevent the relevant page from being generated.

Gemican can optionally create per-year, per-month, and per-day archives
of your posts. These secondary archives are disabled by default but are
automatically enabled if you supply format strings for their respective
`_SAVE_AS` settings. Period archives fit intuitively with the
hierarchical model of web URLs and can make it easier for readers to
navigate through the posts you've written over time.

Example usage:

    YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.gmi'
    MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.gmi'

With these settings, Gemican will create an archive of all your posts
for the year at (for instance) `posts/2011/index.gmi` and an archive of
all your posts for the month at `posts/2011/Aug/index.gmi`.

Note:

> Period archives work best when the final path segment is `index.gmi`. This way a reader can remove a portion of your URL and automatically arrive at an appropriate archive of posts, without having to specify a page name.

### YEAR_ARCHIVE_URL = ''

   The URL to use for per-year archives of your posts. Used only if you have
   the `{url}` placeholder in `PAGINATION_PATTERNS`.

### YEAR_ARCHIVE_SAVE_AS = ''

   The location to save per-year archives of your posts.

### MONTH_ARCHIVE_URL = ''

   The URL to use for per-month archives of your posts. Used only if you have
   the `{url}` placeholder in `PAGINATION_PATTERNS`.

### MONTH_ARCHIVE_SAVE_AS = ''

   The location to save per-month archives of your posts.

### DAY_ARCHIVE_URL = ''

   The URL to use for per-day archives of your posts. Used only if you have the
   `{url}` placeholder in `PAGINATION_PATTERNS`.

### DAY_ARCHIVE_SAVE_AS = ''

   The location to save per-day archives of your posts.

`DIRECT_TEMPLATES` work a bit differently than noted above. Only the
`_SAVE_AS` settings are available, but it is available for any direct
template.

### ARCHIVES_SAVE_AS = 'archives.gmi'

   The location to save the article archives page.

### AUTHORS_SAVE_AS = 'authors.gmi'

   The location to save the author list.

### CATEGORIES_SAVE_AS = 'categories.gmi'

   The location to save the category list.

### TAGS_SAVE_AS = 'tags.gmi'

   The location to save the tag list.

### INDEX_SAVE_AS = 'index.gmi'

   The location to save the list of all articles.

URLs for direct template pages are theme-dependent. Some themes use
corresponding `*_URL` setting as string, while others hard-code them:
`'archives.gmi'`, `'authors.gmi'`, `'categories.gmi'`, `'tags.gmi'`.

### SLUGIFY_SOURCE = 'title'

   Specifies from where you want the slug to be automatically generated. Can be
   set to `title` to use the "Title:" metadata tag or `basename` to use the
   article's file name when creating the slug.

### SLUGIFY_USE_UNICODE = False

   Allow Unicode characters in slugs. Set `True` to keep Unicode characters
   in auto-generated slugs. Otherwise, Unicode characters will be replaced
   with ASCII equivalents.

### SLUGIFY_PRESERVE_CASE = False

   Preserve uppercase characters in slugs. Set `True` to keep uppercase
   characters from `SLUGIFY_SOURCE` as-is.

### SLUG_REGEX_SUBSTITUTIONS = [
        (r'[^\\w\\s-]', ''),  # remove non-alphabetical/whitespace/'-' chars
        (r'(?u)\\A\\s*', ''),  # strip leading whitespace
        (r'(?u)\\s*\\Z', ''),  # strip trailing whitespace
        (r'[-\\s]+', '-'),  # reduce multiple whitespace or '-' to single '-'
    ]

   Regex substitutions to make when generating slugs of articles and pages.
   Specified as a list of pairs of `(from, to)` which are applied in order,
   ignoring case. The default substitutions have the effect of removing
   non-alphanumeric characters and converting internal whitespace to dashes.
   Apart from these substitutions, slugs are always converted to lowercase
   ascii characters and leading and trailing whitespace is stripped. Useful for
   backward compatibility with existing URLs.

### AUTHOR_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS

   Regex substitutions for author slugs. Defaults to
   `SLUG_REGEX_SUBSTITUTIONS`.

### CATEGORY_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS

   Regex substitutions for category slugs. Defaults to
   `SLUG_REGEX_SUBSTITUTIONS`.

### TAG_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS

   Regex substitutions for tag slugs. Defaults to `SLUG_REGEX_SUBSTITUTIONS`.

## Time and Date

### TIMEZONE

   The timezone used in the date information, to generate Atom and RSS feeds.

   If no timezone is defined, UTC is assumed. This means that the generated
   Atom and RSS feeds will contain incorrect date information if your locale is
   not UTC.

   Gemican issues a warning in case this setting is not defined.

   Have a look at [the wikipedia page](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) to get a list of valid timezone values.

### DEFAULT_DATE = None

   The default date you want to use.  If `'fs'`, Gemican will use the file
   system timestamp information (mtime) if it can't get date information from
   the metadata.  If given any other string, it will be parsed by the same
   method as article metadata.  If set to a tuple object, the default datetime
   object will instead be generated by passing the tuple to the
   `datetime.datetime` constructor.

### DEFAULT_DATE_FORMAT = '%a %d %B %Y'

   The default date format you want to use.

### DATE_FORMATS = {}

   If you manage multiple languages, you can set the date formatting here.

   If no `DATE_FORMATS` are set, Gemican will fall back to
   `DEFAULT_DATE_FORMAT`. If you need to maintain multiple languages with
   different date formats, you can set the `DATE_FORMATS` dictionary using
   the language name (`lang` metadata in your post content) as the key.

   In addition to the standard C89 strftime format codes that are listed in
   `Python datetime documentation`_, you can use the `-` character between
   `%` and the format character to remove any leading zeros. For example,
   `%d/%m/%Y` will output `01/01/2014` whereas `%-d/%-m/%Y` will result
   in `1/1/2014`.

       DATE_FORMATS = {
           'en': '%a, %d %b %Y',
           'jp': '%Y-%m-%d(%a)',
       }

   It is also possible to set different locale settings for each language by
   using a `(locale, format)` tuple as a dictionary value which will override
   the `LOCALE` setting:

      # On Unix/Linux
      DATE_FORMATS = {
          'en': ('en_US','%a, %d %b %Y'),
          'jp': ('ja_JP','%Y-%m-%d(%a)'),
      }

      # On Windows
      DATE_FORMATS = {
          'en': ('usa','%a, %d %b %Y'),
          'jp': ('jpn','%Y-%m-%d(%a)'),
      }

### LOCALE

   Change the locale. The default is the system locale. A list of locales can be provided here or a single
   string representing one locale.  When providing a list, all the locales will
   be tried until one works.

   You can set locale to further control date format:

      LOCALE = ('usa', 'jpn',      # On Windows
                'en_US', 'ja_JP'   # On Unix/Linux
      )

   For a list of available locales refer to [locales on Windows](https://www.microsoft.com/en-us/download/details.aspx?id=55979) or on Unix/Linux, use the `locale -a` command; see manpage [locale(1)](https://linux.die.net/man/1/locale) for more information.

## Template pages

### TEMPLATE_PAGES = None

   A mapping containing template pages that will be rendered with the blog
   entries.

   If you want to generate custom pages besides your blog entries, you can
   point any Jinja2 template file with a path pointing to the file and the
   destination path for the generated file.

   For instance, if you have a blog with three static pages — a list of books,
   your resume, and a contact page — you could have::

       TEMPLATE_PAGES = {'src/books.gmi': 'dest/books.gmi',
                         'src/resume.gmi': 'dest/resume.gmi',
                         'src/contact.gmi': 'dest/contact.gmi'}

### TEMPLATE_EXTENSIONS = ['.gmi']

   The extensions to use when looking up template files from template names.

### DIRECT_TEMPLATES = ['index', 'authors', 'categories', 'tags', 'archives']

   List of templates that are used directly to render content. Typically direct
   templates are used to generate index pages for collections of content (e.g.,
   category and tag index pages). If the author, category and tag collections are not needed, set `DIRECT_TEMPLATES = ['index', 'archives']`

   `DIRECT_TEMPLATES` are searched for over paths maintained in `THEME_TEMPLATES_OVERRIDES`.

## Metadata

### AUTHOR

   Default author (usually your name).

### DEFAULT_METADATA = {}

   The default metadata you want to use for all articles and pages.

### FILENAME_METADATA = r'(?P<date>\\d{4}-\\d{2}-\\d{2}).*'

   The regexp that will be used to extract any metadata from the filename. All
   named groups that are matched will be set in the metadata object.  The
   default value will only extract the date from the filename.

   For example, to extract both the date and the slug::

      FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'

   See also `SLUGIFY_SOURCE`.

### PATH_METADATA = ''

   Like `FILENAME_METADATA`, but parsed from a page's full path relative to
   the content source directory.

### EXTRA_PATH_METADATA = {}

   Extra metadata dictionaries keyed by relative path. Relative paths require
   correct OS-specific directory separators (i.e. / in UNIX and \ in Windows)
   unlike some other Gemican file settings. Paths to a directory apply to all
   files under it. The most-specific path wins conflicts.

Not all metadata needs to be embedded in source file itself. For example, blog posts are often named following a `YYYY-MM-DD-SLUG.gmi` pattern, or nested into `YYYY/MM/DD-SLUG` directories. To extract metadata from the filename or path, set `FILENAME_METADATA` or `PATH_METADATA` to regular expressions that use Python's [group name notation](https://docs.python.org/3/library/re.html#regular-expression-syntax) `(?P<name>…)`. If you want to attach additional metadata but don't want to encode it in the path, you can set `EXTRA_PATH_METADATA`:

    EXTRA_PATH_METADATA = {
      'relative/path/to/file-1': {
          'key-1a': 'value-1a',
          'key-1b': 'value-1b',
        },
      'relative/path/to/file-2': {
          'key-2': 'value-2',
        },
    }

This can be a convenient way to shift the installed location of a
particular file:

    # Take advantage of the following defaults
    # STATIC_SAVE_AS = '{path}'
    # STATIC_URL = '{path}'
    STATIC_PATHS = [
        'static/robots.txt',
    ]
    EXTRA_PATH_METADATA = {
        'static/robots.txt': {'path': 'robots.txt'},
    }

## Feed settings

By default, Gemican uses Atom feeds. However, it is also possible to use
RSS feeds if you prefer.

Gemican generates category feeds as well as feeds for all your articles.
It does not generate feeds for tags by default, but it is possible to do
so using the `TAG_FEED_ATOM` and `TAG_FEED_RSS` settings:

### FEED_DOMAIN = None, i.e. base URL is "/"

   The domain prepended to feed URLs. Since feed URLs should always be
   absolute, it is highly recommended to define this (e.g.,
   "https://feeds.example.com"). If you have already explicitly defined SITEURL
   (see above) and want to use the same domain for your feeds, you can just
   set:  `FEED_DOMAIN = SITEURL`.

### FEED_ATOM = None, i.e. no Atom feed

   The location to save the Atom feed.

### FEED_ATOM_URL = None

   Relative URL of the Atom feed. If not set, `FEED_ATOM` is used both for
   save location and URL.

### FEED_RSS = None, i.e. no RSS

   The location to save the RSS feed.

### FEED_RSS_URL = None

   Relative URL of the RSS feed. If not set, `FEED_RSS` is used both for save
   location and URL.

### FEED_ALL_ATOM = 'feeds/all.atom.xml'

   The location to save the all-posts Atom feed: this feed will contain all
   posts regardless of their language.

### FEED_ALL_ATOM_URL = None

   Relative URL of the all-posts Atom feed. If not set, `FEED_ALL_ATOM` is
   used both for save location and URL.

### FEED_ALL_RSS = None, i.e. no all-posts RSS

   The location to save the the all-posts RSS feed: this feed will contain all
   posts regardless of their language.

### FEED_ALL_RSS_URL = None

   Relative URL of the all-posts RSS feed. If not set, `FEED_ALL_RSS` is used
   both for save location and URL.

### CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

   The location to save the category Atom feeds. [2]_

### CATEGORY_FEED_ATOM_URL = None

   Relative URL of the category Atom feeds, including the `{slug}`
   placeholder. [2]_ If not set, `CATEGORY_FEED_ATOM` is used both for save
   location and URL.

### CATEGORY_FEED_RSS = None, i.e. no RSS

   The location to save the category RSS feeds, including the `{slug}`
   placeholder. [2]_

### CATEGORY_FEED_RSS_URL = None

   Relative URL of the category RSS feeds, including the `{slug}`
   placeholder. [2]_ If not set, `CATEGORY_FEED_RSS` is used both for save
   location and URL.

### AUTHOR_FEED_ATOM = 'feeds/{slug}.atom.xml'

   The location to save the author Atom feeds. [2]_

### AUTHOR_FEED_ATOM_URL = None

   Relative URL of the author Atom feeds, including the `{slug}` placeholder.
   [2]_ If not set, `AUTHOR_FEED_ATOM` is used both for save location and
   URL.

### AUTHOR_FEED_RSS = 'feeds/{slug}.rss.xml'

   The location to save the author RSS feeds. [2]_

### AUTHOR_FEED_RSS_URL = None

   Relative URL of the author RSS feeds, including the `{slug}` placeholder.
   [2]_ If not set, `AUTHOR_FEED_RSS` is used both for save location and URL.

### TAG_FEED_ATOM = None, i.e. no tag feed

   The location to save the tag Atom feed, including the `{slug}`
   placeholder. [2]_

### TAG_FEED_ATOM_URL = None

   Relative URL of the tag Atom feed, including the `{slug}` placeholder.
   [2]_

### TAG_FEED_RSS = None, i.e. no RSS tag feed

   Relative URL to output the tag RSS feed, including the `{slug}`
   placeholder. If not set, `TAG_FEED_RSS` is used both for save location and
   URL.

### FEED_MAX_ITEMS

   Maximum number of items allowed in a feed. Feed item quantity is
   unrestricted by default.

### RSS_FEED_SUMMARY_ONLY = True

   Only include item summaries in the `description` tag of RSS feeds. If set
   to `False`, the full content will be included instead. This setting
   doesn't affect Atom feeds, only RSS ones.

If you don't want to generate some or any of these feeds, set the above
variables to `None`.

## Pagination

The default behaviour of Gemican is to list all the article titles along
with a short description on the index page. While this works well for
small-to-medium sites, sites with a large quantity of articles will
probably benefit from paginating this list.

You can use the following settings to configure the pagination.

### DEFAULT_ORPHANS = 0

   The minimum number of articles allowed on the last page. Use this when you
   don't want the last page to only contain a handful of articles.

### DEFAULT_PAGINATION = False

   The maximum number of articles to include on a page, not including orphans.
   False to disable pagination.

### PAGINATED_TEMPLATES = {'index': None, 'tag': None, 'category': None, 'author': None}

   The templates to use pagination with, and the number of articles to include
   on a page. If this value is `None`, it defaults to `DEFAULT_PAGINATION`.

### PAGINATION_PATTERNS = (...)

  Default:

    (
        (1, '{name}{extension}', '{name}{extension}'),
        (2, '{name}{number}{extension}', '{name}{number}{extension}'),
    )

   A set of patterns that are used to determine advanced pagination output.

### Using Pagination Patterns

By default, pages subsequent to `.../foo.gmi` are created as
`.../foo2.gmi`, etc. The `PAGINATION_PATTERNS` setting can be used to
change this. It takes a sequence of triples, where each triple consists
of:

    (minimum_page, page_url, page_save_as,)

For `page_url` and `page_save_as`, you may use a number of variables.
`{url}` and `{save_as}` correspond respectively to the `*_URL` and
`*_SAVE_AS` values of the corresponding page type (e.g.
`ARTICLE_SAVE_AS`). If `{save_as} == foo/bar.gmi`, then
`{name} == foo/bar` and `{extension} == .gmi`. `{base_name}` equals
`{name}` except that it strips trailing `/index` if present. `{number}`
equals the page number.

For example, if you want to leave the first page unchanged, but place
subsequent pages at `.../page/2/` etc, you could set
`PAGINATION_PATTERNS` as follows:

    PAGINATION_PATTERNS = (
        (1, '{url}', '{save_as}'),
        (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.gmi'),
    )

If you want a pattern to apply to the last page in the list, use `-1` as
the `minimum_page` value:

    (-1, '{base_name}/last/', '{base_name}/last/index.gmi'),

## Translations

Gemican offers a way to translate articles. See the
[Content]({filename}/pages/content.md) section for more information.

### DEFAULT_LANG = 'en'

   The default language to use.

### ARTICLE_TRANSLATION_ID = 'slug'

   The metadata attribute(s) used to identify which articles are translations
   of one another. May be a string or a collection of strings. Set to `None`
   or `False` to disable the identification of translations.

### PAGE_TRANSLATION_ID = 'slug'

   The metadata attribute(s) used to identify which pages are translations of
   one another. May be a string or a collection of strings. Set to `None` or
   `False` to disable the identification of translations.

### TRANSLATION_FEED_ATOM = 'feeds/all-{lang}.atom.xml'

   The location to save the Atom feed for translations. [3]_

### TRANSLATION_FEED_ATOM_URL = None

   Relative URL of the Atom feed for translations, including the `{lang}`
   placeholder, which is the language code. If not set, `TRANSLATION_FEED_ATOM` is used both for
   save location and URL.

### TRANSLATION_FEED_RSS = None, i.e. no RSS

   Where to put the RSS feed for translations.

### TRANSLATION_FEED_RSS_URL = None

   Relative URL of the RSS feed for translations, including the `{lang}`
   placeholder, which is the language code. If not set, `TRANSLATION_FEED_RSS` is used both for save
   location and URL.

## Ordering content

### NEWEST_FIRST_ARCHIVES = True

   Order archives by newest first by date. (False: orders by date with older
   articles first.)

### REVERSE_CATEGORY_ORDER = False

   Reverse the category order. (True: lists by reverse alphabetical order;
   default lists alphabetically.)

### ARTICLE_ORDER_BY = 'reversed-date'

   Defines how the articles (`articles_page.object_list` in the template) are
   sorted. Valid options are: metadata as a string (use `reversed-` prefix
   to reverse the sort order), special option `'basename'` which will use
   the basename of the file (without path), or a custom function to extract the
   sorting key from articles. Using a value of `'date'` will sort articles in
   chronological order, while the default value, `'reversed-date'`, will sort
   articles by date in reverse order (i.e., newest article comes first).

### PAGE_ORDER_BY = 'basename'

   Defines how the pages (`pages` variable in the template) are sorted.
   Options are same as `ARTICLE_ORDER_BY`.  The default value, `'basename'`
   will sort pages by their basename.

## Themes

Creating Gemican themes is addressed in a dedicated section (see
[Creating Themes]({filename}/pages/themes.md)). However, here are the settings that are related to
themes.

### THEME

   Theme to use to produce the output. Can be a relative or absolute path to a
   theme folder, or the name of a default theme or a theme installed via
   `gemican-themes` (see below).

### THEME_STATIC_DIR = 'theme'

   Destination directory in the output path where Gemican will place the files
   collected from `THEME_STATIC_PATHS`. Default is `theme`.

### THEME_STATIC_PATHS = ['static']

   Static theme paths you want to copy. Default value is `static`, but if your
   theme has other static paths, you can put them here. If files or directories
   with the same names are included in the paths defined in this settings, they
   will be progressively overwritten.

### THEME_TEMPLATES_OVERRIDES = []

   A list of paths you want Jinja2 to search for templates before searching the
   theme's `templates/` directory.  Allows for overriding individual theme
   template files without having to fork an existing theme.  Jinja2 searches in
   the following order: files in `THEME_TEMPLATES_OVERRIDES` first, then the
   theme's `templates/`.

   You can also extend templates from the theme using the `{% extends %}`
   directive utilizing the `!theme` prefix as shown in the following example:

      {% extends '!theme/article.html' %}

By default, two themes are available. You can specify them using the
`THEME` setting or by passing the `-t` option to the `gemican` command:

-   hyper
-   simple (a synonym for "plain text" :)

Gemican comes with gemican-themes, a small script for managing themes.

You can define your own theme, either by starting from scratch or by duplicating and modifying a pre-existing theme. Here is a guide on how to [create your theme]({filename}/pages/themes.md).

Following are example ways to specify your preferred theme:

    # Specify name of a built-in theme
    THEME = "hyper"
    # Specify name of a theme installed via the gemican-themes tool
    THEME = "chunk"
    # Specify a customized theme, via path relative to the settings file
    THEME = "themes/mycustomtheme"
    # Specify a customized theme, via absolute path
    THEME = "/home/myuser/projects/mysite/themes/mycustomtheme"

The built-in `hyper` theme can make good use of the following
settings. Feel free to use them in your themes as well.

### SITESUBTITLE

   A subtitle to appear in the header.

### SITEASCII

   A string containing ASCII art to include in the header.

### MENUITEMS

   A list of tuples (Title, URL) for additional menu items to appear at the
   beginning of the main menu.

### LINKS

   A list of tuples (Title, URL) for links to appear on the header.

### SOCIAL

   A list of tuples (Title, URL) to appear in the "social" section.

### LINKS_WIDGET_NAME

   Allows override of the name of the links widget.  If not specified, defaults
   to "links".

### SOCIAL_WIDGET_NAME

   Allows override of the name of the "social" widget.  If not specified,
   defaults to "social".

## Logging

Sometimes, a long list of warnings may appear during site generation.
Finding the **meaningful** error message in the middle of tons of
annoying log output can be quite tricky. In order to filter out
redundant log messages, Gemican comes with the `LOG_FILTER` setting.

`LOG_FILTER` should be a list of tuples `(level, msg)`, each of them
being composed of the logging level (up to `warning`) and the message to
be ignored. Simply populate the list with the log messages you want to
hide, and they will be filtered out.

For example:

    import logging
    LOG_FILTER = [(logging.WARN, 'TAG_SAVE_AS is set to False')]

It is possible to filter out messages by a template. Check out source
code to obtain a template.

For example:

    import logging
    LOG_FILTER = [(logging.WARN, 'Empty alt attribute for image %s in %s')]

Warning:

> Silencing messages by templates is a dangerous feature. It is possible to unintentionally filter out multiple message types with the same template (including messages from future Gemican versions). Proceed with caution.

Note:

> This option does nothing if `--debug` is passed.

## Reading only modified content

To speed up the build process, Gemican can optionally read only articles
and pages with modified content.

When Gemican is about to read some content source file:

-   The hash or modification time information for the file from a
    previous build are loaded from a cache file if `LOAD_CONTENT_CACHE`
    is `True`. These files are stored in the `CACHE_PATH` directory. If
    the file has no record in the cache file, it is read as usual.
-   The file is checked according to `CHECK_MODIFIED_METHOD`:
    If set to `'mtime'`, the modification time of the file is checked.
    If set to a name of a function provided by the `hashlib` module, e.g. `'md5'`, the file hash is checked.
    If set to anything else or the necessary information about the file cannot be found in the cache file, the content is read as usual.
-   If the file is considered unchanged, the content data saved in a
    previous build corresponding to the file is loaded from the cache,
    and the file is not read.
-   If the file is considered changed, the file is read and the new
    modification information and the content data are saved to the cache
    if `CACHE_CONTENT` is `True`.

If `CONTENT_CACHING_LAYER` is set to `'reader'` (the default), the raw
content and metadata returned by a reader are cached. If this setting is
instead set to `'generator'`, the processed content object is cached.
Caching the processed content object may conflict with plugins (as some
reading related signals may be skipped) and the `WITH_FUTURE_DATES`
functionality (as the `draft` status of the cached content objects would
not change automatically over time).

Checking modification times is faster than comparing file hashes, but it
is not as reliable because `mtime` information can be lost, e.g., when
copying content source files using the `cp` or `rsync` commands without
the `mtime` preservation mode (which for `rsync` can be invoked by
passing the `--archive` flag).

The cache files are Python pickles, so they may not be readable by
different versions of Python as the pickle format often changes. If such
an error is encountered, it is caught and the cache file is rebuilt
automatically in the new format. The cache files will also be rebuilt
after the `GZIP_CACHE` setting has been changed.

The `--ignore-cache` command-line option is useful when the whole cache
needs to be regenerated, such as when making modifications to the
settings file that will affect the cached content, or just for debugging
purposes. When Gemican runs in autoreload mode, modification of the
settings file will make it ignore the cache automatically if
`AUTORELOAD_IGNORE_CACHE` is `True`.

Note that even when using cached content, all output is always written,
so the modification times of the generated `*.html` files will always
change. Therefore, `rsync`-based uploading may benefit from the
`--checksum` option.

## Writing only selected content

When only working on a single article or page, or making tweaks to your
theme, it is often desirable to generate and review your work as quickly
as possible. In such cases, generating and writing the entire site
output is often unnecessary. By specifying only the desired files as
output paths in the `WRITE_SELECTED` list, **only** those files will be
written. This list can be also specified on the command line using the
`--write-selected` option, which accepts a comma-separated list of
output file paths. By default this list is empty, so all output is
written.

## Example settings

```
AUTHOR = 'Alexis Métaireau'
SITENAME = "Alexis' log"
SITESUBTITLE = 'A personal blog.'
SITEURL = 'gemini://blog.notmyidea.org'
TIMEZONE = "Europe/Paris"

SITEASCII = """
 _______                  __
|     __|.-----.--------.|__|.----.---.-.-----.
|    |  ||  -__|        ||  ||  __|  _  |     |
|_______||_____|__|__|__||__||____|___._|__|__|
"""

# can be useful in development, but set to False when you're ready to publish
RELATIVE_URLS = True

GITHUB_URL = 'http://github.com/ametaireau/'
DISQUS_SITENAME = "blog-notmyidea"
REVERSE_CATEGORY_ORDER = True
LOCALE = "en_US.utf8"
DEFAULT_PAGINATION = 4
DEFAULT_DATE = (2012, 3, 2, 14, 1, 1)

FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

LINKS = (('Biologeek', 'http://biologeek.org'),
         ('Filyb', "http://filyb.info/"),
         ('Libert-fr', "http://www.libert-fr.com"),
         ('N1k0', "http://prendreuncafe.com/blog/"),
         ('Tarek Ziadé', "http://ziade.org/blog"),
         ('Zubin Mithra', "http://zubin71.wordpress.com/"),)

SOCIAL = (('twitter', 'http://twitter.com/ametaireau'),
          ('lastfm', 'http://lastfm.com/user/akounet'),
          ('github', 'http://github.com/ametaireau'),)

# global metadata to all the contents
DEFAULT_METADATA = {'yeah': 'it is'}

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    }

# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'images',
    'extra/robots.txt',
    ]

# custom page generated with a jinja2 template
# TODO: This presents a problem because the template looks the same as a page
# and the page generator picks it up.
TEMPLATE_PAGES = {'pages/jinja2_template.gmi': 'jinja2_template.gmi'}

# foobar will not be used, because it's not in caps. All configuration keys
# have to be in caps
foobar = "barbaz"
```
