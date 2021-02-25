# -*- coding: utf-8 -*-
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

"""Clean up SRT subtitle files removing ads, misplaced credits and fixing encoding"""

import argparse
import inspect
import logging
import os
import pkgutil
import shutil
import sys

# There's 3 `magic` modules in PyPI, all wrappers to libmagic, but with different API:
# - file-magic,   https://github.com/file/file, from libmagic itself
# - python-magic, https://github.com/ahupp/python-magic
# - filemagic,    https://github.com/aliles/filemagic
# `file-magic` is the one listed on setup.py, se we can assume it'll be available.
# But must handle all 3 so we don't force user to create a venv. See detect_encoding()
import magic
import pysrt

if __name__ == "__main__":
    sys.exit("This module should not run directly as a script."
             " Try `python -m srtcleaner`")

from . import __about__ as a
from . import apppaths


NAUTILUS_SCRIPT = a.__project__

log = logging.getLogger(__name__)


if sys.version_info[0] >= 3:
    PY3 = True
    unicode = str
    def fsig(f):
        return inspect.getfullargspec(f)[0]
    def printsubs(subs, encoding=None):  # @UnusedVariable
        for sub in subs:
            print(sub)
else:
    PY3 = False
    from io import open
    def fsig(f):
        return inspect.getargspec(f)[0]
    def printsubs(subs, encoding=None):
        for sub in subs:
            print(unicode(sub).encode(encoding or subs.encoding))


class ParseError(Exception):
    pass


def parseargs(argv=None):
    parser = argparse.ArgumentParser(
        prog=a.__title__, epilog=a.epilog,
        description='Clean subtitles deleting items that matches entries in blacklist file. '
            "Useful to remove ads and misplaced credits"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet', dest='loglevel',
                       action="store_const", const=logging.WARNING, default=logging.INFO,
                       help="Suppress informative messages and summary statistics.")

    group.add_argument('-v', '--verbose', dest='loglevel',
                       action="store_const", const=logging.DEBUG,
                       help="Print additional information for each processed file.")

    parser.add_argument('--recursive', '-r',
                        action="store_true", default=False,
                        help='recurse inside directories.')

    parser.add_argument('--input-encoding', '-e', dest="encoding",
                        help="Encoding used in subtitles, if known."
                             " By default tries to autodetect encoding.")

    parser.add_argument('--input-fallback-encoding', '-f', dest="fallback_encoding",
                        default="windows-1252",
                        help="Fallback encoding to read subtitles"
                            " if encoding autodetection fails. [Default: %(default)s]")

    parser.add_argument('--convert', '-c', dest="output_encoding",
                        help="Convert subtitle encoding."
                             " By default output uses the same encoding as the input.")

    parser.add_argument('--in-place', '-i',
                        action="store_true", default=False,
                        help="Overwrite original file"
                             " instead of outputting to standard output")

    parser.add_argument('--no-backup', '-B', dest="backup",
                        action="store_false", default=True,
                        help="When using --in-place, do not create a backup file.")

    parser.add_argument('--no-rebuild-index', '-I', dest="rebuild_index",
                        action="store_false", default=True,
                        help="Do not rebuild subtitles indexes after removing items."
                             " Resulting SRT will not be strictly valid,"
                             " although it will work in most players."
                             " Useful when debugging for comparing"
                             " original and modified subtitles")

    parser.add_argument('--blacklist', '-b', dest="blacklistpath",
                        default=get_blacklist_path(),
                        help="Blacklist file path. [Default: %(default)s]")

    parser.add_argument('--install-nautilus-script', '-N', dest='nautilus',
                        nargs='?', const=NAUTILUS_SCRIPT,
                        metavar='PATH',
                        help="Install Nautilus Script for SRT Cleaner at %(metavar)s."
                            " %(metavar)s can be either the script basename, optionally"
                            " prefixed with subdirs, that will be joined to your default"
                            " nautilus scripts path; or a full absolute path, including"
                            " the script basename, to install at an alternate location."
                            " [Default: %(const)r]")

    parser.add_argument('srtpaths',
                        nargs='*', metavar='PATH',
                        help='SRT file(s) or dir(s) to modify')

    return parser.parse_args(argv)


def install_nautilus_script(path):
    if not apppaths.platform == apppaths.LINUX:
        log.warning("Installing Nautilus Script in a non-Linux platform"
                    " is most likely pointless")
    path = os.path.join(apppaths.data_home, 'nautilus', 'scripts', path)
    apppaths.makedirs(os.path.dirname(path), exist_ok=True)
    log.debug("Nautilus Script path: %r", path)
    with open(path, 'wb') as f:
        f.write(pkgutil.get_data(__name__, 'data/nautilus-script.sh'))
    # Set executable flag
    mode = os.stat(path).st_mode
    mode |= (mode & 292) >> 2  # copy R bits to X. 292 = 0o444 (Py3) / 0444 (Py2)
    os.chmod(path, mode)
    return path


def get_blacklist_path(create=False):
    return os.path.join(apppaths.save_config_path(a.__title__, create=create),
                        "{}.conf".format(a.__title__))


