#!/bin/bash

mkdir -p ebook/OEBPS/Text
find chapters/ -type f | xargs -P "$(nproc)" -n 1 python ./filterPage.py
python ./adjustToc.py

name='Ascending the Heavens as an Evil God.epub'
rm "$name"
cd ebook
zip -0X ../"$name" mimetype
zip -9XrD ../"$name" * -x mimetype | grep -vP '^\s*adding'
cd ..
ls -l "$name"
