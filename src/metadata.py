from utils import jsonx

METADATA_FILE = 'data/metadata.json'


def store(metadata):
    store_file = METADATA_FILE.replace('.json', '.formatted.json')
    jsonx.write(store_file, metadata)


def load():
    return jsonx.read(METADATA_FILE)


if __name__ == '__main__':
    metadata = load()
    store(metadata)
