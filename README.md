SRT Cleaner
===========

A simple tool to clean up SRT subtitle files removing ads and misplaced credits,
also fixing their encoding.


Usage
-----

#### Library

```python
import srtcleaner

srtfiles = ['/data/TVSeries/Cosmos/Cosmos.S01E01.srt',
            '/data/TVSeries/Cosmos/Cosmos.S01E02.srt']

srtcleaner.srtcleaner(srtfiles, in_place=True, backup=False, convert='UTF-8')
```

#### Command-line

```
$ srtcleaner --help

usage: srtcleaner [-h] [-q | -v] [--recursive] [--input-encoding ENCODING]
                  [--input-fallback-encoding FALLBACK_ENCODING]
                  [--convert OUTPUT_ENCODING] [--in-place] [--no-backup]
                  [--no-rebuild-index] [--blacklist BLACKLISTPATH]
                  srtpaths [srtpaths ...]

Clean subtitles deleting items that matches entries in blacklist file. Useful
to remove ads and misplaced credits

positional arguments:
  srtpaths              SRT file(s) or dir(s) to modify

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Suppress informative messages and summary statistics.
  -v, --verbose         Print additional information for each processed file.
  --recursive, -r       recurse inside directories.
  --input-encoding ENCODING, -e ENCODING
                        Encoding used in subtitles, if known. By default tries
                        to autodetect encoding.
  --input-fallback-encoding FALLBACK_ENCODING, -f FALLBACK_ENCODING
                        Fallback encoding to read subtitles if encoding
                        autodetection fails. [Default: windows-1252]
  --convert OUTPUT_ENCODING, -c OUTPUT_ENCODING
                        Convert subtitle encoding. By default output uses the
                        same encoding as the input.
  --in-place, -i        Overwrite original file instead of outputting to
                        standard output
  --no-backup, -B       When using --in-place, do not create a backup file.
  --no-rebuild-index, -I
                        Do not rebuild subtitles indexes after removing items.
                        Resulting SRT will not be strictly valid, although it
                        will work in most players. Useful when debugging for
                        comparing original and modified subtitles
  --blacklist BLACKLISTPATH, -b BLACKLISTPATH
                        Blacklist file path. [Default:
                        /home/user/.config/srtcleaner/srtcleaner.conf]

Copyright (C) 2021 Rodrigo Silva. License: GPLv3 or later, at your choice.
$
$ srtcleaner -v --in-place -B --convert 'UTF-8' '/data/series/Cosmos/Cosmos.S01E01.srt'
[DEBUG] Auto-detected encoding: 'iso-8859-1'
[INFO ] 20      00:00:45,653 --> 00:00:48,842   <b>UNITED       apresenta</b>
[INFO ] 21      00:00:49,270 --> 00:00:52,638   <b>Legenda:     rickSG | .:FGMsp:.</b>
[INFO ] 741     00:46:55,499 --> 00:46:58,557   UNITED  Quality is Everything!
[INFO ] 3 items deleted

$ srtcleaner -v --in-place -B --convert 'UTF-8' '/data/series/Cosmos/Cosmos.S01E01.srt'
[DEBUG] Auto-detected encoding: 'utf-8'
```


Configuring
-----------

SRT Cleaner will remove any entries that matches any record on its blacklist file,
located by default at `~/.config/srtcleaner/srtcleaner.conf`. Create or edit it
before using `srtcleaner`.

A record can span over multiple lines, so use a blank line to separate each record.
Its text is matched against each SRT entry by a simple `text in entry` comparison,
in a _case-insensitive_ way. So if the whole text is found as part of an entry,
the whole entry is removed from the SRT file. Escape sequences such as `\n` and
`\t` are also interpreted, so you can use `\n` when you want to include a newline
at the end of the text to match.

Leave the default blacklist empty for no SRT entry removal, for example when using
SRT Cleaner just for converting the SRT file encoding, otherwise SRT Cleaner might
re-create the blacklist with a basic set of records.

Example of a basic `srtcleaner.conf`:
```
OpenSubtitles.org

facebook.com/

fb.com/

@gmail.com

Resync

Legendas:\n

UNITED4EVER

UNITED
Quality is everything

<b>UNITED
Qualidade É Tudo</b>

INSUBS\n

L.O.T.S\n
```


Requirements
------------
- Python 2.7 or 3.6+
- [Pysrt](https://github.com/byroot/pysrt), to parse the SRT files
- [file-magic](https://github.com/file/file), to detect encoding.

**Note**: There are (at least) 3 python modules named `magic` available on
PyPI, all wrappers to [`libmagic`](https://github.com/file/file),
but with very distinct API:

  - [file-magic](https://github.com/file/file), from `libmagic` project itself
  - [python-magic](https://github.com/ahupp/python-magic)
  - [filemagic](https://github.com/aliles/filemagic)

SRT Cleaner supports any of the above `libmagic` wrappers, and on install pulls
the one from the `file`/`libmagic` project. And all of them obviously requires
`libmagic` to be installed on your system. It usually ships in the `file`
package and comes pre-installed in most GNU/Linux distributions and MacOS.

On Windows, the following could be used to install `libmagic`:
- [file-windows](https://github.com/nscaife/file-windows)
- [libmagicwin64](https://github.com/pidydx/libmagicwin64)


Installing
----------

#### From Git:

```sh
git clone https://github.com/MestreLion/srtcleaner
cd srtcleaner
python3 -m srtcleaner [ARGS...]           # Run/Test prior to installing
pip3 install --user .                     # Regular install, OR
pip3 install --user --no-use-pep517 -e .  # Editable/Development install
```

#### From PyPi:

```sh
pip3 install --user srtcleaner
```


Contributing
------------

Patches are welcome! Fork, hack, request pull!

If you find a bug or have any enhancement request, please open a
[new issue](https://github.com/MestreLion/srtcleaner/issues/new)


Author
------

Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>


License and Copyright
---------------------
```
Copyright (C) 2021 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```
