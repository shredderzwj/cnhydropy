from pathlib import Path
import os


class Tree(object):
    def __init__(self, api_path='docs', root_dir=os.path.dirname(os.path.abspath(__file__))):
        self.tree_str = ""
        self.api = api_path
        self.root_dir = root_dir

    def __call__(self):
        top = self.root_dir
        self.tree_str = ""
        self.top = Path(top)
        return self.__tree(top)

    def __tree(self, top, tabs=0):
        top = Path(top)
        flag = 1
        if self.top.name == top.name:
            flag = 0
        if top.is_dir():
            self.tree_str += '|&nbsp;&nbsp;&nbsp;&nbsp;' * (tabs - 1) + "|---"*flag + '<b>%s</b><br>' % top.name
            for x in top.iterdir():
                self.__tree(x, tabs + 1)
        else:
            if top.name.split('.')[-1] in ['md', 'markdown']:
                file = str(top.absolute()).replace(self.root_dir, '.')
                # title = top.absolute().parent.name + top.name
                title = top.name
                self.tree_str += '|&nbsp;&nbsp;&nbsp;&nbsp;' * (tabs - 1) + "|---<a href=/%s?f=%s&t=%s target=_blank>" % (self.api, file, title) + title + '</a></b><br>'
        return self.tree_str
