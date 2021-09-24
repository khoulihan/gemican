Gemican
=======

Gemican is a static gemini capsule generator, written in Python_, and based on
the static site generator Pelican_.

* Write content in Markdown_ or directly in Gemtext using your editor of choice
* Includes a simple command line tool to (re)generate capsule files
* Easy to interface with version control systems and web hooks
* Completely static output is simple to host anywhere


Features
--------

Gemican’s feature highlights include:

* Chronological content (e.g., articles, blog posts) as well as static pages
* Site themes (created using Jinja2_ templates)
* Publication of articles in multiple languages
* Generation of Atom and RSS feeds
* Import existing content from WordPress, Dotclear, or RSS feeds
* Fast rebuild times due to content caching and selective output writing

Check out `Pelican's documentation`_ for further information. Gemican doesn't have its
own documentation yet.


Source code
-----------

Gemican's source code is `hosted on GitHub`_. If you feel like hacking,
take a look at `Pelican's internals`_, since Gemican doesn't have its own
documentation yet and is mostly identical to Pelican.


Why the name "Gemican"?
-----------------------

"Gemican" is an anagram of *camegin*, which means nothing.


.. Links

.. _Python: https://www.python.org/
.. _Pelican: https://github.com/getpelican/pelican
.. _Markdown: https://daringfireball.net/projects/markdown/
.. _Jinja2: https://palletsprojects.com/p/jinja/
.. _Pygments: https://pygments.org/
.. _`Pelican Plugins`: https://github.com/pelican-plugins
.. _`Pelican's documentation`: https://docs.getpelican.com/
.. _`Pelican's internals`: https://docs.getpelican.com/en/latest/internals.html
.. _`hosted on GitHub`: https://github.com/khoulihan/gemican
