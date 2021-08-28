import re
import json
from bs4 import BeautifulSoup
from utils import www

URL_ROOT = 'https://www.accesstoinsight.org/tipitaka/mn/'

REGEX_TITLE = r'\w{1}N (?P<num_str>\d+):\s(?P<title_str>.+)\s—\s(?P<title_description_str>.+)'


def parse(html_file, parent_id):
    html = www.read(html_file)
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
    parse(
        'https://www.accesstoinsight.org/tipitaka/dn/index.html',
        '2.1',
    )
