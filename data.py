from utils import jsonx
METADATA_FILE = 'data/metadata.json'

def load_metadata():
    return jsonx.read(METADATA_FILE)


if __name__ == '__main__':
    load_metadata()
