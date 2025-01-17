Title: Contributing and feedback guidelines
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Contributing and feedback guidelines

There are many ways to contribute to Gemican. You can improve the
documentation, add missing features, test existing features that may have been broken in the conversion to dealiing with gemini, and fix bugs (or just report them). You can also help out by reviewing and commenting on [existing issues](https://github.com/khoulihan/gemican/issues).

Don't hesitate to fork Gemican and submit an issue or pull request on
GitHub.

## Contact

Feel free to contact me (Kevin) if you have feedback or questions. The other authors listed in this documentation and elsewhere are the Pelican developers and don't know anything about Gemican specifically.

``` Contact details
Email      kevin at crimsoncookie.com
Matrix     @hyperlink_your_heart:matrix.org
Discord    Hyperlink Your Heart#1390
```

## Setting up the development environment

While there are many ways to set up one's development environment, the
following instructions will utilize [Pip](https://pip.pypa.io/) and
[Poetry](https://poetry.eustace.io/docs/#installation). These tools
facilitate managing virtual environments for separate Python projects
that are isolated from one another, so you can use different packages
(and package versions) for each.

Please note that Python 3.6+ is required for Gemican development.

*(Optional)* If you prefer to install Poetry once for use with multiple
projects, you can install it via:

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

Point your web browser to the [Gemican repository](https://github.com/khoulihan/gemican) and tap the **Fork** button at top-right. Then clone the source for your fork and add the
upstream project as a Git remote:

    mkdir ~/projects
    git clone https://github.com/YOUR_USERNAME/gemican.git ~/projects/gemican
    cd ~/projects/gemican
    git remote add upstream https://github.com/khoulihan/gemican.git

While Poetry can dynamically create and manage virtual environments,
we're going to manually create and activate a virtual environment:

    mkdir ~/virtualenvs && cd ~/virtualenvs
    python3 -m venv gemican
    source ~/virtualenvs/gemican/*/activate

Install the needed dependencies and set up the project:

    python -m pip install invoke
    invoke setup
    python -m pip install -e ~/projects/gemican

Your local environment should now be ready to go!

## Development

Once Gemican has been set up for local development, create a topic
branch for your bug fix or feature:

    git checkout -b name-of-your-bugfix-or-feature

Now you can make changes to Gemican, its documentation, and/or other
aspects of the project.

### Running the test suite

Each time you make changes to Gemican, there are two things to do
regarding tests: check that the existing tests pass, and add tests for
any new features or bug fixes. The tests are located in `gemican/tests`,
and you can run them via:

    invoke tests

In addition to running the test suite, it is important to also ensure
that any lines you changed conform to code style guidelines. You can
check that via:

    invoke lint

If code style violations are found in lines you changed, correct those
lines and re-run the above lint command until they have all been fixed.
You do not need to address style violations, if any, for code lines you
did not touch.

After making your changes and running the tests, you may see a test
failure mentioning that "some generated files differ from the expected
functional tests output." If you have made changes that affect the
output generated by Gemican, and the changes to that output are expected
and deemed correct given the nature of your changes, then you should
update the output used by the functional tests. To do so, make sure
you have both `en_EN.utf8` and `fr_FR.utf8` locales installed,
and then run the following command:

    invoke update-functional-tests

You may also find that some tests are skipped because some dependency
(e.g., Pandoc) is not installed. This does not automatically mean that
these tests have passed; you should at least verify that any skipped
tests are not affected by your changes.

You should run the test suite under each of the supported versions of
Python. This is best done by creating a separate Python environment for
each version. [Tox](https://tox.readthedocs.io/en/latest/) is a useful
tool to automate running tests inside `virtualenv` environments.

### Building the docs

If you make changes to the documentation, you should build and inspect
your changes before committing them:

    invoke docserve

Open gemini://localhost:1966 in your browser to review the
documentation. While the above task is running, any changes you make and
save to the documentation should automatically appear in the browser, as
it live-reloads when it detects changes to the documentation source
files.

### Submitting your changes

Assuming linting validation and tests pass, add a `RELEASE.md` file in
the root of the project that contains the release type (major, minor,
patch) and a summary of the changes that will be used as the release
changelog entry. For example:

    Release type: patch

    Fix browser reloading upon changes to content, settings, or theme

Commit your changes and push your topic branch:

    git add .
    git commit -m "Your detailed description of your changes"
    git push origin name-of-your-bugfix-or-feature

Finally, browse to your repository fork on GitHub and submit a pull
request.

## Logging tips

Try to use logging with appropriate levels.

For logging messages that are not repeated, use the usual Python way:

    # at top of file
    import logging
    logger = logging.getLogger(__name__)

    # when needed
    logger.warning("A warning with %s formatting", arg_to_be_formatted)

Do not format log messages yourself. Use `%s` formatting in messages and
pass arguments to logger. This is important, because the Gemican logger
will preprocess some arguments, such as exceptions.

### Limiting extraneous log messages

If the log message can occur several times, you may want to limit the
log to prevent flooding. In order to do that, use the `extra` keyword
argument for the logging message in the following format:

    logger.warning("A warning with %s formatting", arg_to_be_formatted,
        extra={'limit_msg': 'A generic message for too many warnings'})

Optionally, you can also set `'limit_args'` as a tuple of arguments in
`extra` dict if your generic message needs formatting.

Limit is set to `5`, i.e, first four logs with the same `'limit_msg'`
are outputted normally but the fifth one will be logged using
`'limit_msg'` (and `'limit_args'` if present). After the fifth,
corresponding log messages will be ignored.

For example, if you want to log missing resources, use the following
code:

    for resource in resources:
        if resource.is_missing:
            logger.warning(
                'The resource %s is missing', resource.name,
                extra={'limit_msg': 'Other resources were missing'})

The log messages will be displayed as follows:

    WARNING: The resource prettiest_cat.jpg is missing
    WARNING: The resource best_cat_ever.jpg is missing
    WARNING: The resource cutest_cat.jpg is missing
    WARNING: The resource lolcat.jpg is missing
    WARNING: Other resources were missing

### Outputting traceback in the logs

If you're logging inside an `except` block, you may want to provide the
traceback information as well. You can do that by setting `exc_info`
keyword argument to `True` during logging. However, doing so by default
can be undesired because tracebacks are long and can be confusing to
regular users. Try to limit them to `--debug` mode like the following:

    try:
        some_action()
    except Exception as e:
        logger.error('Exception occurred: %s', e,
            exc_info=settings.get('DEBUG', False))
