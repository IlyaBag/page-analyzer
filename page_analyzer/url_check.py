from bs4 import BeautifulSoup


def url_check(content):
    soup = BeautifulSoup(content, 'html.parser')

    h1 = soup.h1
    tag_h1 = ''
    if h1:
        tag_h1_strings = [elem for elem in h1.strings]
        tag_h1 = ''.join(tag_h1_strings)

    title = soup.title
    tag_title = ''
    if title:
        tag_title_strings = [elem for elem in title.strings]
        tag_title = ''.join(tag_title_strings)

    meta = soup.find('meta', attrs={'name': 'description', 'content': True})
    tag_meta_descr = meta.get('content') if meta else ''

    return (tag_h1, tag_title, tag_meta_descr)
