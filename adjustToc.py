#!/usr/bin/python3
from bs4 import BeautifulSoup
from natsort import natsorted
import os

def get_title(file):
    with open(file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    return soup.find('h1').get_text()

os.chdir('ebook/OEBPS')

with open('toc.xhtml', 'r', encoding='utf-8') as file:
    soupX = BeautifulSoup(file, 'html.parser')

ol = soupX.find('ol')
ol.clear()

with open('toc.ncx', 'r', encoding='utf-8') as file:
    soupN = BeautifulSoup(file, 'xml')

nm = soupN.find('navMap')
nm.clear()

with open('content.opf', 'r', encoding='utf-8') as file:
    soupO = BeautifulSoup(file, 'xml')

mani = soupO.find('manifest')
mani.clear()

mani.append(BeautifulSoup(f'<item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>', 'xml'))
mani.append(BeautifulSoup(f'<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>', 'xml'))
mani.append(BeautifulSoup(f'<item id="cover" href="Images/cover.jpeg" media-type="image/jpeg"/>', 'xml'))
mani.append(BeautifulSoup(f'<item id="cover-page" href="titlepage.xhtml" media-type="application/xhtml+xml" properties="svg"/>', 'xml'))

spine = soupO.find('spine')
spine.clear()
    
i = 0
for f in natsorted(os.listdir('Text')):
    f = os.path.join('Text', f)
    li = soupX.new_tag('li')
    a = soupX.new_tag('a', href=str(f))
    title = get_title(f)
    a.string = title
    li.append(a)
    ol.append(li)

    np = soupN.new_tag('navPoint')
    np['class'] = 'chapter'
    np['id'] = f'navPoint-{i}'
    np['playOrder'] = f'{i + 1}'
    nm.append(np)

    nl = soupN.new_tag('navLabel')
    np.append(nl)

    t = soupN.new_tag('text')
    nl.append(t)
    t.string = title

    np.append(BeautifulSoup(f'<content src="{f}"/>', 'xml'))

    mani.append(BeautifulSoup(f'<item id="chapter_{i+1}" href="{f}" media-type="application/xhtml+xml"/>', 'xml'))
    spine.append(BeautifulSoup(f'<itemref idref="chapter_{i+1}"/>', 'xml'))

    i += 1


with open('toc.xhtml', 'w', encoding='utf-8') as file:
    file.write(str(soupX.prettify()))

with open('toc.ncx', 'w', encoding='utf-8') as file:
    file.write(str(soupN.prettify()))

with open('content.opf', 'w', encoding='utf-8') as file:
    file.write(str(soupO.prettify()))


