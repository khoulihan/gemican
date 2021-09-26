Title: Frequently Asked Questions (FAQ)
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Frequently Asked Questions (FAQ)

Here are some frequently asked questions about Gemican.

## What's the best way to communicate a problem, question, or suggestion?

Please read our [feedback guidelines]({filename}/pages/contribute.md).

## How can I help?

There are several ways to help out. First, you can report any Gemican
suggestions or problems you might have via Discord, Matrix (preferred) or the [issue tracker](https://github.com/khoulihan/gemican/gemican/issues). If submitting an issue report, please first check the existing issue list (both open and closed) in order to avoid submitting a duplicate issue.

If you want to contribute, please fork [the git repository](https://github.com/khoulihan/gemican), create a new feature branch, make your changes, and issue a pull request. Someone will review your changes as soon as possible. Please refer to the [How to Contribute]({filename}/pages/contribute.md) section for more details.

You can also contribute by creating themes, plugins, and improving the
documentation.

## Is the Gemican settings file mandatory?

Configuration files are optional and are just an easy way to configure
Gemican. For basic operations, it's possible to specify options while
invoking Gemican via the command line. See `gemican --help` for more
information.

## Changes to the settings file take no effect

When experimenting with different settings (especially the metadata
ones) caching may interfere and the changes may not be visible. In such
cases, ensure that caching is disabled via `LOAD_CONTENT_CACHE = False`
or use the `--ignore-cache` command-line switch.

## How do I create my own theme?

Please refer to [Creating Themes]({filename}/pages/themes.md).

## I want to use Markdown, but I got an error.

If you try to generate Markdown content without first installing the
md2gemini library, may see a message that says
`No valid files found in content`. md2gemini is not a hard dependency for
Gemican, so if you have content in Markdown format, you will need to
explicitly install the md2gemini library. You can do so by typing the
following command, prepending `sudo` if permissions require it:

    python -m pip install md2gemini

## Can I use arbitrary metadata in my templates?

Yes. For example, to include a modified date in a Markdown post, one
could include the following at the top of the article:

    Modified: 2012-08-08

This metadata can then be accessed in templates such as `article.gmi`
via:

    {% if article.modified %}
    Last modified: {{ article.modified }}
    {% endif %}

If you want to include metadata in templates outside the article context
(e.g., `base.gmi`), the `if` statement should instead be:

    {% if article and article.modified %}

## How do I assign custom templates on a per-page basis?

It's as simple as adding an extra line of metadata to any page or
article that you want to have its own template. For example:

    Template: template_name

Then just make sure your theme contains the relevant template file (e.g.
`template_name.gmi`).

## How can I override the generated URL of a specific page or article?

Include `url` and `save_as` metadata in any pages or articles that you
want to override the generated URL. Here is an example:

    Title: Override url/save_as page
    url: override/url/
    save_as: override/url/index.gmi

With this metadata, the page will be written to
`override/url/index.gmi` and Gemican will use url `override/url/` to
link to this page.

## How can I use a static page as my home page?

The override feature mentioned above can be used to specify a static
page as your home page. The following Markdown example could be stored
in `content/pages/home.md`:

    Title: Welcome to My Site
    URL:
    save_as: index.gmi

    Thank you for visiting. Welcome!

If the original gemlog index is still wanted, it can then be saved in a
different location by setting `INDEX_SAVE_AS = 'gemlog_index.gmi'` for
the `'index'` direct template.

## What if I want to disable feed generation?

To disable feed generation, all feed settings should be set to `None`.
All but three feed settings already default to `None`, so if you want to
disable all feed generation, you only need to specify the following
settings:

    FEED_ALL_ATOM = None
    CATEGORY_FEED_ATOM = None
    TRANSLATION_FEED_ATOM = None
    AUTHOR_FEED_ATOM = None
    AUTHOR_FEED_RSS = None

The word `None` should not be surrounded by quotes. Please note that
`None` and `''` are not the same thing.

## I'm getting a warning about feeds generated without SITEURL being set properly

[RSS and Atom feeds require all URL links to be
absolute](https://validator.w3.org/feed/docs/rss2.html#comments). In
order to properly generate links in Gemican you will need to set
`SITEURL` to the full path of your site.

Feeds are still generated when this warning is displayed, but links
within may be malformed and thus the feed may not validate.

## Can I force Atom feeds to show only summaries instead of article content?

Instead of having to open a separate browser window to read articles,
the overwhelming majority of folks who use feed readers prefer to read
content within the feed reader itself. Mainly for that reason, Gemican
does not support restricting Atom feeds to only contain summaries.
Unlike Atom feeds, the RSS feed specification does not include a
separate `content` field, so by default Gemican publishes RSS feeds that
only contain summaries (but can optionally be set to instead publish
full content RSS feeds). So the default feed generation behavior
provides users with a choice: subscribe to Atom feeds for full content
or to RSS feeds for just the summaries.

## Is Gemican only suitable for gemlogs?

No. Gemican can be easily configured to create and maintain any type of
static site. This may require a little customization of your theme and
Gemican configuration. For example, if you do not need tags on your site, you could remove the relevant code from your theme. You can also disable generation of tag-related pages via:

    TAGS_SAVE_AS = ''
    TAG_SAVE_AS = ''

This documentation is created using Gemican. I has no articles, only pages, with one of the pages overriding the default index using `save_as` and `URL`.

## Why does Gemican always write all gemtext files even with content caching enabled?

In order to reliably determine whether the Gemtext output is different
before writing it, a large part of the generation environment including
the template contexts, imported plugins, etc. would have to be saved and
compared, at least in the form of a hash (which would require special
handling of unhashable types), because of all the possible combinations
of plugins, pagination, etc. which may change in many different ways.
This would require a lot more processing time and memory and storage
space. Simply writing the files each time is a lot faster and a lot more
reliable.

However, this means that the modification time of the files changes
every time, so a `rsync` based upload will transfer them even if their
content hasn't changed. A simple solution is to make `rsync` use the
`--checksum` option, which will make it compare the file checksums in a
much faster way than Gemican would.

When only several specific output files are of interest (e.g. when
working on some specific page or the theme templates), the
`WRITE_SELECTED` option may help.

## How to process only a subset of all articles?

It is often useful to process only e.g. 10 articles for debugging
purposes. This can be achieved by explicitly specifying only the
filenames of those articles in `ARTICLE_PATHS`. A list of such filenames
could be found using a command similar to
`cd content; find -name '*.md' | head -n 10`.

## How can I stop Gemican from trying to parse my static files as content?

Gemican's article and page generators run before it's static generator.
That means if you use a setup similar to the default configuration,
where a static source directory is defined inside a `*_PATHS` setting,
all files that have a valid content file ending (`.html`, `.rst`, `.md`,
...) will be treated as articles or pages before they get treated as
static files.

To circumvent this issue either use the appropriate `*_EXCLUDES` setting
or disable the offending reader via `READERS` if you don't need it.

## Why is \[arbitrary Markdown syntax\] not supported?

Gemican does not directly handle Markdown processing and instead delegates that task to the [md2gemini](https://github.com/makeworld-the-better-one/md2gemini) project. md2gemini does not support extensions at this time, so to support some other flavour of Markdown, or some custom syntax, you would have to write a plugin.
