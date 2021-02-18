import os
import re

from md2html import MD2Html


class Documentation(object):
    principle_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'principle.md')
    documentation_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
    source_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frequency.py')

    @staticmethod
    def get_md_str(path, **kwargs):
        with open(path, **kwargs) as f:
            return f.read()

    @staticmethod
    def get_html_str(path, **kwargs):
        try:
            return MD2Html(path, **kwargs).html
        except NameError:
            raise NameError('MD2Html类未定义')

    def principle_html(self, **kwargs):
        return self.get_html_str(self.principle_file_path, **kwargs)

    def documentation_html(self, **kwargs):
        return self.get_html_str(self.documentation_file_path, **kwargs)

    def principle_and_documentation_html(self, **kwargs):
        principle_md_str = self.get_md_str(self.principle_file_path, encoding='utf-8')
        documentation_md_str = self.get_md_str(self.documentation_file_path, encoding='utf-8')
        merge_md_str = re.sub(r'\[TOC\]', '', '%s\n\n%s' % (principle_md_str, documentation_md_str))
        merge_md_str = '[TOC]\n\n%s' % merge_md_str
        return self.get_html_str(merge_md_str, from_str=True, **kwargs)

    def source_html(self, **kwargs):
        return self.get_html_str(self.source_file_path, **kwargs)

