#!/usr/bin/env python
"""
Generates the output for the /prism directory inside /_site.

Converts any .shtml files encountered to plain .html files.

Usage:
    python _plugins/prism.py
"""

import os
import os.path
import shutil
import re
import sys


def main(args):
    for (dirpath, dirnames, filenames) in os.walk('prism'):
        out_dirpath = os.path.join('_site', dirpath)
        if not os.path.exists(out_dirpath):
            os.mkdir(out_dirpath)
        
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            out_filepath = os.path.join(out_dirpath, filename)
            
            if filename.endswith('.shtml'):
                out_filepath = os.path.splitext(out_filepath)[0] + '.html'
                convert_shtml_to_html(filepath, out_filepath)
            else:
                shutil.copyfile(filepath, out_filepath)


def convert_shtml_to_html(in_filepath, out_filepath):
    regex = re.compile(br'<!--#include virtual="([^"]*)" -->')
    file_contents = lambda filename: open(filename, 'rb').read()
    resolve_path = lambda filepath: \
        filepath if not filepath.startswith('/') else ('.' + filepath)
    match_ssi = lambda match: ssi(file_contents(resolve_path(match.group(1))))
    ssi = lambda txt: regex.sub(match_ssi, txt)
    
    # HACK: Assumes the specified filepath ends with 'index.shtml'.
    #       Does not actually check.
    def chop_index_shtml_suffix(filepath):
        return os.path.dirname(filepath) + '/'
    
    with open(out_filepath, 'wb') as out_file:
        out_file.write(ssi(file_contents(in_filepath)).replace(
            '<!--#echo var="SCRIPT_NAME" -->',
            '/' + chop_index_shtml_suffix(in_filepath)))


if __name__ == '__main__':
    main(sys.argv[1:])