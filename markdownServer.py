import flask
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
print(BASE_DIR)

from cnhydropy.utils import md2html
from cnhydropy.utils.markdown_file_tree import Tree

app = flask.Flask(__name__)

@app.route('/')
def index():
    tree = Tree(root_dir=path)
    return """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html>
        <head>
        <title>文档</title>
        </head>
        <body>
            %s
        </body>
        </html>
    """ % tree()


@app.route('/docs')
def html():
    args = flask.request.args
    file_name = os.path.join(path, args.get('f'))
    title = args.get('t')
    if not os.path.exists(file_name):
        return "文件不存在！"
    else:
        html = md2html.MD2Html(file_name, title=title)
        return html.html


if __name__ == '__main__':
    help_str = """
使用方法：
python app.py path
path: 需要查看的路径。
"""
    try:
        path = sys.argv[1]
        if path == '--help':
            print(help_str)
        elif not os.path.exists(path):
            print('指定路径不存在')
        else:
            app.run()
    except IndexError:
        print(help_str, '\n')
