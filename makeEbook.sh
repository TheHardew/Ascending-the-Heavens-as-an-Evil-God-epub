#!/usr/bin/env bash

mkdir -p ebook/OEBPS/Text
./filterPages.py
./adjustToc.py

name='Ascending the Heavens as an Evil God.epub'
rm -f "$name"
cd ebook
zip -0X ../"$name" mimetype
zip -9XrD ../"$name" * -x mimetype | grep -vP '^\s*adding'
cd ..
ls -l "$name"
