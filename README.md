Various tools
=============

This is a collection of miscellaneous tools for my personal use. Some of the
might not work out-of-the-box and require some tweaking. Most are also not
documented particularly well.

## Contents

* `anonymize_token.py`: Transform a secret token into an anonymized one.
* `apache_stats.py`: Generate statistics from Apache common log files.
* `apparmor_logparse.py`: Parse apparmor logging and print out all operations
  performed by a binary.
* `bta_latest_linker.py`: Create symlinks in a dir pointing the latest files
  in a list of source dirs.
* `bta_latest.py`: Print the latest episode of a season found on disk.
* `bta_norm.py`: Find downloaded TV series torrent files and normalize/move
  them.
* `chrome_socks.sh`: Start a Chrome(ium) browser on a Socks 5 proxy. This
  causes all traffic in the browser to travel through the proxy, which makes
  it seem like the browser is running remotely. This is useful for access
  resources on private networks without having to set up a manual tunnel or
  traditional VPN.
* `java_jar2jad.sh`: Convert .jar to .jad
* `mem_usage.sh`: Print real memory usage, sorted.
* `mysql_fix_debsysmaint.sh`: Fix broken MySQL authentication for
  `debian-sys-maint.sh` user, which happens when you import a dump including the
  `mysql` schema.
* `trac_update_url.py`: Search and replace a URL with a new URL in a Trac
  database.
* `php_logcolor.py`: Show colorized PHP log files.
