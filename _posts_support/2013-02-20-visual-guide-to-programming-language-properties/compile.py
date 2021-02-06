#!/usr/bin/env python

import os
import os.path
import re
import subprocess
import sys


def main(args):
    if len(args) >= 2 and args[0] == '--image-directory-url':
        images_urlpath = args[1]
        args = args[2:]
    else:
        images_urlpath = ''
    
    if not os.path.exists('gen'):
        os.mkdir('gen')
    
    for input_filename in args:
        if not '.dot' in input_filename:
            raise ValueError('Expected input filename to contain ".dot": ' + input_filename)
        
        with open(input_filename, 'rb') as input_file:
            input = input_file.read()
        
        langs = set(re.findall(r'\bL_[A-Z]+\b', input))
        langs.add('L_ALL')
        
        # Compile images
        for output_lang in langs:
            output = compile_dot(input, output_lang, langs)
            
            # Write compiled .dot
            dot_filename = 'gen/' + input_filename.replace('.dot', '.' + output_lang[2:] + '.dot')
            with open(dot_filename, 'wb') as output_file:
                output_file.write(output)
            
            # Generate image from .dot
            image_filename = dot_filename.replace('.dot', '.gif')
            subprocess.check_call(['dot', '-Tgif', dot_filename, '-o', image_filename])
        
        # Compile HTML inclusion fragment
        include_filename = 'gen/' + input_filename.replace('.dot', '.html.inc')
        with open(include_filename, 'wb') as output_file:
            output_file.write(compile_html_include(input_filename, langs, images_urlpath))
        
        # Compile HTML preview
        compile_html_preview(input_filename)


def compile_dot(input, output_lang, langs):
    output_lines = input.split('\n')
    for (i, line) in enumerate(output_lines):
        line_has_any_lang = any((lang in line for lang in langs))
        if line_has_any_lang:
            node_enabled = (output_lang in line) or (output_lang == 'L_ALL')
            if not node_enabled:
                if ']' not in line:
                    raise ValueError('Expected line to contain "]": ' + line)
                output_lines[i] = line.replace(']', ', color=gray, fontcolor=gray]')
    
    return '\n'.join(output_lines)


def compile_html_include(input_filename, langs, images_urlpath=''):
    lang_infos = [
        ('L_ALL', 'All'),
        ('L_CPP', 'C++'),
        ('L_OBJC', 'Objective-C'),
        ('L_JAVA', 'Java'),
        ('L_HASKELL', 'Haskell'),
        ('L_PYTHON', 'Python'),
        ('L_RUBY', 'Ruby'),
        ('L_LISP', 'Lisp'),
    ]
    langs_with_info = [x for (x, _) in lang_infos]
    if set(langs_with_info) != set(langs):
        raise ValueError
    
    OUTER_TEMPLATE = """
<ul class="nav nav-tabs">%(tab_headers)s
</ul>
<div class="tab-content">%(tab_contents)s
</div>"""
    
    TAB_HEADER_ITEM_TEMPLATE = """
  <li class="%(cls)s">
    <a href="#%(ref)s" class="tab-header tab-header-%(lang)s" data-toggle="tab">%(title)s</a>
  </li>"""
    TAB_CONTENT_ITEM_TEMPLATE = """
  <a class="tab-pane %(cls)s" id="%(ref)s" href="%(img_src)s">
    <img src="%(img_src)s" style="max-width: 100%%;" />
  </a>"""
    
    tab_header_items = []
    tab_content_items = []
    for (lang, title) in lang_infos:
        props = dict(
            cls='active' if lang == 'L_ALL' else '',
            ref=input_filename.replace('.dot', '') + '-' + lang[2:],
            lang=lang[2:],
            img_src=images_urlpath + input_filename.replace('.dot', '') + '.' + lang[2:] + '.gif',
            title=title
        )
        
        tab_header_items.append(TAB_HEADER_ITEM_TEMPLATE % props)
        tab_content_items.append(TAB_CONTENT_ITEM_TEMPLATE % props)
    
    return OUTER_TEMPLATE % dict(
        tab_headers=''.join(tab_header_items),
        tab_contents=''.join(tab_content_items)
    )


def compile_html_preview(input_filename):
    PREVIEW_TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <title>Preview</title>
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/css/bootstrap-combined.min.css" rel="stylesheet">
    <style>
      .tab-content { overflow: auto; }
      .tab-content img { max-width: none; }
    </style>
  </head>
  <body>%(included)s
    
    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/js/bootstrap.min.js"></script>
  </body>
</html>
    """
    
    include_filename = 'gen/' + input_filename.replace('.dot', '.html.inc')
    with open(include_filename, 'rb') as input_file:
        included = input_file.read()
    
    preview = PREVIEW_TEMPLATE % dict(
        included=included
    )
    
    preview_filename = 'gen/' + input_filename.replace('.dot', '.preview.html')
    with open(preview_filename, 'wb') as output_file:
        output_file.write(preview)

if __name__ == '__main__':
    main(sys.argv[1:])