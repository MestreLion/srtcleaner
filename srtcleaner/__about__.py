# SRT Cleaner - Clean up SRT subtitle files removing ads and misplaced credits
#
#    Copyright (C) 2021 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. See <http://www.gnu.org/licenses/gpl.html>

"""
    Project metadata

The single source of truth for version number and related information.
Must be truly self-contained: do not import modules or read external files
Preferably only trivial string manipulations and basic list/tuple/dict operations
"""


# Main
# Literals only

__title__        = "srtcleaner"  # could be inferred from basename(dirname(__file__))
__project__      = "SRT Cleaner"
__description__  = "Clean up SRT subtitle files removing ads and misplaced credits."
__url__          = "https://github.com/MestreLion/srtcleaner"

__author__       = "Rodrigo Silva (MestreLion)"
__email__        = "linux@rodrigosilva.com"

__version__      = "1.1.0"

__license__      = "GPLv3+"
__copyright__    = "Copyright (C) 2021 Rodrigo Silva"


# ../setup.py
# https://pypi.org/classifiers/
python_requires  = '>=2.7'  # Adjust __classifiers__ accordingly!
classifiers      = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "License :: DFSG approved",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Multimedia :: Video",
    "Topic :: Text Processing",
    "Topic :: Utilities",
]
keywords         = "subtitles srt library"
entry_points     = {
    'console_scripts': ['{__title__} = {__title__}:cli'.format(**locals())]
}
install_requires = [
    'pysrt',
    'file-magic',
]
extras_require   = {}
readme           = "README.md"
project_urls     = {"Bug Tracker": __url__ + "/issues", "Source Code": __url__}
package_data     = {'': ['data/*']}
setup_options    = {  # replaces setup.cfg
    'metadata'   : {'license_file': 'LICENSE'},  # Include in sdist without MANIFEST.in
    'bdist_wheel': {'universal': '1'},  # For pure-python, compatible with both 2 and 3
}


# Argument parsing
epilog = """{__copyright__}.
License: GPLv3 or later, at your choice.
""".format(**locals())


# Possibly irrelevant
__status__ = "Production"


# Derived data
__version_info__ = tuple(map(int, __version__.split('-')[0].split('+')[0].split('.')[:3]))
if len(__version_info__) < 3: __version_info__ = (__version_info__ + 3*(0,))[:3]
