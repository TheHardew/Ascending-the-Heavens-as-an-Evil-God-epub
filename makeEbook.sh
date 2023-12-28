#!/bin/bash

find chapters/ -type f | xargs -P "$(nproc)" -n 1 ./filterPage.py
./adjustToc.py
sed -i 's#<item#<opf:item#g' ebook/content.opf

rm ebook.epub
cd ebook
zip -0X ../ebook.epub mimetype
zip -9XrD ../ebook.epub * -x mimetype
