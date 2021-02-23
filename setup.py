#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of SRT Cleaner, see <https://github.com/MestreLion/legendastv>
# Copyright (C) 2021 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>

"""Build/Install script. For the actual metadata, see srtcleaner/__about__.py"""

import mimetypes
import os
import sys

if sys.version_info[0] < 3:
    from io import open  # open(..., encoding) support for Python 2.x

from setuptools import find_packages, setup


packages = find_packages(exclude=["tests", "tests.*"])
project = packages[0]
here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, project, '__about__.py'), encoding='utf-8') as fp:
    exec(fp.read(), about)

with open(os.path.join(here, about['readme']), encoding='utf-8') as fp:
    readme = fp.read().strip()

kwargs = dict(
    name             = about['__title__'],
    version          = about['__version__'],
    author           = about['__author__'],
    author_email     = about['__email__'],
    url              = about['__url__'],
    description      = about['__description__'],
    license          = about['__license__'],
    python_requires  = about['python_requires'],
    classifiers      = about['classifiers'],
    keywords         = about['keywords'],
    entry_points     = about['entry_points'],
    install_requires = about['install_requires'],
    extras_require   = about['extras_require'],
    project_urls     = about['project_urls'],
    package_data     = about['package_data'],
    options          = about['setup_options'],
    packages         = packages,
    long_description = readme,
    long_description_content_type = mimetypes.guess_type(about['readme'])[0],
)

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    python = sys.executable
    os.system('{} -m pip install --user --upgrade setuptools wheel twine'.format(python))
    os.system('rm -rf build */*.egg-info *.egg-info')
    os.system('{} setup.py sdist bdist_wheel'.format(python))
    os.system('twine upload dist/*')
    sys.exit()

if sys.argv[-1] == 'checkargs':
    import pprint
    pprint.pprint(kwargs)
    sys.exit()

if __name__ == '__main__':
    setup(**kwargs)
