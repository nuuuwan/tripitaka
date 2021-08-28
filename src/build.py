import os
import logging
from utils import dt, filex
from tripitaka.src import metadata, parse

DEFAULT_SOURCE = 'https://www.accesstoinsight.org/tipitaka'

log = logging.getLogger('tripitaka')
log.setLevel(logging.INFO)

def build():
    _metadata = metadata.load()
    os.system('rm -rf docs; mkdir docs')

    tripitaka_name = _metadata['name']
    tripitaka_link = _metadata.get('link', DEFAULT_SOURCE)
    tripitaka_summary = _metadata['summary']

    tripitaka_lines = [
        f'# {tripitaka_name}',
        f'Source: [{tripitaka_link}]({tripitaka_link})',
        '## Summary',
        f'{tripitaka_summary}',
        '## Pitakas, Nikayas & Suttas',
    ]

    for pitaka in _metadata['pitakas']:
        pitaka_id = pitaka['id']
        pitaka_name = pitaka['name']
        log.info(f'Building {pitaka_name}')
        pitaka_name_kebab = dt.to_kebab(pitaka_name)
        dir_pitaka_only = f'{pitaka_id}-{pitaka_name_kebab}'
        dir_pitaka = f'docs/{dir_pitaka_only}'
        os.system(f'mkdir {dir_pitaka}')

        tripitaka_lines.append(
            f'* [{pitaka_name}](./{dir_pitaka_only})',
        )

        pitaka_summary = pitaka.get('summary', '')
        pitaka_lines = [
            f'# {pitaka_name}',
            '## Summary',
            f'{pitaka_summary}',
            '## Nikayas & Suttas',
        ]

        nikayas = pitaka.get('nikayas', [])
        for nikaya in nikayas:
            nikaya_id = nikaya['id']
            nikaya_name = nikaya['name']
            log.info(f'  Building {nikaya_name}')
            nikaya_name_kebab = dt.to_kebab(nikaya_name)
            dir_nikaya_only = f'{nikaya_id}-{nikaya_name_kebab}'
            dir_nikaya = f'{dir_pitaka}/{dir_nikaya_only}'
            os.system(f'mkdir {dir_nikaya}')

            pitaka_lines.append(
                f'* [{nikaya_name}](./{dir_nikaya_only})',
            )
            tripitaka_lines.append(
                f'    *  [{nikaya_name}](./{dir_pitaka_only}/{dir_nikaya_only})',
            )

            nikaya_summary = nikaya.get('summary', '')
            nikaya_lines = [
                f'# {nikaya_name}',
                '## Summary',
                f'{nikaya_summary}',
                '## Suttas',
            ]

            suttas = nikaya.get('suttas', [])
            for sutta in suttas:
                sutta_link = sutta['link']
                if not sutta_link:
                    continue

                sutta_id = sutta['id']
                sutta_name = sutta['name']
                log.info(f'    Building {sutta_name}')
                sutta_name_kebab = dt.to_kebab(sutta_name)
                file_sutta_only = f'{sutta_id}-{sutta_name_kebab}.md'
                file_sutta = f'{dir_nikaya}/{file_sutta_only}'

                sutta_content = parse.parse_sutta(sutta_link)

                sutta_summary = sutta['summary']
                content = '\n'.join(
                    [
                        f'# {sutta_name}',
                        f'*{sutta_summary}*',
                        f'Source: [{sutta_link}]({sutta_link})',
                        '---',
                        '*%s*' % sutta_content['author'],
                    ]
                    + ['### Preface']
                    + sutta_content['preface_lines']
                    + ['### Chapter']
                    + sutta_content['chapter_lines'],
                )
                filex.write(file_sutta, content)

                nikaya_lines.append(
                    f'* [{sutta_name}](./{file_sutta_only})',
                )
                pitaka_lines.append(
                    f'    * [{sutta_name}](./{dir_nikaya_only}/{file_sutta_only})',
                )
                tripitaka_lines.append(
                    f'        * [{sutta_name}](./{dir_pitaka_only}/{dir_nikaya_only}/{file_sutta_only})',
                )

            nikaya_summary_file = f'{dir_nikaya}/README.md'
            filex.write(nikaya_summary_file, '\n'.join(nikaya_lines))
        pitaka_summary_file = f'{dir_pitaka}/README.md'
        filex.write(pitaka_summary_file, '\n'.join(pitaka_lines))
    tripitaka_summary_file = 'docs/README.md'
    filex.write(tripitaka_summary_file, '\n'.join(tripitaka_lines))


if __name__ == '__main__':
    build()
