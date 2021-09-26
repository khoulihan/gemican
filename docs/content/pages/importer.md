Title: Importing an existing site
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Importing an existing site

## Description

`gemican-import` is a command-line tool for converting articles from
other software to Markdown. The supported import
formats are:

-   Blogger XML export
-   Dotclear export
-   Posterous API
-   Tumblr API
-   WordPress XML export
-   RSS/Atom feed

The conversion from HTML to Markdown relies on
[Pandoc](https://pandoc.org/). For Dotclear, if the source posts are
written with Markdown syntax, they will not be converted (as Gemican
also supports Markdown).

Unlike Gemican, Wordpress supports multiple categories per article.
These are imported as a comma-separated string. You have to resolve
these manually, or use a plugin such as [More Categories](https://github.com/pelican-plugins/more-categories) that enables multiple categories per article.

## Dependencies

`gemican-import` has some dependencies not required by the rest of
Gemican:

-   *BeautifulSoup4* and *lxml*, for WordPress and Dotclear import. Can
    be installed like any other Python package
    (`pip install BeautifulSoup4 lxml`).
-   *Feedparser*, for feed import (`pip install feedparser`).
-   *Pandoc*, see the [Pandoc site](https://pandoc.org/installing.html)
    for installation instructions on your operating system.

## Usage

    gemican-import [-h] [--blogger] [--dotclear] [--posterous] [--tumblr] [--wpfile] [--feed]
                   [-o OUTPUT] [-m MARKUP] [--dir-cat] [--dir-page] [--strip-raw] [--wp-custpost]
                   [--wp-attach] [--disable-slugs] [-e EMAIL] [-p PASSWORD] [-b BLOGNAME]
                   input|api_token|api_key

### Positional arguments

``` Table of positional arguments
=============         ============================================================================
`input`               The input file to read
`api_token`           (Posterous only) api_token can be obtained from http://posterous.com/api/
`api_key`             (Tumblr only) api_key can be obtained from https://www.tumblr.com/oauth/apps
=============         ============================================================================
```

### Optional arguments

```
-h, --help            Show this help message and exit
--blogger             Blogger XML export (default: False)
--dotclear            Dotclear export (default: False)
--posterous           Posterous API (default: False)
--tumblr              Tumblr API (default: False)
--wpfile              WordPress XML export (default: False)
--feed                Feed to parse (default: False)
-o OUTPUT, --output OUTPUT
                      Output path (default: content)
-m MARKUP, --markup MARKUP
                      Output markup format: ``rst``, ``markdown``, or ``asciidoc``
                      (default: ``rst``)
--dir-cat             Put files in directories with categories name
                      (default: False)
--dir-page            Put files recognised as pages in "pages/" sub-
                        directory (blogger and wordpress import only)
                        (default: False)
--filter-author       Import only post from the specified author
--strip-raw           Strip raw HTML code that can't be converted to markup
                      such as flash embeds or iframes (wordpress import
                      only) (default: False)
--wp-custpost         Put wordpress custom post types in directories. If
                      used with --dir-cat option directories will be created
                      as "/post_type/category/" (wordpress import only)
--wp-attach           Download files uploaded to wordpress as attachments.
                      Files will be added to posts as a list in the post
                      header and links to the files within the post will be
                      updated. All files will be downloaded, even if they
                      aren't associated with a post. Files will be downloaded
                      with their original path inside the output directory,
                      e.g. "output/wp-uploads/date/postname/file.jpg".
                      (wordpress import only) (requires an internet
                      connection)
--disable-slugs       Disable storing slugs from imported posts within
                      output. With this disabled, your Gemican URLs may not
                      be consistent with your original posts. (default:
                      False)
-e EMAIL, --email=EMAIL
                      Email used to authenticate Posterous API
-p PASSWORD, --password=PASSWORD
                      Password used to authenticate Posterous API
-b BLOGNAME, --blogname=BLOGNAME
                      Blog name used in Tumblr API
```

## Examples

For Blogger:

    $ gemican-import --blogger -o ~/output ~/posts.xml

For Dotclear:

    $ gemican-import --dotclear -o ~/output ~/backup.txt

for Posterous:

    $ gemican-import --posterous -o ~/output --email=<email_address> --password=<password> <api_token>

For Tumblr:

    $ gemican-import --tumblr -o ~/output --blogname=<blogname> <api_token>

For WordPress:

    $ gemican-import --wpfile -o ~/output ~/posts.xml

## Tests

To test the module, one can use sample files:

-   for WordPress:
    <https://www.wpbeginner.com/wp-themes/how-to-add-dummy-content-for-theme-development-in-wordpress/>
-   for Dotclear:
    <http://media.dotaddict.org/tda/downloads/lorem-backup.txt>