def check_config(path):
    """Create the blacklist template if needed"""
    if path != get_blacklist_path() or os.path.isfile(path):
        # Not the default or default alredy exists, nothing to do
        return

    # Copy the default blacklist template
    path = get_blacklist_path(create=True)
    log.debug("Default blacklist path: %r", path)
    with open(path, 'w') as f:
        f.write(unicode(pkgutil.get_data(__name__, 'data/srtcleaner.template.conf'),
                        encoding='utf-8'))

    # Copy blacklist README
    readme = 'README.conf.txt'
    readme_path = os.path.join(os.path.dirname(path), readme)
    with open(readme_path, 'w') as f:
        f.write(unicode(pkgutil.get_data(__name__, os.path.join('data', readme)),
                        encoding='utf-8'))

    return path, readme_path


def find_subtitles(paths, recursive=False):
    def ext(path):
        return os.path.splitext(path)[1][1:].lower()

    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                if not recursive:
                    del dirs[:]
                for basename in files:
                    if ext(basename) == 'srt':
                        yield os.path.join(root, basename)
        else:
            if ext(path) == 'srt':
                yield path
            else:
                log.warn("Not an SRT file: '%s'", path)


def detect_encoding(filename, fallback=None):
    encoding = ""

    # file-magic, from `libmagic` upstream
    if hasattr(magic.Magic, "file"):
        ms = magic.open(magic.MAGIC_MIME_ENCODING)  # @UndefinedVariable
        ms.load()
        encoding = ms.file(filename)
        ms.close()

    # python-magic
    elif hasattr(magic.Magic, "from_file"):
        ms = magic.Magic(mime_encoding=True)
        encoding = ms.from_file(filename)
        del ms  # force automatic close()

    # filemagic
    else:
        with magic.Magic(flags=magic.MAGIC_MIME_ENCODING) as m:
            encoding = m.id_filename(filename)

    if encoding and encoding not in ['unknown-8bit', 'binary']:
        log.debug("Auto-detected encoding: '%s'", encoding)
        return encoding

    log.debug("Encoding auto-detection failed, using fallback: '%s'", fallback)
    return fallback


def open_subtitle(filename, encoding=None, fallback=None):
    '''Wrapper to pysrt.open() with encoding auto-detection
        could eventually be replaced with another parser to avoid this encoding madness
    '''
    if encoding is None:
        encoding = detect_encoding(filename, fallback=fallback)
    else:
        log.debug("Encoding: '%s'", encoding)

    try:
        return pysrt.open(filename, encoding=encoding)
    except UnicodeDecodeError as e:
        raise ParseError("error using encoding '%s': %r" % (encoding, e))


def clean(subs, blacklistfile, rebuild_index=True):
    try:
        with open(blacklistfile, 'r', encoding='utf-8') as fp:
            blacklist = fp.read().strip().split('\n\n')
    except IOError:
        return False

    deleted = []
    for i, sub in reversed(list(enumerate(subs))):
        for text in blacklist:
            if text.replace('\\n', '\n').lower() in sub.text.lower():
                deleted.append(sub)
                del subs[i]
                break

    if not deleted:
        return False

    for item in reversed(deleted):
        log.info(unicode(item).replace('\n', '\t').strip())
    log.info("%d items deleted", len(deleted))
    if rebuild_index:
        subs.clean_indexes()

    return True


def srtcleaner(
    srtpaths, blacklistpath,
    recursive=False,
    encoding=None, fallback_encoding="windows-1252", output_encoding=None,
    in_place=False, backup=True,
    rebuild_index=False
):
    """Main function"""
    for path in find_subtitles(srtpaths, recursive=recursive):
        log.info("Processing subtitle: '%s'", path)
        modified = False
        try:
            subs = open_subtitle(path,
                                 encoding=encoding,
                                 fallback=fallback_encoding)
        except ParseError as e:
            log.error("Could not open '%s': %s", path, e)
            continue

        modified = clean(subs, blacklistpath, rebuild_index=rebuild_index)

        if modified or output_encoding:
            if in_place:
                if backup:
                    shutil.copy(path, "{}.{}.bak".format(path, a.__title__))
                subs.save(encoding=output_encoding)
            else:
                printsubs(subs, encoding=output_encoding)


def cli(argv=None):
    """CLI entry point"""
    args = parseargs(argv)
    logging.basicConfig(level=args.loglevel, format='[%(levelname)-5s] %(message)s')
    log.debug("Arguments: %s", args)

    if args.nautilus:
        path = install_nautilus_script(args.nautilus)
        log.info("Nautilus script installed to %r", path)
        return

    if not args.srtpaths:
        log.error("No paths specified, see --help for usage.")
        return 1

    paths = check_config(args.blacklistpath)
    if paths:
        log.info("A basic blacklist file was created at %r,"
                 " edit it to customize. See %r for details.",
                 *paths)

    srtcleaner(**{_: getattr(args, _) for _ in fsig(srtcleaner)})
