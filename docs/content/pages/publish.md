Title: Publish your site
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Publish your site

## Site generation

Once Gemican is installed and you have some content (e.g., in Markdown
or Gemtext format), you can convert your content into HTML via the
`gemican` command, specifying the path to your content and (optionally)
the path to your [settings]({filename}/pages/settings.md) file:

    gemican /path/to/your/content/ [-s path/to/your/settings.py]

The above command will generate your site and save it in the `output/`
folder, using the default theme to produce a simple site. The default
theme consists of very simple Gemtext that supports most of the default settings and is provided so
folks may use it as a basis for creating their own themes.

When working on a single article or page, it is possible to generate
only the file that corresponds to that content. To do this, use the
`--write-selected` argument, like so:

    gemican --write-selected output/posts/my-post-title.gmi

Note that you must specify the path to the generated *output* file — not
the source content. To determine the output file name and location, use
the `--debug` flag. If desired, `--write-selected` can take a
comma-separated list of paths or can be configured as a setting.

You can also tell Gemican to watch for your modifications, instead of
manually re-running it every time you want to see your changes. To
enable this, run the `gemican` command with the `-r` or `--autoreload`
option. On non-Windows environments, this option can also be combined
with the `-l` or `--listen` option to simultaneously both
auto-regenerate *and* serve the output at [gemini://localhost:1966](gemini://localhost:1966):

    gemican --autoreload --listen

Gemican has other command-line switches available. Have a look at the
help to see all the options you can use:

    gemican --help

## Deployment

After you have generated your site, previewed it in your local
development environment, and are ready to deploy it to production, you
might first re-generate your site with any production-specific settings
(e.g., analytics feeds, etc.) that you may have defined:

    gemican content -s publishconf.py

To base your publish configuration on top of your `gemicanconf.py`, you
can import your `gemicanconf` settings by including the following line
in your `publishconf.py`:

    from gemicanconf import *

If you have generated a `publishconf.py` using `gemican-quickstart`,
this line is included by default.

The steps for deploying your site will depend on where it will be
hosted. If you have SSH access to a server running Gemini server software, you
might use the `rsync` tool to transmit your site files:

    rsync -avc --delete output/ host.example.com:/var/gemini/your-site/

There are many other deployment options, some of which can be configured
when first setting up your site via the `gemican-quickstart` command.
See the [Tips]({filename}/pages/tips.md) page for detail on publishing via GitHub Pages.

## Automation

While the `gemican` command is the canonical way to generate your site,
automation tools can be used to streamline the generation and
publication flow. One of the questions asked during the
`gemican-quickstart` process pertains to whether you want to automate
site generation and publication. If you answered "yes" to that question,
a `tasks.py` and `Makefile` will be generated in the root of your
project. These files, pre-populated with certain information gleaned
from other answers provided during the `gemican-quickstart` process, are
meant as a starting point and should be customized to fit your
particular needs and usage patterns. If you find one or both of these
automation tools to be of limited utility, these files can deleted at
any time and will not affect usage of the canonical `gemican` command.

Following are automation tools that "wrap" the `gemican` command and can
simplify the process of generating, previewing, and uploading your site.

### Invoke

The advantage of [Invoke](https://www.pyinvoke.org/) is that it is
written in Python and thus can be used in a wide range of environments.
The downside is that it must be installed separately. Use the following
command to install Invoke, prefixing with `sudo` if your environment
requires it:

    python -m pip install invoke

Take a moment to open the `tasks.py` file that was generated in your
project root. You will see a number of commands, any one of which can be
renamed, removed, and/or customized to your liking. Using the
out-of-the-box configuration, you can generate your site via:

    invoke build

If you'd prefer to have Gemican automatically regenerate your site every
time a change is detected (which is handy when testing locally), use the
following command instead:

    invoke regenerate

To serve the generated site so it can be previewed in your browser at
gemini://localhost:1966/:

    invoke serve

To serve the generated site with automatic browser reloading every time
a change is detected, first `python -m pip install livereload`, then use
the following command:

    invoke livereload

If during the `gemican-quickstart` process you answered "yes" when asked
whether you want to upload your site via SSH, you can use the following
command to publish your site via rsync over SSH:

    invoke publish

These are just a few of the commands available by default, so feel free
to explore `tasks.py` and see what other commands are available. More
importantly, don't hesitate to customize `tasks.py` to suit your
specific needs and preferences.

### Make

A `Makefile` is also automatically created for you when you say "yes" to
the relevant question during the `gemican-quickstart` process. The
advantage of this method is that the `make` command is built into most
POSIX systems and thus doesn't require installing anything else in order
to use it. The downside is that non-POSIX systems (e.g., Windows) do not
include `make`, and installing it on those systems can be a non-trivial
task.

If you want to use `make` to generate your site using the settings in
`gemicanconf.py`, run:

    make gemtext

To generate the site for production, using the settings in
`publishconf.py`, run:

    make publish

If you'd prefer to have Gemican automatically regenerate your site every
time a change is detected (which is handy when testing locally), use the
following command instead:

    make regenerate

To serve the generated site so it can be previewed in your browser at
gemini://localhost:1966/:

    make serve

Normally you would need to run `make regenerate` and `make serve` in two
separate terminal sessions, but you can run both at once via:

    make devserver

The above command will simultaneously run Gemican in regeneration mode
as well as serve the output at gemini://localhost:1966.

When you're ready to publish your site, you can upload it via the
method(s) you chose during the `gemican-quickstart` questionnaire. For
this example, we'll use rsync over ssh:

    make rsync_upload

That's it! Your site should now be live.

(The default `Makefile` and `devserver.sh` scripts use the `python` and
`gemican` executables to complete its tasks. If you want to use
different executables, such as `python3`, you can set the `PY` and
`PELICAN` environment variables, respectively, to override the default
executable names.)
