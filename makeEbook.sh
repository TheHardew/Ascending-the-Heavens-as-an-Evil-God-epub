#!/bin/bash

mkdir -p ebook/OEBPS
find chapters/ -type f | xargs -P "$(nproc)" -n 1 python ./filterPage.py
python ./adjustToc.py
sed -i 's#<item#<opf:item#g' ebook/content.opf

name='Ascending the Heavens as an Evil God.epub'
rm "$name"
cd ebook
zip -0X ../"$name" mimetype
zip -9XrD ../"$name" * -x mimetype | grep -vP '^\s*adding'
cd ..
ls -l "$name"
