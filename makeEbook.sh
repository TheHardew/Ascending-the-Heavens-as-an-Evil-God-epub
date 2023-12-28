#!/bin/bash

find chapters/ -type f | xargs -P "$(nproc)" -n 1 ./filterPage.py
./adjustToc.py
sed -i 's#<item#<opf:item#g' ebook/content.opf

name='Ascending the Heavens as an Evil God.epub'
rm "$name"
cd ebook
zip -0X ../"$name" mimetype
zip -9XrD ../"$name" * -x mimetype
