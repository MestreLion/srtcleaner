#!/bin/sh
#
# Nautilus script for SRT Cleaner
#
# Copy or symlink to '~/.local/share/nautilus/scripts' or to your system equivalent,
#   or run `srtcleaner --install-nautilus-script`
#
# Copyright (C) 2021 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>

srtcleaner --recursive --convert UTF-8 --no-backup --in-place "$@" 2>&1 |
if type zenity >/dev/null 2>&1 ; then
	zenity --text-info --title "Clean Subtitles" \
		--no-wrap --width=1000 --height=500
else
	cat
fi
