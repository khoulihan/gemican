Title: Installing Gemican
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Installing Gemican

Gemican currently runs best on 3.6+; earlier versions of Python are not
supported.

You can install Gemican via several different methods. The simplest is via [Pip](https://pip.pypa.io/):

    python -m pip install gemican

Or, if you plan on using Markdown:

    python -m pip install "gemican[markdown]"

(Keep in mind that some operating systems will require you to prefix the above command with `sudo` in order to install Gemican system-wide.)

While the above is the simplest method, the recommended approach is to create a virtual environment for Gemican via [virtualenv](https://virtualenv.pypa.io/en/latest/) before installing Gemican. Assuming you have virtualenv installed, you can then open a new terminal session and create a new virtual environment for Gemican:

    virtualenv ~/virtualenvs/gemican
    cd ~/virtualenvs/gemican
    source bin/activate

Once the virtual environment has been created and activated, Gemican can be installed via `python -m pip install gemican` as noted above. Alternatively, if you have the project source, you can install Gemican using the distutils method:

    cd path-to-Gemican-source
    python setup.py install

If you have Git installed and prefer to install the latest bleeding-edge version of Gemican rather than a stable release, use the following command:

    python -m pip install -e "git+https://github.com/getgemican/gemican.git#egg=gemican"

Once Gemican is installed, you can run `gemican --help` to see basic usage options. For more detail, refer to the [Publish]({filename}/pages/publish.md) section.

## Optional packages

If you plan on using [Markdown](https://pypi.org/project/Markdown/) as a markup format, you can install Gemican with Markdown support:

    python -m pip install "gemican[markdown]"

## Dependencies

When Gemican is installed, the following dependent Python packages should be automatically installed without any action on your part:

-   [feedgenerator](https://pypi.org/project/feedgenerator/), to generate the Atom feeds
-   [jinja2](https://pypi.org/project/Jinja2/), for templating support
-   [pytz](https://pypi.org/project/pytz/), for timezone definitions
-   [blinker](https://pypi.org/project/blinker/), an object-to-object and broadcast signaling system
-   [unidecode](https://pypi.org/project/Unidecode/), for ASCII transliterations of Unicode text utilities
-   [MarkupSafe](https://pypi.org/project/MarkupSafe/), for a markup-safe string implementation
-   [python-dateutil](https://pypi.org/project/python-dateutil/), to read the date metadata
-   [rich](https://github.com/willmcgugan/rich), for enhanced user experience in the terminal
-   [Twisted](https://twistedmatrix.com/trac/), for running the dev server
-   [pyOpenSSL](https://pypi.org/project/pyOpenSSL/) and [service-identity](https://pypi.org/project/service-identity/), for dealing with TLS certificates
-   [python-magic](https://github.com/ahupp/python-magic), for identifying file types

## Upgrading

If you installed a stable Gemican release via
[Pip](https://pip.pypa.io/) and wish to upgrade to the latest stable
release, you can do so by adding `--upgrade`:

    python -m pip install --upgrade gemican

If you installed Gemican via distutils or the bleeding-edge method,
simply perform the same step to install the most recent version.

## Kickstart your site

Once Gemican has been installed, you can create a skeleton project via
the `gemican-quickstart` command, which begins by asking some questions
about your site:

    gemican-quickstart

If run inside an activated virtual environment, `gemican-quickstart`
will look for an associated project path inside `$VIRTUAL_ENV/.project`.
If that file exists and contains a valid directory path, the new Gemican
project will be saved at that location. Otherwise, the default is the
current working directory. To set the new project path on initial
invocation, use: `gemican-quickstart --path /your/desired/directory`

Once you finish answering all the questions, your project will consist
of the following hierarchy (except for *pages* — shown in parentheses
below — which you can optionally add yourself if you plan to create
non-chronological content):

    yourproject/
    ├── content
    │   └── (pages)
    ├── output
    ├── tasks.py
    ├── Makefile
    ├── gemicanconf.py       # Main settings file
    └── publishconf.py       # Settings to use when ready to publish

The next step is to begin to adding content to the *content* folder that
has been created for you.
