#!/usr/bin/python3
from bs4 import BeautifulSoup
import os
import sys
import re
import multiprocessing as mp

def process_file(filename):
    parts = filename.split('/')
    with open(filename, 'r') as file:
        text = file.read()

    soup = BeautifulSoup(text, 'lxml')
    title = extract_title(soup)
    target_tag = soup.find('div', class_='fTEXDR')

    result = re.search(r'(chapter-\d+)', parts[1]).group(1)
    if target_tag is not None:
        target_tag = change_lines(target_tag, soup)
        target_tag = transform_main_text(target_tag, soup)
        target_tag = link(target_tag, soup)
        target_tag = remove_divs(target_tag, soup)
        target_tag = remove_styles(target_tag)
        write_file(result + '.xhtml', title, target_tag)

def link(root, soup):
    i = 1
    while True:
        patternTN = rf'^\s*\[\s*{i}\s*\].*'
        patternNote = re.compile(rf'\s*\[\s*{i}\s*\].*')

        note = root.find(string=patternNote)
        ref = root.find(lambda tag: tag.name == 'p' and re.match(patternTN, tag.get_text()) and tag.get('id', ''))

        if not note and not ref:
            break

        if ref == None:
            print(root)
            print(i)
    
        link_to_ref = soup.new_tag('a', href= '#' + ref.attrs['id'])
        note.wrap(link_to_ref)
        #link_to_ref.attrs['id'] = f'note-to-{i}'

        #link_to_note = soup.new_tag('a', href=f'#note-to-{i}')
        #link_to_note.string = 'Back'
        #new_span = soup.new_tag('span')
        #new_span.append(link_to_note)
        #new_span['style'] = 'margin-left: 1em'
        #ref.append(new_span)

        i += 1

    return root


def remove_styles(root):
    for d in root.find_all('style'):
        d.decompose()

    return root


def write_file(filename, title, tag):
    with open(os.path.join('ebook/OEBPS/Text', filename), 'w', encoding='utf-8') as output_file:
        output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output_file.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
        output_file.write('<head>\n')
        output_file.write(f'<title>{title}</title>\n')
        output_file.write('</head>\n')
        output_file.write('<body>\n')
        output_file.write('<h1 class="h4 title" itemprop="headline">')
        output_file.write(title)
        output_file.write('</h1>')
        while len(tag.contents) == 1:
            tag = tag.contents[0]
        for c in tag.contents:
            output_file.write(str(c))
        output_file.write('</body>\n')
        output_file.write('</html>')

def transform_main_text(root, soup):
    for header in root.find_all('h6', id=lambda x: x and x.startswith('viewer-')):
        secondChild = header.find()
        if not secondChild:
            print(header)

        p_tag = soup.new_tag('p')
        p_tag['id'] = header.get('id')
        for c in list(secondChild.contents):
            p_tag.append(c)
        header.replace_with(p_tag)

    for tag in soup.find_all(True):
        if tag.has_attr('class'):
            tag['class'] = ''
            del tag['class']

    for tag in soup.find_all(True):
        if tag.has_attr('id') and tag['id'].startswith('viewer-'):
            tag['id'] = tag['id'][7:]

    return root

def change_lines(root, soup):
    for l in root.find_all('line'):
        h = soup.new_tag('hr')
        ancestor_div = l.find_parent('div', id=lambda x: x and x.startswith('viewer-'))
        if ancestor_div:
            ancestor_div.insert_after(h)
            ancestor_div.decompose()

    return root

def check_only_font_size(span):
    style_options = span['style'].split(';')
    return len(style_options) == 1 and style_options[0].strip().lower().startswith('font-size')


def remove_divs(root, soup):
    for div in soup.find_all('div', {'data-hook': lambda x: x and x.startswith('rcv-block')}):
        div.extract()

    for d in root.find_all('div', {'data-breakout': 'normal'}):
        d.unwrap()

    texts = ['Next Chapter', 'Previous Chapter', 'Index']
    for t in texts:
        while (d := root.find(lambda tag: tag.name == 'div' and t in tag.get_text() and tag.get('id', ''))) != None:
            d.decompose()

    start_text = 'Game System Inspired Note'
    tag_to_remove = root.find(lambda tag: tag.name == 'p' and start_text in tag.get_text())
    while tag_to_remove and tag_to_remove.name != 'hr':
        next_tag = tag_to_remove.find_next_sibling()
        tag_to_remove.decompose()
        tag_to_remove = next_tag
    if tag_to_remove:
        tag_to_remove.decompose()

    start_text = 'If you see something wrong'
    first_target_child = root.find(lambda tag: tag.name == 'p' and start_text in tag.get_text())
    if first_target_child:
        for sibling in first_target_child.find_next_siblings():
            sibling.decompose()
        first_target_child.decompose()

    for d in root.find_all(lambda tag: tag.name == 'div' and tag.get_text() == ''):
        d.decompose()

    for span in soup.find_all('span'):
        if 'style' not in span.attrs or check_only_font_size(span):
            span.unwrap()

    return root
    

def extract_title(root):
    t = root.find('span', class_='blog-post-title-font')
    return t.get_text() if t else ''

def main():
    files = [os.path.join('chapters', file_name) for file_name in os.listdir('chapters')]
    with mp.Pool() as pool:
        pool.map(process_file, files)

if __name__ == '__main__':
    main()
