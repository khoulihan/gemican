Title: Gemican internals
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Gemican internals

This section describe how Gemican works internally. As you'll see, it's
quite simple, but a bit of documentation doesn't hurt. :)

You can also find in the report section an excerpt of a report the
original author wrote with some software design information.

## Overall structure

What Gemican does is take a list of files and process them into some
sort of output. Usually, the input files are Gemtext and
Markdown files, and the output is a gemlog, but both input and output can
be anything you want.

The logic is separated into different classes and concepts:

-   *Writers* are responsible for writing files: .gmi files, RSS
    feeds, and so on. Since those operations are commonly used, the
    object is created once and then passed to the generators.
-   *Readers* are used to read from various formats (Markdown
    and Gemtext for now, but the system is extensible). Given a
    file, they return metadata (author, tags, category, etc.) and
    content (HTML-formatted).
-   *Generators* generate the different outputs. For instance, Gemican
    comes with `ArticlesGenerator` and `PageGenerator`. Given a
    configuration, they can do whatever they want. Most of the time,
    it's generating files from inputs.
-   Gemican also uses templates, so it's easy to write your own theme.
    The syntax is [Jinja2](https://palletsprojects.com/p/jinja/) and is
    very easy to learn, so don't hesitate to jump in and build your own
    theme.

## How to implement a new reader?

Is there an awesome markup language you want to add to Gemican? Well,
the only thing you have to do is to create a class with a `read` method
that returns HTML content and some metadata.

Take a look at the Markdown reader:

    from gemican.readers import MarkdownMetaDataReader

    try:
        from md2gemini import md2gemini
    except ImportError:
        md2gemini = False  # NOQA


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

Simple, isn't it?

If your new reader requires additional Python dependencies, then you
should wrap their `import` statements in a `try...except` block. Then
inside the reader's class, set the `enabled` class attribute to mark
import success or failure. This makes it possible for users to continue
using their favourite markup method without needing to install modules
for formats they don't use.

## How to implement a new generator?

Generators have two important methods. You're not forced to create both;
only the existing ones will be called.

-   `generate_context`, that is called first, for all the generators. Do
    whatever you have to do, and update the global context if needed.
    This context is shared between all generators, and will be passed to
    the templates. For instance, the `PageGenerator` `generate_context`
    method finds all the pages, transforms them into objects, and
    populates the context with them. Be careful *not* to output anything
    using this context at this stage, as it is likely to change by the
    effect of other generators.
-   `generate_output` is then called. And guess what is it made for? Oh,
    generating the output. :) It's here that you may want to look at the
    context and call the methods of the `writer` object that is passed
    as the first argument of this function. In the `PageGenerator`
    example, this method will look at all the pages recorded in the
    global context and output a file on the disk (using the writer
    method `write_file`) for each page encountered.
