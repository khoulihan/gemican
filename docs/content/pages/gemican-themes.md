Title: Gemican Themes
Date: 2021-09-25 22:38
Authors: Kevin Houlihan, Justin Mayer, Alexis Metaireau, contributors
Summary: Gemican Themes

## Description

`gemican-themes` is a command line tool for managing themes for Gemican.
See settings/themes for settings related to themes.

### Usage

```
gemican-themes [-h] [-l] [-i theme path [theme path ...]]
               [-r theme name [theme name ...]]
               [-s theme path [theme path ...]] [-v]
               [--version]
```

### Optional arguments:

```
-h, --help                                Show the help an exit

-l, --list                                Show the themes already installed

-i theme_path, --install theme_path       One or more themes to install

-r theme_name, --remove theme_name        One or more themes to remove

-s theme_path, --symlink theme_path       Same as "--install", but create a
                                          symbolic link instead of copying the
                                          theme.
                                          Useful for theme development

-v, --verbose                             Verbose output

--version                                 Print the version of this script
```

## Examples

### Listing the installed themes

With `gemican-themes`, you can see the available themes by using the
`-l` or `--list` option:

    $ gemican-themes -l
    hyper
    two-column@
    simple
    $ gemican-themes --list
    hyper
    two-column@
    simple

In this example, we can see there are three themes available:
`hyper`, `simple`, and `two-column`.

`two-column` is prefixed with an `@` because this theme is not copied to
the Gemican theme path, but is instead just linked to it (see `Creating
symbolic links` for details about creating symbolic links).

Note that you can combine the `--list` option with the `-v` or
`--verbose` option to get more verbose output, like this:

    $ gemican-themes -v -l
    /usr/local/lib/python2.6/dist-packages/gemican-2.6.0-py2.6.egg/gemican/themes/hyper
    /usr/local/lib/python2.6/dist-packages/gemican-2.6.0-py2.6.egg/gemican/themes/two-column (symbolic link to `/home/skami/Dev/Python/gemican-themes/two-column`)
    /usr/local/lib/python2.6/dist-packages/gemican-2.6.0-py2.6.egg/gemican/themes/simple

### Installing themes

You can install one or more themes using the `-i` or `--install` option.
This option takes as argument the path(s) of the theme(s) you want to
install, and can be combined with the verbose option:

    # gemican-themes --install ~/Dev/Python/gemican-themes/hyper-cms --verbose

    # gemican-themes --install ~/Dev/Python/gemican-themes/hyper-cms\
                               ~/Dev/Python/gemican-themes/martyalchin \
                               --verbose

    # gemican-themes -vi ~/Dev/Python/gemican-themes/two-column

### Removing themes

The `gemican-themes` command can also remove themes from the Gemican
themes path. The `-r` or `--remove` option takes as argument the name(s)
of the theme(s) you want to remove, and can be combined with the
`--verbose` option.

    # gemican-themes --remove two-column

    # gemican-themes -r martyachin hyper-cmd -v

### Creating symbolic links

`gemican-themes` can also install themes by creating symbolic links
instead of copying entire themes into the Gemican themes path.

To symbolically link a theme, you can use the `-s` or `--symlink`, which
works exactly as the `--install` option:

    # gemican-themes --symlink ~/Dev/Python/gemican-themes/two-column

In this example, the `two-column` theme is now symbolically linked to
the Gemican themes path, so we can use it, but we can also modify it
without having to reinstall it after each modification.

This is useful for theme development:

    $ sudo gemican-themes -s ~/Dev/Python/gemican-themes/two-column
    $ gemican ~/Blog/content -o /tmp/out -t two-column
    $ firefox /tmp/out/index.gmi
    $ vim ~/Dev/Gemican/gemican-themes/two-column/static/css/main.css
    $ gemican ~/Blog/content -o /tmp/out -t two-column
    $ cp /tmp/bg.png ~/Dev/Gemican/gemican-themes/two-column/static/img/bg.png
    $ gemican ~/Blog/content -o /tmp/out -t two-column
    $ vim ~/Dev/Gemican/gemican-themes/two-column/templates/index.gmi
    $ gemican ~/Blog/content -o /tmp/out -t two-column

### Doing several things at once

The `--install`, `--remove` and `--symlink` option are not mutually
exclusive, so you can combine them in the same command line to do more
than one operation at time, like this:

    # gemican-themes --remove hyper-cms two-column \
                     --install ~/Dev/Python/gemican-themes/hyper-cms-fr \
                     --symlink ~/Dev/Python/gemican-themes/two-column \
                     --verbose

In this example, the theme `hyper-cms` is replaced by the theme
`hyper-cms-fr`
