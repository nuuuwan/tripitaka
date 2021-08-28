from utils import jsonx
METADATA_FILE = 'data/metadata.json'


def store_metadata(metadata):
    store_file = METADATA_FILE.replace('.json', '.copy.json')
    jsonx.write(store_file, metadata)

def load_metadata():
    return jsonx.read(METADATA_FILE)


if __name__ == '__main__':
    metadata = load_metadata()
    store_metadata(metadata)
