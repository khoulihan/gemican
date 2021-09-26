#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Kevin Houlihan'
SITENAME = 'Gemican Docs'
SITEURL = 'gemini://localhost:1966'

SITEASCII = """
             =: --              -- :=
           =||||||*-          -*||||||=
         +%%%%%%%%%|*-      -*||||||||||=
       +%@@@@@@@@@@%%|*-  -*||||||||%|||||=
    .+%@@@@@@@*-|@@@@%%|*|@@%||||*-*@%%|||||=
   +%@@@@@@@*:   -|@@@@%%||%@@%*:   .*@%%|||||=
   -@@@@@@|:       -|@@@@%%||%-       .|||||||-
   |@@@@@%|*:     -  -|@@@@%%|*-     :+|||||||*.
    =%@@@@%|*:  -%@%=  -|@@@@%%|-  :+||||||||-
      =%@@%=  -|%@@@@%=  -|@@%+. :*||||||||-
        =%%+-%%|||%@@|-    -+. :*||||||||-
          -  *||||||+        :*||||||||-
            -%@%|||||*:    :+||||||||-
              =%@%|||||*::+||||||||-
                =%@%|||||||||||||-
                  =%@%|||||||||-
                    =%@%||%||-
                      =|--|=
"""

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

MARKDOWN = {
    'links': 'at-end',
    'code_tag': 'Code/command example',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Blog', 'https://blog.hyperlinkyourheart.com/'),
    ('Portfolio', 'https://portfolio.hyperlinkyourheart.com/'),
    ('YouTube', 'https://www.youtube.com/channel/UCc_O9Hp5UfQ-IHswi1H54Zg'),
)

# Social widget
SOCIAL = (('Mastodon', 'https://mastodon.art/@hyperlinkyourheart'),
          ('Twitter', 'https://twitter.com/http_your_heart'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

THEME = 'themes/gemican_docs'
TEMPLATE_EXTENSIONS = ['.gmi', '.gemini']

INDEX_SAVE_AS = 'articles.gmi'
