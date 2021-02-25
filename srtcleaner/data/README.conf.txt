SRT Cleaner will remove any entries that matches any record on the blacklist file,
`srtcleaner.conf`. This default can be changed per-run using the command line
argument '--blacklist FILE', see `srtcleaner --help` for details.

A record can span over multiple lines, so use a blank line to separate each record.
Its text is matched against each SRT entry by a simple `text in entry` comparison,
in a _case-insensitive_ way. So if the whole text is found as part of an entry,
the whole entry is removed from the SRT file. Escape sequences such as `\n` and
`\t` are also interpreted, so you can use `\n` when you want to include a newline
at the end of the text to match.

Leave the default blacklist empty for no SRT entry removal, for example when using
SRT Cleaner just for converting the SRT file encoding, otherwise SRT Cleaner might
re-create the blacklist with a basic set of records.
