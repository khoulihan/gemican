Title: Creating Themes
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Creating themes

To generate its Gemtext output, Gemican uses the
[Jinja](https://palletsprojects.com/p/jinja/) templating engine due to
its flexibility and straightforward syntax. If you want to create your
own theme, feel free to take inspiration from the ["simple"
theme](https://github.com/khoulihan/gemican/tree/master/gemican/themes/simple/templates).

To generate your site using a theme you have created (or downloaded
manually and then modified), you can specify that theme via the `-t`
flag:

    gemican content -s gemicanconf.py -t /projects/your-site/themes/your-theme

If you'd rather not specify the theme on every invocation, you can
define `THEME` in your settings to point to the location of your
preferred theme.

## Structure

To make your own theme, you must follow the following structure:

    ├── static
    │   ├── css
    │   └── images
    └── templates
        ├── archives.gmi         // to display archives
        ├── period_archives.gmi  // to display time-period archives
        ├── article.gmi          // processed for each article
        ├── author.gmi           // processed for each author
        ├── authors.gmi          // must list all the authors
        ├── categories.gmi       // must list all the categories
        ├── category.gmi         // processed for each category
        ├── index.gmi            // the index (list all the articles)
        ├── page.gmi             // processed for each page
        ├── tag.gmi              // processed for each tag
        └── tags.gmi             // must list all the tags. Can be a tag cloud.

-   `static` contains all the static assets, which will be copied to the
    output theme folder. The above filesystem layout includes CSS and
    image folders, but those are just examples. Put what you need here.
-   `templates` contains all the templates that will be used to generate
    the content. The template files listed above are mandatory; you can
    add your own templates if it helps you keep things organized while
    creating your theme.

## Templates and variables

The idea is to use a simple syntax that you can embed into your Gemtext
pages. This document describes which templates should exist in a theme,
and which variables will be passed to each template at generation time.

All templates will receive the variables defined in your settings file,
as long as they are in all-caps. You can access them directly.

### Common variables

All of these settings will be available to all templates.

``` Table of variables
=============== ===================================================
Variable        Description
=============== ===================================================
output_file     The name of the file currently being generated. For
                instance, when Gemican is rendering the home page,
                output_file will be "index.gmi".
articles        The list of articles, ordered descending by date.
                All the elements are `Article` objects, so you can
                access their attributes (e.g. title, summary, author
                etc.). Sometimes this is shadowed (for instance, in
                the tags page). You will then find info about it
                in the `all_articles` variable.
dates           The same list of articles, but ordered by date,
                ascending.
hidden_articles The list of hidden articles
drafts          The list of draft articles
authors         A list of (author, articles) tuples, containing all
                the authors and corresponding articles (values)
categories      A list of (category, articles) tuples, containing
                all the categories and corresponding articles (values)
tags            A list of (tag, articles) tuples, containing all
                the tags and corresponding articles (values)
pages           The list of pages
hidden_pages    The list of hidden pages
draft_pages     The list of draft pages
=============== ===================================================
```

### Sorting

URL wrappers (currently categories, tags, and authors), have comparison
methods that allow them to be easily sorted by name:

    {% for tag, articles in tags|sort %}

If you want to sort based on different criteria, [Jinja's sort
command](https://jinja.palletsprojects.com/en/latest/templates/#sort)
has a number of options.

### Date Formatting

Gemican formats the date according to your settings and locale
(`DATE_FORMATS`/`DEFAULT_DATE_FORMAT`) and provides a `locale_date`
attribute. On the other hand, the `date` attribute will be a
[datetime](https://docs.python.org/3/library/datetime.html#datetime-objects)
object. If you need custom formatting for a date different than your
settings, use the Jinja filter `strftime` that comes with Gemican. Usage
is same as Python
[strftime](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)
format, but the filter will do the right thing and format your date
according to the locale given in your settings:

    {{ article.date|strftime('%d %B %Y') }}

### index.gmi

This is the home page or index of your blog, generated at `index.gmi`.

If pagination is active, subsequent pages will reside in
`index{number}.gmi`.

``` Table of index variables
======================  ===================================================
Variable                Description
======================  ===================================================
articles_paginator      A paginator object for the list of articles
articles_page           The current page of articles
articles_previous_page  The previous page of articles (`None` if page does
                        not exist)
articles_next_page      The next page of articles (`None` if page does
                        not exist)
dates_paginator         A paginator object for the article list, ordered by
                        date, ascending.
dates_page              The current page of articles, ordered by date,
                        ascending.
dates_previous_page     The previous page of articles, ordered by date,
                        ascending (`None` if page does not exist)
dates_next_page         The next page of articles, ordered by date,
                        ascending (`None` if page does not exist)
page_name               'index' -- useful for pagination links
======================  ===================================================
```

### author.gmi

This template will be processed for each of the existing authors, with
output generated according to the `AUTHOR_SAVE_AS` setting (Default:
`author/{slug}.gmi`). If pagination is active, subsequent pages will by
default reside at `author/{slug}{number}.gmi`.

``` Table of author template variables
======================  ===================================================
Variable                Description
======================  ===================================================
author                  The name of the author being processed
articles                Articles by this author
dates                   Articles by this author, but ordered by date,
                        ascending
articles_paginator      A paginator object for the list of articles
articles_page           The current page of articles
articles_previous_page  The previous page of articles (`None` if page does
                        not exist)
articles_next_page      The next page of articles (`None` if page does
                        not exist)
dates_paginator         A paginator object for the article list, ordered by
                        date, ascending.
dates_page              The current page of articles, ordered by date,
                        ascending.
dates_previous_page     The previous page of articles, ordered by date,
                        ascending (`None` if page does not exist)
dates_next_page         The next page of articles, ordered by date,
                        ascending (`None` if page does not exist)
page_name               AUTHOR_URL where everything after `{slug}` is
                        removed -- useful for pagination links
======================  ===================================================
```

### category.gmi

This template will be processed for each of the existing categories,
with output generated according to the `CATEGORY_SAVE_AS` setting
(Default: `category/{slug}.gmi`). If pagination is active, subsequent
pages will by default reside at `category/{slug}{number}.gmi`.

``` Table of category template variables
======================  ===================================================
Variable                Description
======================  ===================================================
category                The name of the category being processed
articles                Articles for this category
dates                   Articles for this category, but ordered by date,
                        ascending
articles_paginator      A paginator object for the list of articles
articles_page           The current page of articles
articles_previous_page  The previous page of articles (`None` if page does
                        not exist)
articles_next_page      The next page of articles (`None` if page does
                        not exist)
dates_paginator         A paginator object for the list of articles,
                        ordered by date, ascending
dates_page              The current page of articles, ordered by date,
                        ascending
dates_previous_page     The previous page of articles, ordered by date,
                        ascending (`None` if page does not exist)
dates_next_page         The next page of articles, ordered by date,
                        ascending (`None` if page does not exist)
page_name               CATEGORY_URL where everything after `{slug}` is
                        removed -- useful for pagination links
======================  ===================================================
```

### article.gmi

This template will be processed for each article, with output generated
according to the `ARTICLE_SAVE_AS` setting (Default: `{slug}.gmi`). The
following variables are available when rendering.

``` Table of article template variables
=============   ===================================================
Variable        Description
=============   ===================================================
article         The article object to be displayed
category        The name of the category for the current article
=============   ===================================================
```

Any metadata that you put in the header of the article source file will
be available as fields on the `article` object. The field name will be
the same as the name of the metadata field, except in all-lowercase
characters.

For example, you could add a field called Image to your article
metadata, as shown below:

    Title: I love Python more than music
    Date: 2013-11-06 10:06
    Tags: personal, python
    Category: Tech
    Slug: python-je-l-aime-a-mourir
    Author: Francis Cabrel
    Image: gemini://franciscabrel.com/images/pythonlove.png

This new metadata will be made available as article.image in
your article.gmi template. This would allow you, for example, to
specify an image to link to at a specific location:

    => {{ article.image }} Article image

### page.gmi

This template will be processed for each page, with output generated
according to the `PAGE_SAVE_AS` setting (Default: `pages/{slug}.gmi`).
The following variables are available when rendering.

``` Table of page template variables
=============   ===================================================
Variable        Description
=============   ===================================================
page            The page object to be displayed. You can access its
                title, slug, and content.
=============   ===================================================
```

### tag.gmi

This template will be processed for each tag, with output generated
according to the `TAG_SAVE_AS` setting (Default: `tag/{slug}.gmi`). If
pagination is active, subsequent pages will by default reside at
`tag/{slug}{number}.gmi`.

``` Table of tag template variables
======================  ===================================================
Variable                Description
======================  ===================================================
tag                     The name of the tag being processed
articles                Articles related to this tag
dates                   Articles related to this tag, but ordered by date,
                        ascending
articles_paginator      A paginator object for the list of articles
articles_page           The current page of articles
articles_previous_page  The previous page of articles (`None` if page does
                        not exist)
articles_next_page      The next page of articles (`None` if page does
                        not exist)
dates_paginator         A paginator object for the list of articles,
                        ordered by date, ascending
dates_page              The current page of articles, ordered by date,
                        ascending
dates_previous_page     The previous page of articles, ordered by date,
                        ascending (`None` if page does not exist)
dates_next_page         The next page of articles, ordered by date,
                        ascending (`None` if page does not exist)
page_name               TAG_URL where everything after `{slug}` is removed
                        -- useful for pagination links
======================  ===================================================
```

### period_archives.gmi

This template will be processed for each year of your posts if a path
for `YEAR_ARCHIVE_SAVE_AS` is defined, each month if
`MONTH_ARCHIVE_SAVE_AS` is defined, and each day if
`DAY_ARCHIVE_SAVE_AS` is defined.

``` Table of period_archive template variables
===================     ===================================================
Variable                Description
===================     ===================================================
period                  A tuple of the form (`year`, `month`, `day`) that
                        indicates the current time period. `year` and `day`
                        are numbers while `month` is a string. This tuple
                        only contains `year` if the time period is a
                        given year. It contains both `year` and `month`
                        if the time period is over years and months and
                        so on.
period_num              A tuple of the form (`year`, `month`, `day`),
                        as in `period`, except all values are numbers.

===================     ===================================================
```

You can see an example of how to use `period` in the `"simple"` theme
[period_archives.gmi template](https://github.com/khoulihan/gemican/blob/master/gemican/themes/simple/templates/period_archives.gmi)

## Objects

Detail objects attributes that are available and useful in templates.
Not all attributes are listed here, this is a selection of attributes
considered useful in a template.

### Article

The string representation of an Article is the source\_path attribute.

``` Table of Article attributes
======================  ===================================================
Attribute               Description
======================  ===================================================
author                  The Author of this article.
authors                 A list of Authors of this article.
category                The Category of this article.
content                 The rendered content of the article.
date                    Datetime object representing the article date.
date_format             Either default date format or locale date format.
default_template        Default template name.
in_default_lang         Boolean representing if the article is written
                        in the default language.
lang                    Language of the article.
locale_date             Date formatted by the `date_format`.
metadata                Article header metadata `dict`.
save_as                 Location to save the article page.
slug                    Page slug.
source_path             Full system path of the article source file.
relative_source_path    Relative path from PATH_ to the article source file.
status                  The article status, can be any of 'published' or
                        'draft'.
summary                 Rendered summary content.
tags                    List of Tag objects.
template                Template name to use for rendering.
title                   Title of the article.
translations            List of translations objects.
url                     URL to the article page.
======================  ===================================================
```

### Author / Category / Tag

The string representation of those objects is the name attribute.

``` Table of object attributes
===================     ===================================================
Attribute               Description
===================     ===================================================
name                    Name of this object.
page_name               Author page name.
save_as                 Location to save the author page.
slug                    Page slug.
url                     URL to the author page.
===================     ===================================================
```

### Page

The string representation of a Page is the source\_path attribute.

``` Table of Page object attributes
=====================  ===================================================
Attribute              Description
=====================  ===================================================
author                 The Author of this page.
content                The rendered content of the page.
date                   Datetime object representing the page date.
date_format            Either default date format or locale date format.
default_template       Default template name.
in_default_lang        Boolean representing if the article is written
                       in the default language.
lang                   Language of the article.
locale_date            Date formatted by the `date_format`.
metadata               Page header metadata `dict`.
save_as                Location to save the page.
slug                   Page slug.
source_path            Full system path of the page source file.
relative_source_path   Relative path from PATH_ to the page source file.
status                 The page status, can be any of 'published', 'hidden' or
                       'draft'.
summary                Rendered summary content.
tags                   List of Tag objects.
template               Template name to use for rendering.
title                  Title of the page.
translations           List of translations objects.
url                    URL to the page.
=====================  ===================================================
```

## Feeds

Each variable explicitly lists ATOM or RSS in the name. ATOM is still the default. Here is a complete list of the feed variables:

    FEED_ATOM
    FEED_RSS
    FEED_ALL_ATOM
    FEED_ALL_RSS
    CATEGORY_FEED_ATOM
    CATEGORY_FEED_RSS
    AUTHOR_FEED_ATOM
    AUTHOR_FEED_RSS
    TAG_FEED_ATOM
    TAG_FEED_RSS
    TRANSLATION_FEED_ATOM
    TRANSLATION_FEED_RSS

## Inheritance

Gemican supports inheritance from the `simple` theme,
so you can re-use the `simple` theme templates in your own themes.

If one of the mandatory files in the `templates/` directory of your
theme is missing, it will be replaced by the matching template from the
`simple` theme. So if the Gemtext structure of a template in the `simple`
theme is right for you, you don't have to write a new template from
scratch.

You can also extend templates from the `simple` theme in your own themes
by using the `{% extends %}` directive as in the following example:

    {% extends "!simple/index.gmi" %}

    {% extends "index.gmi" %}

## Newlines and Whitespace

Gemtext is a bit more difficult to template than HTML because whitespace, and especially newlines, are significant in Gemtext, while in HTML only the tags generally determine how the content is rendered. This requires special attention when templating for Gemican themes.

Take this template code which conditionally lists a capsule's pages:

```
{% if DISPLAY_PAGES_ON_MENU %}
  ### Pages
  {% for p in pages %}
    => {{ SITEURL }}/{{ p.url }} {% if p == page %}👉 {% endif %}{{ p.title }}
  {% endfor %}
{% endif %}
```

The indentation improves the readability of the template, but it is preserved in the output, resulting in invalid Gemtext. By default, Jinja is configured to strip newlines after, and whitespace to the left of, block statements, so those can be indented without consequence, but the content cannot:

```
{% if DISPLAY_PAGES_ON_MENU %}
### Pages
  {% for p in pages %}
=> {{ SITEURL }}/{{ p.url }} {% if p == page %}👉 {% endif %}{{ p.title }}
  {% endfor %}
{% endif %}
```

Another consideration is newlines (or lack thereof) within a conditional. If the content is supposed to be on its own line, you generally want to include the newline within the block.

This code will result in `SITENAME` and `SITESUBTITLE` being smushed together on the same line (assuming both conditions are met):

```
{% if page_name == 'index' %}# {{SITENAME}}{% endif %}
{% if SITESUBTITLE %}### {{ SITESUBTITLE }}{% endif %}
```

For this reason, when text is supposed to be on a line of its own it is important to include the newlines:

```
{% if page_name == 'index' %}
# {{SITENAME}}
{% endif %}
{% if SITESUBTITLE %}
### {{ SITESUBTITLE }}
{% endif %}
```
