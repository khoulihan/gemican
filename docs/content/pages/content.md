Title: Writing Content
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Writing Content

## Articles and pages

Gemican considers "articles" to be chronological content, such as posts
on a blog, and thus associated with a date.

The idea behind "pages" is that they are usually not temporal in nature
and are used for content that does not change very often (e.g., "About"
or "Contact" pages).

You can find sample content in the repository at `samples/content/`.

## Content Markup Formats

Content can either be authored directly in Gemtext, or using Markdown syntax (with a file ending in `.md`, `.markdown`, `.mkd`, or `.mdown`). Markdown generation requires that you first explicitly install the [md2gemini](https://github.com/makeworld-the-better-one/md2gemini) package, which can be done via `pip install md2gemini`.

## File metadata

Gemican tries to be smart enough to get the information it needs from
the file system (for instance, about the category of your articles), but
some information you need to provide in the form of metadata inside your
files.

Metadata should be included using the following syntax in both Gemtext and Markdown formatted files:

    Title: My super title
    Date: 2010-12-03 10:20
    Modified: 2010-12-05 19:30
    Category: Python
    Tags: gemican, publishing
    Slug: my-super-post
    Authors: Alexis Metaireau, Conan Doyle
    Summary: Short version for index and feeds

    This is the content of my super blog post.

Author and tag lists may be semicolon-separated instead, which allows
you to write authors and tags containing commas:

    Tags: gemican, publishing tool; gemican, bird
    Authors: Metaireau, Alexis; Doyle, Conan

You can also have your own metadata keys (so long as they don't conflict
with reserved metadata keywords) for use in your templates. The
following table contains a list of reserved metadata keywords:

``` Reserved metadata keywords
=============== ===============================================================
    Metadata                              Description
=============== ===============================================================
`title`         Title of the article or page
`date`          Publication date (e.g., `YYYY-MM-DD HH:SS`)
`modified`      Modification date (e.g., `YYYY-MM-DD HH:SS`)
`tags`          Content tags, separated by commas
`keywords`      Content keywords, separated by commas (HTML content only)
`category`      Content category (one only — not multiple)
`slug`          Identifier used in URLs and translations
`author`        Content author, when there is only one
`authors`       Content authors, when there are multiple
`summary`       Brief description of content for index pages
`lang`          Content language ID (`en`, `fr`, etc.)
`translation`   If content is a translation of another (`true` or `false`)
`status`        Content status: `draft`, `hidden`, or `published`
`template`      Name of template to use to generate content (without extension)
`save_as`       Save content to this relative file path
`url`           URL to use for this article/page
=============== ===============================================================
```

Readers for additional formats could be implemented via [plugins]({filename}/pages/plugins.md).

Note that, aside from the title, none of this content metadata is
mandatory: if the date is not specified and `DEFAULT_DATE` is set to
`'fs'`, Gemican will rely on the file's "mtime" timestamp, and the
category can be determined by the directory in which the file resides.
For example, a file located at `python/foobar/myfoobar.rst` will have a
category of `foobar`. If you would like to organize your files in other
ways where the name of the subfolder would not be a good category name,
you can set the setting `USE_FOLDER_AS_CATEGORY` to `False`. When
parsing dates given in the page metadata, Gemican supports the W3C's
suggested subset ISO 8601.

So the title is the only required metadata. If that bothers you, worry
not. Instead of manually specifying a title in your metadata each time,
you can use the source content file name as the title. For example, a
Markdown source file named `Publishing via Gemican.md` would
automatically be assigned a title of *Publishing via Gemican*. If you
would prefer this behavior, add the following line to your settings
file:

    FILENAME_METADATA = '(?P<title>.*)'

When experimenting with different settings (especially the metadata
ones) caching may interfere and the changes may not be visible. In such
cases disable caching with `LOAD_CONTENT_CACHE = False` or use the
`--ignore-cache` command-line switch.

`modified` should be last time you updated the article, and defaults to
`date` if not specified. Besides you can show `modified` in the
templates, feed entries in feed readers will be updated automatically
when you set `modified` to the current date after you modified your
article.

`authors` is a comma-separated list of article authors. If there's only
one author you can use `author` field.

If you do not explicitly specify summary metadata for a given post, the
`SUMMARY_MAX_LENGTH` setting can be used to specify how many words from
the beginning of an article are used as the summary.

You can also extract any metadata from the filename through a regular
expression to be set in the `FILENAME_METADATA` setting. All named
groups that are matched will be set in the metadata object. The default
value for the `FILENAME_METADATA` setting will only extract the date
from the filename. For example, if you would like to extract both the
date and the slug, you could set something like:
`'(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'`

Please note that the metadata available inside your files takes
precedence over the metadata extracted from the filename.

## Pages

If you create a folder named `pages` inside the content folder, all the
files in it will be used to generate static pages, such as **About** or
**Contact** pages. (See example filesystem layout below.)

You can use the `DISPLAY_PAGES_ON_MENU` setting to control whether all
those pages are displayed in the primary navigation menu. (Default is
`True`.)

If you want to exclude any pages from being linked to or listed in the
menu then add a `status: hidden` attribute to its metadata. This is
useful for things like making error pages that fit the generated theme
of your site.

## Static content

Static files are files other than articles and pages that are copied to
the output folder as-is, without processing. You can control which
static files are copied over with the `STATIC_PATHS` setting of the
project's `gemicanconf.py` file. Gemican's default configuration
includes the `images` directory for this, but others must be added
manually. In addition, static files that are explicitly linked to are
included (see below).

### Mixed content in the same directory

Static files can safely share a source
directory with page source files, without exposing the page sources in
the generated site. Any such directory must be added to both
`STATIC_PATHS` and `PAGE_PATHS` (or `STATIC_PATHS` and `ARTICLE_PATHS`).
Gemican will identify and process the page source files normally, and
copy the remaining files as if they lived in a separate directory
reserved for static files.

Note: Placing static and content source files together in the same
source directory does not guarantee that they will end up in the same
place in the generated site. The easiest way to do this is by using the
`{attach}` link syntax (described below). Alternatively, the
`STATIC_SAVE_AS`, `PAGE_SAVE_AS`, and `ARTICLE_SAVE_AS` settings (and
the corresponding `*_URL` settings) can be configured to place files of
different types together, just as they could in earlier versions of
Gemican.

## Linking to internal content

It is possible to specify intra-site links
to files in the *source content* hierarchy instead of files in the
*generated* hierarchy. This makes it easier to link from the current
post to other content that may be sitting alongside that post (instead
of having to determine where the other content will be placed after site
generation).

To link to internal content (files in the `content` directory), use the
following syntax for the link target: `{filename}path/to/file` Note:
forward slashes, `/`, are the required path separator in the
`{filename}` directive on all operating systems, including Windows.

For example, a Gemican project might be structured like this:

    website/
    ├── content
    │   ├── category/
    │   │   └── article1.md
    │   ├── article2.md
    │   └── pages
    │       └── about.md
    └── gemican.conf.py

In this example, `article1.md` could look like this:

    Title: The first article
    Date: 2012-12-01 10:02

    See below intra-site link examples.

    [a link relative to the current file]({filename}../article2.md)
    [a link relative to the content root]({filename}/article2.md)

and `article2.md`:

    Title: The second article
    Date: 2012-12-01 10:02

    See below intra-site link examples in Markdown format.

    [a link relative to the current file]({filename}category/article1.md)
    [a link relative to the content root]({filename}/category/article1.md)

### Linking to static files

You can link to static content using `{static}path/to/file`. Files
linked to with this syntax will automatically be copied to the output
directory, even if the source directories containing them are not
included in the `STATIC_PATHS` setting of the project's `gemicanconf.py`
file.

For example, a project's content directory might be structured like
this:

    content
    ├── images
    │   └── han.jpg
    ├── pdfs
    │   └── menu.pdf
    └── pages
        └── test.md

`test.md` would include:

    ![Alt Text]({static}/images/han.jpg)
    [Our Menu]({static}/pdfs/menu.pdf)

Site generation would then copy `han.jpg` to `output/images/han.jpg`,
`menu.pdf` to `output/pdfs/menu.pdf`, and write the appropriate links in
`test.md`.

If you use `{static}` to link to an article or a page, this will be
turned into a link to its source code.

### Attaching static files

Starting with Gemican 3.5, static files can be "attached" to a page or
article using this syntax for the link target: `{attach}path/to/file`
This works like the `{static}` syntax, but also relocates the static
file into the linking document's output directory. If the static file
originates from a subdirectory beneath the linking document's source,
that relationship will be preserved on output. Otherwise, it will become
a sibling of the linking document.

This only works for linking to static files.

For example, a project's content directory might be structured like
this:

    content
    ├── blog
    │   ├── icons
    │   │   └── icon.png
    │   ├── photo.jpg
    │   └── testpost.md
    └── downloads
        └── archive.zip

`gemicanconf.py` would include:

    PATH = 'content'
    ARTICLE_PATHS = ['blog']
    ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
    ARTICLE_URL = '{date:%Y}/{slug}.html'

`testpost.md` would include:

    Title: Test Post
    Category: test
    Date: 2014-10-31

    ![Icon]({attach}icons/icon.png)
    ![Photo]({attach}photo.jpg)
    [Downloadable File]({attach}/downloads/archive.zip)

Site generation would then produce an output directory structured like
this:

    output
    └── 2014
        ├── archive.zip
        ├── icons
        │   └── icon.png
        ├── photo.jpg
        └── test-post.html

Notice that all the files linked using `{attach}` ended up in or beneath
the article's output directory.

If a static file is linked multiple times, the relocating feature of
`{attach}` will only work in the first of those links to be processed.
After the first link, Gemican will treat `{attach}` like `{static}`.
This avoids breaking the already-processed links.

**Be careful when linking to a file from multiple documents:** Since the
first link to a file finalizes its location and Gemican does not define
the order in which documents are processed, using `{attach}` on a file
linked by multiple documents can cause its location to change from one
site build to the next. (Whether this happens in practice will depend on
the operating system, file system, version of Gemican, and documents
being added, modified, or removed from the project.) Any external sites
linking to the file's old location might then find their links broken.
**It is therefore advisable to use {attach} only if you use it in all
links to a file, and only if the linking documents share a single
directory.** Under these conditions, the file's output location will not
change in future builds. In cases where these precautions are not
possible, consider using `{static}` links instead of `{attach}`, and
letting the file's location be determined by the project's
`STATIC_SAVE_AS` and `STATIC_URL` settings. (Per-file `save_as` and
`url` overrides can still be set in `EXTRA_PATH_METADATA`.)

When using `{attach}`, any parent directory in `*_URL` / `*_SAVE_AS`
settings should match each other. See also: url-settings

### Linking to authors, categories, index and tags

You can link to authors, categories, index and tags using the
`{author}name`, `{category}foobar`, `{index}` and `{tag}tagname` syntax.

## Importing an existing site

It is possible to import your site from WordPress, Tumblr, Dotclear, and
RSS feeds using a simple script. See [import]({filename}/pages/importer.md).

## Translations

It is possible to translate articles. To do so, you need to add a `lang`
meta attribute to your articles/pages and set a `DEFAULT_LANG` setting
(which is English \[en\] by default). With those settings in place, only
articles with the default language will be listed, and each article will
be accompanied by a list of available translations for that article.

This core Gemican functionality does not create sub-sites (e.g.
`example.com/de`) with translated templates for each language.

By default, Gemican uses the article's URL "slug" to determine if two or
more articles are translations of one another. (This can be changed with
the `ARTICLE_TRANSLATION_ID` setting.) The slug can be set manually in
the file's metadata; if not set explicitly, Gemican will auto-generate
the slug from the title of the article.

Here is an example of two articles, one in English and the other in
French.

The English article:

    Title: Foobar is not dead
    slug: foobar-is-not-dead
    lang: en

    That's true, foobar is still alive!

And the French version:

    Title: Foobar n'est pas mort !
    slug: foobar-is-not-dead
    lang: fr

    Oui oui, foobar est toujours vivant !

Post content quality notwithstanding, you can see that only item in
common between the two articles is the slug, which is functioning here
as an identifier. If you'd rather not explicitly define the slug this
way, you must then instead ensure that the translated article titles are
identical, since the slug will be auto-generated from the article title.

If you do not want the original version of one specific article to be
detected by the `DEFAULT_LANG` setting, use the `translation` metadata
to specify which posts are translations:

    Title: Foobar is not dead
    slug: foobar-is-not-dead
    lang: en
    translation: true

    That's true, foobar is still alive!

## Publishing drafts

If you want to publish an article or a page as a draft (for friends to
review before publishing, for example), you can add a `Status: draft`
attribute to its metadata. That article will then be output to the
`drafts` folder and not listed on the index page nor on any category or
tag page.

If your articles should be automatically published as a draft (to not
accidentally publish an article before it is finished) include the
status in the `DEFAULT_METADATA`:

    DEFAULT_METADATA = {
        'status': 'draft',
    }

To publish a post when the default status is `draft`, update the post's
metadata to include `Status: published`.

## Hidden Posts

Like pages, posts can also be marked as `hidden` with the
`Status: hidden` attribute. Hidden posts will be output to
`ARTICLE_SAVE_AS` as expected, but are not included by default in tag or
category indexes, nor in the main article feed. This has the effect of
creating an "unlisted" post.
