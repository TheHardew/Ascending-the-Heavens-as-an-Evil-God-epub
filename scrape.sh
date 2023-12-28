#!/bin/bash

curl -s 'https://phoenixtls.wixsite.com/phoenixtl/chapter-index' | grep -o 'https://[^"]*post/chapter[^"]*' | while read -r link; do
	echo "$link"
	./scrapePage.py "$link"
	sleep 1
done
