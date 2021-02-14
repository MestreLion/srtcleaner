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
    Package setup

Mostly setup for usage as a library, such as exporting main names from modules
and adding NullHandler to package logger
"""

from .__about__ import (
    __title__,
    __project__,
    __description__,
    __url__,
    __version__,
    __version_info__,
    __author__,
    __email__,
    __copyright__,
)
from .srtcleaner import srtcleaner, cli

# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging
