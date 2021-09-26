Title: Quickstart
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Quickstart

Reading through all the documentation is highly recommended, but for the
truly impatient, following are some quick steps to get started.

## Installation

Install Gemican (and optionally Markdown if you intend to use it) on
Python 3.6+ by running the following command in your preferred terminal,
prefixing with `sudo` if permissions warrant:

    python -m pip install "gemican[markdown]"

## Create a project

First, choose a name for your project, create an appropriately-named
directory for your site, and switch to that directory:

    mkdir -p ~/projects/yoursite
    cd ~/projects/yoursite

Create a skeleton project via the `gemican-quickstart` command, which
begins by asking some questions about your site:

    gemican-quickstart

For questions that have default values denoted in brackets, feel free to
use the Return key to accept those default values[1]. When asked for
your URL prefix, enter your domain name as indicated (e.g.,
`gemini://example.com`).

## Create an article

You cannot run Gemican until you have created some content. Use your
preferred text editor to create your first article with the following
content:

    Title: My First Review
    Date: 2010-12-03 10:20
    Category: Review

    Following is a review of my favorite mechanical keyboard.

Given that this example article is in Markdown format, save it as
`~/projects/yoursite/content/keyboard-review.md`.

## Create SSL certificate

The gemini protocol requires the use of SSL, and the Gemican development server is no exception to this. It does not currently create self-signed certificates on the fly, so you must create some before running the dev server.

Create a self-signed certificate and key using `openssl` (this
creates `cert.pem` and `key.pem`):

    $ openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'

These file names are the defaults, and gemican should pick them up if run from the current directory.

## Generate your site

From your project root directory, run the `gemican` command to generate
your site:

    gemican content

Your site has now been generated inside the `output/` directory. (You
may see a warning related to feeds, but that is normal when developing
locally and can be ignored for now.)

## Preview your site

Open a new terminal session, navigate to your project root directory,
and run the following command to launch Gemican's web server:

    gemican --listen

Preview your site by navigating to <gemini://localhost:1966/> in your
Gemini browser.

Continue reading the other documentation sections for more details.
