import os
import json
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
curve_data_dir = os.path.join(BASE_DIR, 'data', 'contour')


def gen_format(li, var, n, l, xs, tn=0):
    dm = '\t' * tn + '%s = [' % var
    for i, x in enumerate(li):
        if i % n == 0:
            dm += '\n\t' + '\t' * tn
        dm += ('{: >%d},' % l).format(('{:.%df}' % xs).format(x))
    dm += '\n' + '\t' * tn + ']\n'
    return dm


def gen(file_path):
    dm = ''
    for _ in os.listdir(curve_data_dir):
        if _.endswith('.csv'):
            df = pd.read_csv(os.path.join(curve_data_dir, _), encoding='gbk')
            x = list(df.get('X轴'))
            xd = gen_format(x, 'x', 11, 7, 1, 1)
            y = list(df.get('Y轴'))
            yd = gen_format(y, 'y', 11, 7, 1, 1)
            z = list(df.get('Z轴'))
            zd = gen_format(z, 'z', 12, 7, 2, 1)
            dm += 'class HN%s:\n%s\n\n%s\n\n%s\n\n\n' % (
                _.replace('.csv', ''), xd.rstrip(), yd.rstrip(), zd.rstrip()
            )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(dm.replace('\t', '    '))
    return dm


# def gen():
#     ini = ''
#     for _ in os.listdir():
#         if _.endswith('.csv'):
#             dm = ''
#             df = pd.read_csv(_, encoding='gbk')
#             x = list(df.get('X轴'))
#             y = list(df.get('Y轴'))
#             z = list(df.get('Z轴'))
#             dm += "x = %s\ny = %s\nz = %s\n" % (
#                 json.dumps(x), json.dumps(y), json.dumps(z)
#             )
#             name = 'HN%s.py' % _.replace('.csv', '')
#             name = name.lower()
#             ini += 'from . import %s\n' % name.replace('.py', '')
#             with open(os.path.join('geo', name), 'w', encoding='utf-8') as f:
#                 f.write(dm.replace('\t', '    '))
#
#     with open(os.path.join('geo', '__init__.py'), 'w') as f:
#         f.write(ini)

#
# def gen():
#     ini = ''
#     for _ in os.listdir():
#         if _.endswith('.csv'):
#             df = pd.read_csv(_, encoding='gbk')
#             x = list(df.get('X轴'))
#             y = list(df.get('Y轴'))
#             z = list(df.get('Z轴'))
#
#             name = 'HN%s' % _.replace('.csv', '')
#             name = name.lower()
#             ini += 'from . import %s\n' % name
#
#             path_dir = os.path.join('geo', name)
#             os.makedirs(path_dir, exist_ok=True)
#             x_py = os.path.join('geo', name, 'lng.py')
#             y_py = os.path.join('geo', name, 'lat.py')
#             z_py = os.path.join('geo', name, 'elev.py')
#
#             with open(x_py, 'w', encoding='utf-8') as f:
#                 f.write('seq = %s' % json.dumps(x))
#             with open(y_py, 'w', encoding='utf-8') as f:
#                 f.write('seq = %s' % json.dumps(y))
#             with open(z_py, 'w', encoding='utf-8') as f:
#                 f.write('seq = %s' % json.dumps(z))
#             with open(os.path.join('geo', name, '__init__.py'), 'w') as f:
#                 f.write('from . import lng\nfrom . import lat\nfrom . import elev')
#
#     with open(os.path.join('geo', '__init__.py'), 'w') as f:
#         f.write(ini)



if __name__ == '__main__':
    gen('geo.py')
