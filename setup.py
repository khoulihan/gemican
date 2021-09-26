#!/usr/bin/env python

from os import walk
from os.path import join, relpath

from setuptools import find_packages, setup


version = "5.0.0"

requires = ['feedgenerator >= 1.9', 'jinja2 >= 2.7', 'pygments',
            'docutils>=0.15', 'pytz >= 0a', 'blinker', 'unidecode',
            'python-dateutil', 'rich']

entry_points = {
    'console_scripts': [
        'gemican = gemican.__main__:main',
        'gemican-import = gemican.tools.gemican_import:main',
        'gemican-quickstart = gemican.tools.gemican_quickstart:main',
        'gemican-themes = gemican.tools.gemican_themes:main',
        'gemican-plugins = gemican.plugins._utils:list_plugins'
    ]
}

README = open('README.rst', encoding='utf-8').read()
CHANGELOG = open('docs/content/changelog.md', encoding='utf-8').read()

description = '\n'.join([README, CHANGELOG])

setup(
    name='gemican',
    version=version,
    url='https://github.com/khoulihan/gemican',
    author='Kevin Houlihan',
    author_email='kevin@crimsoncookie.com',
    description="Static Gemini capsule generator supporting GemText",
    project_urls={
        'Documentation': 'https://docs.getpelican.com/',
        'Source': 'https://github.com/khoulihan/gemican',
        'Tracker': 'https://github.com/khoulihan/gemican/issues',
    },
    keywords='static web site generator SSG Markdown gemini',
    license='AGPLv3',
    long_description=description,
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    include_package_data=True,  # includes all in MANIFEST.in if in package
    # NOTE : This will collect any files that happen to be in the themes
    # directory, even though they may not be checked into version control.
    package_data={  # gemican/themes is not a package, so include manually
        'gemican': [relpath(join(root, name), 'gemican')
                    for root, _, names in walk(join('gemican', 'themes'))
                    for name in names],
    },
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Framework :: Gemican',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='gemican.tests',
)
