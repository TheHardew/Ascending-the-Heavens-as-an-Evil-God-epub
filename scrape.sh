#!/usr/bin/env bash

mkdir -p chapters
curl -s 'https://phoenixtls.wixsite.com/phoenixtl/chapter-index' | grep -o 'https://[^"]*post/chapter[^"]*' | while read -r link; do
	file=$(echo "$link" | grep -oP 'chapter-\d+')
	if [ ! -f chapters/"$file" ]; then
		./scrapePage.py "$link"
	fi
done
