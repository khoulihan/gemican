Title: Tips
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Tips

Here are some tips about Gemican that you might find useful.

## Develop Locally Using SSL

The gemini protocol requires the use of SSL, and the Gemican development server is no exception to this. It does not currently create self-signed certificates on the fly, so you must create some before running the dev server.

First, create a self-signed certificate and key using `openssl` (this
creates `cert.pem` and `key.pem`):

    $ openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'

These file names are the defaults, and gemican should pick them up if run from the current directory. The `SSL_PRIVATE_KEY_FILE` and `SSL_CERTIFICATE_FILE` settings can be used to specify their locations if you store them elsewhere.

The files can also be specified on the command line using `--key` and `--cert` switches.
