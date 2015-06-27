#!/usr/bin/env python
"""
Ensures that no two posts have the same date,
which can cause problems with Atom feeds.

Usage:
    python _plugins/checkdates.py
"""

from collections import Counter
import os
import re
import sys


POST_DATE_RE = re.compile(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})-')


def main(args):
    post_filenames = os.listdir('_posts')
    post_date_matchers = [POST_DATE_RE.search(fn) for fn in post_filenames]
    post_dates = [m.groups() for m in post_date_matchers if m is not None]
    
    duplicate_dates_detected = False
    for (date, freq) in Counter(post_dates).iteritems():
        if freq > 1:
            print('*** Multiple posts detected with date: %s' % repr(date))
            duplicate_dates_detected = True
    
    if duplicate_dates_detected:
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])