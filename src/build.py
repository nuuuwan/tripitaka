import os
from utils import dt, filex
from tripitaka.src import metadata

DEFAULT_SOURCE = 'https://www.accesstoinsight.org/tipitaka'
def build():
    _metadata = metadata.load()
    os.system('rm -rf docs; mkdir docs')

    for pitaka in _metadata['pitakas']:
        pitaka_id = pitaka['id']
        pitaka_name = pitaka['name']
        pitaka_name_kebab = dt.to_kebab(pitaka_name)
        dir_pitaka_only = f'{pitaka_id}-{pitaka_name_kebab}'
        dir_pitaka = f'docs/{dir_pitaka_only}'
        os.system(f'mkdir {dir_pitaka}')

        pitaka_link = pitaka.get('link', '')
        if not pitaka_link:
            pitaka_link = DEFAULT_SOURCE
        pitaka_summary = pitaka.get('summary', '')
        pitaka_summary_file = f'{dir_pitaka}/README.md'
        pitaka_lines = [
            f'# {pitaka_name}',
            '',
            f'Source: [{pitaka_link}]({pitaka_link})',
            '',
            '## Summary',
            f'{pitaka_summary}',
            '',
            '## Nikayas & Suttas',
        ]

        nikayas = pitaka.get('nikayas', [])
        for nikaya in nikayas:
            nikaya_id = nikaya['id']
            nikaya_name = nikaya['name']
            nikaya_name_kebab = dt.to_kebab(nikaya_name)
            dir_nikaya_only = f'{nikaya_id}-{nikaya_name_kebab}'
            dir_nikaya = f'{dir_pitaka}/{dir_nikaya_only}'
            os.system(f'mkdir {dir_nikaya}')

            pitaka_lines.append(
                f'* {nikaya_id} - [{nikaya_name}](./{dir_nikaya_only})',
            )

            nikaya_link = nikaya.get('link', '')
            if not nikaya_link:
                pitaka_link = DEFAULT_SOURCE
            nikaya_summary = nikaya.get('summary', '')
            nikaya_summary_file = f'{dir_nikaya}/README.md'
            nikaya_lines = [
                f'# {nikaya_name}',
                '',
                f'Source: [{nikaya_link}]({nikaya_link})',
                '',
                '## Summary',
                f'{nikaya_summary}',
                '',
                '## Suttas',
            ]

            suttas = nikaya.get('suttas', [])
            for sutta in suttas:
                sutta_id = sutta['id']
                sutta_name = sutta['name']
                sutta_name_kebab = dt.to_kebab(sutta_name)
                file_sutta_only = f'{sutta_id}-{sutta_name_kebab}.md'
                file_sutta = f'{dir_nikaya}/{file_sutta_only}'
                sutta_link = sutta['link']
                if not sutta_link:
                    sutta_link = DEFAULT_SOURCE
                sutta_summary = sutta['summary']
                content = '\n'.join([
                    f'# {sutta_name}',
                    '',
                    f'Source: [{sutta_link}]({sutta_link})',
                    '',
                    '## Summary',
                    f'{sutta_summary}',
                ])
                filex.write(file_sutta, content)

                nikaya_lines.append(
                    f'*  {sutta_id} - [{sutta_name}](./{file_sutta_only})',
                )
                pitaka_lines.append(
                    f'  *  {sutta_id} - [{sutta_name}](./{dir_nikaya_only}/{file_sutta_only})',
                )

            filex.write(nikaya_summary_file, '\n'.join(nikaya_lines))

        filex.write(pitaka_summary_file, '\n'.join(pitaka_lines))




if __name__ == '__main__':
    build()
