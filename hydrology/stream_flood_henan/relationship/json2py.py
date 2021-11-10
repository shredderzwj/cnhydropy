import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
curve_data_dir = os.path.join(BASE_DIR, 'data', 'relationship')


def gen(file_path):
    dm = ''
    for _ in os.listdir(curve_data_dir):
        if _.endswith('.json'):
            name = _.replace('.json', '').replace('-', '_').replace('+', '_').lower().strip()
            with open(os.path.join(curve_data_dir, _)) as f:
                v = f.read().strip()
            dm += '%s = %s\n' % (name, v)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(dm.replace('\t', '    '))
    return dm


if __name__ == '__main__':
    print(gen('mapping.py'))
