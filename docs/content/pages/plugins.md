Title: Plugins
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Plugins

Gemican supports plugins. Plugins are a way to add features to Gemican without having to directly modify the Gemican core.

## How to use plugins

Gemican has a plugin structure utilizing namespace packages that can be easily installed via [Pip](https://pip.pypa.io/). Plugins supporting this structure will install under the namespace package `gemican.plugins` and can be automatically discovered by Gemican. To see a list of Pip-installed namespace plugins that are active in your environment, run:

    gemican-plugins

If you leave the `PLUGINS` setting as default (`None`), Gemican will
automatically discover namespace plugins and register them. If, on the
other hand, you specify a `PLUGINS` setting as a list of plugins, this
auto-discovery will be disabled. At that point, only the plugins you
specify will be registered, and you must explicitly list any namespace
plugins as well.

If you are using the `PLUGINS` setting, you can specify plugins in two
ways. The first method specifies plugins as a list of strings. Namespace
plugins can be specified either by their full names
(`gemican.plugins.myplugin`) or by their short names (`myplugin`):

    PLUGINS = ['package.myplugin',
               'namespace_plugin1',
               'gemican.plugins.namespace_plugin2']

Alternatively, you can import them in your settings file and pass the
modules:

    from package import myplugin
    from gemican.plugins import namespace_plugin1, namespace_plugin2
    PLUGINS = [myplugin, namespace_plugin1, namespace_plugin2]

Note:

> When experimenting with different plugins (especially the ones that deal with metadata and content) caching may interfere and the changes may not be visible. In such cases disable caching with `LOAD_CONTENT_CACHE = False` or use the `--ignore-cache` command-line switch.

If your plugins are not in an importable path, you can specify a list of
paths via the `PLUGIN_PATHS` setting. As shown in the following example,
paths in the `PLUGIN_PATHS` list can be absolute or relative to the
settings file:

    PLUGIN_PATHS = ["plugins", "/srv/gemican/plugins"]
    PLUGINS = ["assets", "liquid_tags", "sitemap"]

## Where to find plugins

There are a large number of existing plugins for Pelican, on which Gemican is based. These may or may not work with Gemican depending on the assumptions they make about the output or what point in the generation process they intervene.

Namespace plugins can be found in the [gemican-plugins
organization](https://github.com/pelican-plugins) as individual
repositories. Legacy plugins are located in the [pelican-plugins
repository](https://github.com/getpelican/pelican-plugins) and will be
gradually phased out in favor of the namespace versions.

There are no plugins specifically for Gemican at this point in time.

## How to create plugins

Plugins are based on the concept of signals. Gemican sends signals, and
plugins subscribe to those signals. The list of available signals is
documented in a subsequent section.

The only rule to follow for plugins is to define a `register` callable,
in which you map the signals to your plugin logic. Let's take a simple
example:

    import logging

    from gemican import signals

    log = logging.getLogger(__name__)

    def test(sender):
        log.debug("%s initialized !!", sender)

    def register():
        signals.initialized.connect(test)

Note:

> Signal receivers are weakly-referenced and thus must not be defined within your `register` callable or they will be garbage-collected before the signal is emitted.

If multiple plugins connect to the same signal, there is no way to
guarantee or control in which order the plugins will be executed. This
is a limitation inherited from
[Blinker](https://pythonhosted.org/blinker/), the dependency Gemican
uses to implement signals.

### Namespace plugin structure

Namespace plugins must adhere to a certain structure in order to
function properly. They need to be installable (i.e. contain `setup.py`
or equivalent) and have a folder structure as follows:

    myplugin
    ├── gemican
    │   └── plugins
    │       └── myplugin
    │           ├── __init__.py
    │           └── ...
    ├── ...
    └── setup.py

It is crucial that `gemican` or `gemican/plugins` folder **not** contain
an `__init__.py` file. In fact, it is best to have those folders empty
besides the listed folders in the above structure and keep your plugin
related files contained solely in the `gemican/plugins/myplugin` folder
to avoid any issues.

## List of signals

Here is the list of currently implemented signals:

``` Table of plugin signals
=================================   ============================   ===========================================================================
Signal                              Arguments                       Description
=================================   ============================   ===========================================================================
initialized                         gemican object
finalized                           gemican object                 invoked after all the generators are executed and just before gemican exits
                                                                   useful for custom post processing actions, such as:
                                                                   - minifying js/css assets.
                                                                   - notify/ping search engines with an updated sitemap.
generator_init                      generator                      invoked in the Generator.__init__
all_generators_finalized            generators                     invoked after all the generators are executed and before writing output
readers_init                        readers                        invoked in the Readers.__init__
article_generator_context           article_generator, metadata
article_generator_preread           article_generator              invoked before a article is read in ArticlesGenerator.generate_context;
                                                                   use if code needs to do something before every article is parsed
article_generator_init              article_generator              invoked in the ArticlesGenerator.__init__
article_generator_pretaxonomy       article_generator              invoked before categories and tags lists are created
                                                                   useful when e.g. modifying the list of articles to be generated
                                                                   so that removed articles are not leaked in categories or tags
article_generator_finalized         article_generator              invoked at the end of ArticlesGenerator.generate_context
article_generator_write_article     article_generator, content     invoked before writing each article, the article is passed as content
article_writer_finalized            article_generator, writer      invoked after all articles and related pages have been written, but before
                                                                   the article generator is closed.
get_generators                      gemican object                 invoked in Gemican.get_generator_classes,
                                                                   can return a Generator, or several
                                                                   generators in a tuple or in a list.
get_writer                          gemican object                 invoked in Gemican.get_writer,
                                                                   can return a custom Writer.
page_generator_context              page_generator, metadata
page_generator_preread              page_generator                 invoked before a page is read in PageGenerator.generate_context;
                                                                   use if code needs to do something before every page is parsed.
page_generator_init                 page_generator                 invoked in the PagesGenerator.__init__
page_generator_finalized            page_generator                 invoked at the end of PagesGenerator.generate_context
page_generator_write_page           page_generator, content        invoked before writing each page, the page is passed as content
page_writer_finalized               page_generator, writer         invoked after all pages have been written, but before the page generator
                                                                   is closed.
static_generator_context            static_generator, metadata
static_generator_preread            static_generator               invoked before a static file is read in StaticGenerator.generate_context;
                                                                   use if code needs to do something before every static file is added to the
                                                                   staticfiles list.
static_generator_init               static_generator               invoked in the StaticGenerator.__init__
static_generator_finalized          static_generator               invoked at the end of StaticGenerator.generate_context
content_object_init                 content_object                 invoked at the end of Content.__init__
content_written                     path, context                  invoked each time a content file is written.
feed_generated                      context, feed                  invoked each time a feed gets generated. Can be used to modify a feed
                                                                   object before it gets written.
feed_written                        path, context, feed            invoked each time a feed file is written.
=================================   ============================   ===========================================================================
```

Avoid `content_object_init` signal if you intend to read `summary` or
`content` properties of the content object. That combination can result
in unresolved links when linking to internal content. Use
`_summary` and `_content` properties instead, or, alternatively, run
your plugin at a later stage (e.g. `all_generators_finalized`).

## Recipes

We eventually realised some of the recipes to create plugins would be
best shared in the documentation somewhere, so here they are!

### How to create a new reader

One thing you might want is to add support for your very own input
format. While it might make sense to add this feature in Gemican core,
we wisely chose to avoid this situation and instead have the different
readers defined via plugins.

The rationale behind this choice is mainly that plugins are really easy
to write and don't slow down Gemican itself when they're not active.

No more talking — here is an example:

    from gemican import signals
    from gemican.readers import BaseReader

    # Create a new reader class, inheriting from the gemican.reader.BaseReader
    class NewReader(BaseReader):
        enabled = True  # Yeah, you probably want that :-)

        # The list of file extensions you want this reader to match with.
        # If multiple readers were to use the same extension, the latest will
        # win (so the one you're defining here, most probably).
        file_extensions = ['yeah']

        # You need to have a read method, which takes a filename and returns
        # some content and the associated metadata.
        def read(self, filename):
            metadata = {'title': 'Oh yeah',
                        'category': 'Foo',
                        'date': '2012-12-01'}

            parsed = {}
            for key, value in metadata.items():
                parsed[key] = self.process_metadata(key, value)

            return "Some content", parsed

    def add_reader(readers):
        readers.reader_classes['yeah'] = NewReader

    # This is how gemican works.
    def register():
        signals.readers_init.connect(add_reader)

### Adding a new generator

Adding a new generator is also really easy. You might want to have a
look at internals for more information on how to create your own
generator.

    def get_generators(gemican_object):
        # define a new generator here if you need to
        return MyGenerator

    def register():
        signals.get_generators.connect(get_generators)

### Adding a new writer

Adding a writer will allow you to output additional file formats to
disk, or change how the existing formats are written to disk. Note that
only one writer will be active at a time, so be sure to either subclass
the built-in Writer, or completely re-implement it.

Here is a basic example of how to set up your own writer:

    from gemican.writers import Writer
    from gemican import signals

    class MyWriter(Writer):
        # define new writer functionality
        pass


    def add_writer(gemican_object):
        # use gemican_instance to setup stuff if needed
        return MyWriter


    def register():
        signals.get_writer.connect(add_writer)
