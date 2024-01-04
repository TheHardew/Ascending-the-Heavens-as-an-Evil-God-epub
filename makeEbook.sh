#!/bin/bash

mkdir -p ebook/OEBPS/Text
python ./filterPages.py
python ./adjustToc.py

name='Ascending the Heavens as an Evil God.epub'
rm "$name"
cd ebook
zip -0X ../"$name" mimetype
zip -9XrD ../"$name" * -x mimetype | grep -vP '^\s*adding'
cd ..
ls -l "$name"
