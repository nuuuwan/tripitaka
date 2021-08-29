import re
import json
from bs4 import BeautifulSoup
from utils import www, jsonx
from utils.cache import cache

URL_ROOT = 'https://www.accesstoinsight.org/tipitaka/mn/'

REGEX_TITLE = r'\w{1}N (?P<num_str>\d+):\s(?P<title_str>.+)\s—\s(?P<title_description_str>.+)'


@cache('tripitaka', 86400)
def parse_sutta(sutta_id, sutta_name_kebab, html_url):
    sutta_file = f'data/suttas/{sutta_id}-{sutta_name_kebab}.json'
    if os.path.exists(sutta_file):
        sutta = jsonx.read(sutta_file)
        return sutta

    html = www.read(html_url)
    soup = BeautifulSoup(html, 'html.parser')

    div_preface = soup.find('div', class_="preface")
    preface_lines = []
    if div_preface:
        preface_lines = list(
            filter(
                lambda line: len(line.strip()) > 0,
                div_preface.text.split('\n'),
            )
        )

    div_chapter = soup.find('div', class_="chapter")
    chapter_lines = []
    if div_chapter:
        chapter_lines = list(
            filter(
                lambda line: len(line.strip()) > 0,
                div_chapter.text.split('\n'),
            )
        )

    div_author = soup.find('div', {'id': 'H_docAuthor'})
    author = ''
    if div_author:
        author = div_author.text

    sutta = dict(
        author=author,
        preface_lines=preface_lines,
        chapter_lines=chapter_lines,
    )
    jsonx.write(sutta_file, sutta)
    return sutta


def parse_metadata(html_url, parent_id):
    html = www.read(html_url)
    soup = BeautifulSoup(html, 'html.parser')

    ul_suttas = soup.find('ul', class_="suttaList")
    suttas = []
    for li_sutta in ul_suttas.find_all('li'):
        span_title = li_sutta.find('span', class_="sutta_title")
        a_link = span_title.find('a')
        link = ''
        if a_link and a_link.get('href'):
            link = URL_ROOT + a_link.get('href')[2:]
        title = span_title.text
        result = re.search(REGEX_TITLE, title)
        if not result:
            continue
        data = result.groupdict()
        child_id = data.get('num_str')
        id = f'{parent_id}.{child_id}'
        name = data.get('title_str')

        div_summary = li_sutta.find('div', class_="sutta_summary")
        summary = div_summary.text.strip()

        sutta = dict(
            name=name,
            id=id,
            link=link,
            summary=summary,
            source="https://www.accesstoinsight.org/tipitaka",
        )
        suttas.append(sutta)
    print(json.dumps(suttas, indent=2))


if __name__ == '__main__':
    print(
        parse_sutta(
            'https://www.accesstoinsight.org/tipitaka/dn/dn.02.0.than.html'
        )
    )
