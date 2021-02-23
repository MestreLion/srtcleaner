# This file is part of SRT Cleaner, see <https://github.com/MestreLion/srtcleaner>
# Copyright (C) 2021 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>

"""
    Platform-dependent methods in an implementation-independent way

Inspired by pyxdg, appdirs and xdgappdirs.
"""

import logging as _logging
import os as _os
import sys as _sys

CREATE_DIRS=True

# "Enums"
WINDOWS = 'win'
LINUX   = 'linux'
MACOS   = 'darwin'
UNKNOWN = ''  # Falsy value to allow `if not platform:`, as used below

# Py2/Py3 octal literals compatibility
MODE_ALL   = 511  # 0o777
MODE_OWNER = 448  # 0o700

# Let's pretend this module is 100% reusable: try top-level package
_APPTITLE = __name__.split('.')[0] if '.' in __name__ else ""


_log = _logging.getLogger(__name__)

_platform = _sys.platform.lower()
platform = (LINUX   if _platform.startswith(LINUX)   else
           (MACOS   if _platform.startswith(MACOS)   else
           (WINDOWS if _platform.startswith(WINDOWS) else
            UNKNOWN)))

if not platform:  # platform == UNKNOWN
    _log.warning("Unknown platform: %s", _sys.platform)

home = _os.path.expanduser('~')


# Data
if   platform == LINUX:
    data_home = _os.environ.get('XDG_DATA_HOME') or _os.path.join(home, '.local', 'share')
elif platform == MACOS:
    data_home = _os.path.join(home, 'Library', 'Application Support')
elif platform == WINDOWS:
    data_home = _os.environ.get('LOCALAPPDATA') or home
else:
    data_home = home


# Config
if   platform == LINUX:
    config_home = _os.environ.get('XDG_CONFIG_HOME') or _os.path.join(home, '.config')
elif platform == MACOS:
    # Do NOT use ~/Library/Preferences/ on MACOS! That's for .plists!
    # Use of XDG_DATA_HOME on Mac is debatable, and I'm intentionally deviating from spec,
    # using '~/Library/Application Support' instead of ~/.config as default *when not set*
    config_home = _os.environ.get('XDG_CONFIG_HOME') or data_home
else:
    config_home = data_home


# Cache
if   platform == LINUX:
    cache_home = _os.environ.get('XDG_CACHE_HOME') or _os.path.join(home, '.cache')
elif platform == MACOS:
    cache_home = _os.path.join(home, 'Library', 'Caches')
else:
    cache_home = data_home


# Logs
if   platform == MACOS:
    log_home = _os.path.join(home, 'Library', 'Logs')
else:
    log_home = cache_home


if _sys.version_info[0] >= 3:
    makedirs = _os.makedirs
else:
    def makedirs(name, mode=MODE_ALL , exist_ok=False):
        try:
            _os.makedirs(name, mode)
        except OSError as e:
            if e.errno != 17 or not exist_ok:
                raise


def _save_path(path, apptitle="", vendor=None, mode=MODE_ALL, suffix="", create=CREATE_DIRS):
    apptitle = apptitle or _APPTITLE
    if not apptitle or apptitle.startswith('/') or apptitle == '__main__':
        raise ValueError("Invalid App Title: {}".format(apptitle))
    assert not apptitle.startswith('/')
    if vendor is False or not platform == WINDOWS:
        path = _os.path.join(path, apptitle)
    elif vendor is None:
        path = _os.path.join(path, apptitle, apptitle)
    else:
        path = _os.path.join(path, vendor, apptitle)
    if suffix:
        path = _os.path.join(path, suffix)
    if create:
        makedirs(path, mode, exist_ok=True)
    return path


def save_data_path(apptitle="", vendor=None, create=CREATE_DIRS):
    """Return the data path for the application, optionally creating it.

    Data path is usually in the form ``<data_home>/[<vendor>/]<apptitle>``,
    <vendor> is used only on Windows and if not False, ignored otherwise,
    and defaults to <apptitle>.

    Use this when saving or updating application data.
    """
    return _save_path(data_home, apptitle, vendor, create=create)


def save_config_path(apptitle="", vendor=None, create=CREATE_DIRS):
    """Return the config path for the application, optionally creating it.

    Use this when saving or updating application settings and configuration.
    """
    return _save_path(config_home, apptitle, vendor, mode=MODE_OWNER, create=create)


def save_cache_path(apptitle="", vendor=None, create=CREATE_DIRS):
    """Return the cache path for the application, optionally creating it.

    Use this for temporary files.
    """
    suffix = 'Cache' if platform == WINDOWS else ""
    return _save_path(cache_home, apptitle, vendor, suffix=suffix, create=create)


def save_log_path(apptitle="", vendor=None, create=CREATE_DIRS):
    """Return the log path for the application, optionally creating it.

    Use this for log files.
    """
    if   platform == LINUX:   suffix = 'log'
    elif platform == WINDOWS: suffix = 'Logs'
    else:                     suffix = ''
    return _save_path(log_home, apptitle, vendor, mode=MODE_OWNER, suffix=suffix, create=create)
