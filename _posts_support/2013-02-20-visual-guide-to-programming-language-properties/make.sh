#!/bin/sh

python compile.py \
    --image-directory-url /assets/2013/2013-02-20-visual-guide-to-programming-language-properties/ \
    *.dot
cp gen/*.gif ../../assets/2013/2013-02-20-visual-guide-to-programming-language-properties/
cp gen/*.html.inc ../../_includes/2013/2013-02-20-visual-guide-to-programming-language-properties/
