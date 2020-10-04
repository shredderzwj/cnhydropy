# -*- coding: utf-8 -*-
# pip install markdown python-markdown-math


import markdown as md
from mdx_math import MathExtension


class Head(object):
    style = """
    <style type="text/css">
        pan.MathJax_SVG {
            zoom: 1.2;
        }

        @font-face {
            font-family: 'wdsong';
            // src: url('./font/wd-song.ttf');
            font-weight: lighter;
        }

        @font-face {
            font-family: 'ubuntu-mono';
            // src: url('./font/ubuntu-mono.ttf');
            font-weight: lighter;
        }

        @media screen {
            html {
                background-repeat: repeat-x repeat-y;
                background-color: #F2F2F2;
                padding: 16px;
            }

            body {
                background-repeat: repeat-x repeat-y;
                width: auto;
                max-width: 800px;
                min-width: 640px;
                margin: auto;
                margin-top: 0px;
                margin-bottom: 64px;
                padding: 50px;
                // background-color: #E6DBBD;
				background-color: #FAEED7;
                // background-image:url(data:image/jpeg;base64,base64_str);
                // background-size:cover; 
                border-radius: 1px;
                box-shadow: 0px 0px 16px #808080;
                word-wrap: break-word;
                line-height: 150%;
                font-family: 'wdsong';
                color: #101010;
            }

            h1 {
                margin-top: 64px;
                margin-bottom: 48px;
                padding-bottom: 16px;
                text-align: center;
                font-weight: 900;
                font-size: xx-large;
            }

            h2 {
                background-repeat: repeat-x repeat-y;
                margin-top: 32px;
                margin-left: -50px;
                margin-right: -50px;
                padding-left: 50px;
                padding-top: 32px;
                padding-bottom: 16px;
                // border-top: dotted thin #CCCCCC;
                font-weight: bold;
                font-size: x-large;
            }

            h3 {
                margin-top: 24px;
                margin-bottom: 24px;
                padding-bottom: 6px;
                // color: #004499;
                // border-bottom: dotted thin #000000;
                line-height: 100%;
                font-weight: bold;
                font-size: large;
            }

            h4 {
                background-repeat: no-repeat;
                height: 24px;
                margin-bottom: 24px;
                padding-top: 6px;
                /* padding-left      : 48px; */
                line-height: 100%;
                font-weight: bold;
            }

            p {
                text-indent: 32px;
            }

            ol p, ul p {
                text-indent: 1px;
            }

            ol, ul {
                padding-left: 64px;
                padding-right: 48px;
            }

            b {
                margin: 4px;
                color: #004499;
            }

            a {
                color: #0070D0;
            }

            code {
                font-family: 'ubuntu-mono';
                color: #00aa00;
                background-color: #000000;
                word-wrap:break-word;
                word-break:break-all;
                overflow: hidden;
            }

            p code, ol code, ul code {
                padding-top: -1px;
                padding-bottom: 2px;
                padding-left: 4px;
                padding-right: 4px;
                background-color: #000000;
                box-shadow: 0px 0px 4px #D0D0D0 inset;
                border-radius: 4px;
            }

            pre code {
                padding: 0px;
                box-shadow: 0px 0px 0px #D0D0D0;
                border-radius: 4px;
                // background-color: #000000;
            }

            pre {
                background-repeat: no-repeat;
                margin: 10px;
                margin-left: 30px;
                margin-right: 30px;
                padding: 10px;
                background-color: #000000;
                box-shadow: 0px 0px 4px #D0D0D0 inset;
                border-radius: 4px;
                line-height: 130%;
            }

            blockquote {
                background-repeat: no-repeat;
                margin: 10px;
                padding: 10px;
                margin-left: 20px;
                margin-right: 20px;
                background-color: #FCFCFC;
                color: #606060;
                box-shadow: 0px 0px 16px #888888;
                border-radius: 2px;
                line-height: 130%;
                font-size: small;
            }

            table {
                margin-bottom: 10px;
                margin-left: 32px;
                margin-right: 32px;
                box-shadow: 0px 0px 4px #888888;
                border-collapse: collapse;
                border: 1px solid #888888;
                text-align: center;
                font-size: x-small;
                width: 90%;
            }

            th {
                padding: 2px;
                padding-left: 4px;
                padding-right: 4px;
                background-color: #E0E0E0;
                font-family: 黑体;
                font-style: normal;
                font-weight: bold;
                font-size: x-small;
                border: 1px solid #888888;
            }

            td {
                padding: 2px;
                padding-left: 4px;
                padding-right: 4px;
                background-color: #FCFCFC;
                font-family: 'wdsong';
                /* border           : 1px dotted #888888; */
                border: 1px solid #888888;
            }

            center {
                font-size: x-small;
                font-weight: bold;
            }
        }

        @media print {
            html {
                background-repeat: repeat-x repeat-y;
                background-color: #ECECEC;
                padding: 16px;
            }

            body {
                background-repeat: repeat-x;
                width: auto;
                max-width: 800px;
                min-width: 640px;
                margin: auto;
                margin-top: 0px;
                // margin-bottom: 64px;
                padding: 25px;
                background-color: #FFFFFF;
                /*  border-radius    : 1px;
                box-shadow       : 0px 0px 16px #808080; */
                word-wrap: break-word;
                line-height: 180%;
                font-family: 'wdsong';
                color: #000000;
            }

            h1 {
                margin-top: 32px;
                margin-bottom: 32px;
                padding-bottom: 16px;
                text-align: center;
                font-weight: 900;
                font-size: xx-large;
            }

            h2 {
                background-repeat: repeat-x repeat-y;
                margin-top: 16px;
                margin-left: -50px;
                margin-right: -50px;
                padding-left: 50px;
                padding-top: 24px;
                padding-bottom: 16px;
                // border-top: dotted thin #CCCCCC;
                font-weight: bold;
                font-size: x-large;
            }

            h3 {
                margin-top: 18px;
                margin-bottom: 18px;
                padding-bottom: 6px;
                // color: #004499;
                // border-bottom: dotted thin #000000;
                line-height: 100%;
                font-weight: bold;
                font-size: large;
            }

            h4 {
                background-repeat: no-repeat;
                height: 24px;
                margin-bottom: 16px;
                padding-top: 6px;
                /* padding-left      : 48px; */
                line-height: 100%;
                font-weight: bold;
            }

            p {
                text-indent: 32px;
            }

            ol p, ul p {
                text-indent: 1px;
            }

            ol, ul {
                padding-left: 64px;
                padding-right: 48px;
            }

            b {
                margin: 4px;
                color: #004499;
            }

            a {
                color: #0070D0;
            }

            code {
                font-family: 'ubuntu-mono';
            }

            p code, ol code, ul code {
                padding-top: -1px;
                padding-bottom: 2px;
                padding-left: 4px;
                padding-right: 4px;
                background-color: #FAFAFA;
                box-shadow: 0px 0px 4px #D0D0D0 inset;
                border-radius: 4px;
            }

            pre code {
                padding: 0px;
                box-shadow: 0px 0px 0px #D0D0D0;
                border-radius: 4px;
            }

            pre {
                background-repeat: no-repeat;
                margin: 10px;
                margin-left: 30px;
                margin-right: 30px;
                padding: 10px;
                background-color: #FAFAFA;
                box-shadow: 0px 0px 4px #D0D0D0 inset;
                border-radius: 4px;
                line-height: 130%;
            }

            blockquote {
                background-repeat: no-repeat;
                margin: 10px;
                padding: 10px;
                margin-left: 20px;
                margin-right: 20px;
                background-color: #FCFCFC;
                color: #606060;
                box-shadow: 0px 0px 16px #888888;
                border-radius: 2px;
                line-height: 130%;
                font-size: small;
            }

            table {
                margin-bottom: 10px;
                margin-left: 32px;
                margin-right: 32px;
                box-shadow: 0px 0px 4px #888888;
                border-collapse: collapse;
                border: 1px solid #888888;
                text-align: center;
                font-size: x-small;
                width: 90%;
            }

            th {
                padding: 2px;
                padding-left: 4px;
                padding-right: 4px;
                background-color: #E0E0E0;
                font-family: 黑体;
                font-style: normal;
                font-weight: bold;
                font-size: x-small;
                border: 1px solid #888888;
            }

            td {
                padding: 2px;
                padding-left: 4px;
                padding-right: 4px;
                background-color: #FCFCFC;
                font-family: 'wdsong';
                /* border           : 1px dotted #888888; */
                border: 1px solid #888888;
            }

            center {
                font-size: x-small;
                font-weight: bold;
            }
            
            #no-print {
                display: none;
            }
            //.author {
            //    display: none;
            //}
        }
    </style>
    """

    js = """
    <script src="https://cdn.bootcss.com/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
    <script src="https://libs.baidu.com/jquery/1.3.1/jquery.min.js"></script>
    <script>
    (function($) {
        var opt;
    
        $.fn.jqprint = function (options) {
            opt = $.extend({}, $.fn.jqprint.defaults, options);
    
            var $element = (this instanceof jQuery) ? this : $(this);
            
            if (opt.operaSupport && $.browser.opera) 
            { 
                var tab = window.open("","jqPrint-preview");
                tab.document.open();
    
                var doc = tab.document;
            }
            else 
            {
                var $iframe = $("<iframe  />");
            
                if (!opt.debug) { $iframe.css({ position: "absolute", width: "0px", height: "0px", left: "-600px", top: "-600px" }); }
    
                $iframe.appendTo("body");
                var doc = $iframe[0].contentWindow.document;
            }
            
            if (opt.importCSS)
            {
                if ($("link[media=print]").length > 0) 
                {
                    $("link[media=print]").each( function() {
                        doc.write("<link type='text/css' rel='stylesheet' href='" + $(this).attr("href") + "' media='print' />");
                    });
                }
                else 
                {
                    $("link").each( function() {
                        doc.write("<link type='text/css' rel='stylesheet' href='" + $(this).attr("href") + "' />");
                    });
                }
            }
            
            if (opt.printContainer) { doc.write($element.outer()); }
            else { $element.each( function() { doc.write($(this).html()); }); }
            
            doc.close();
            
            (opt.operaSupport && $.browser.opera ? tab : $iframe[0].contentWindow).focus();
            setTimeout( function() { (opt.operaSupport && $.browser.opera ? tab : $iframe[0].contentWindow).print(); if (tab) { tab.close(); } }, 1000);
        }
        
        $.fn.jqprint.defaults = {
            debug: false,
            importCSS: true, 
            printContainer: true,
            operaSupport: true
        };
    
        // Thanks to 9__, found at http://users.livejournal.com/9__/380664.html
        jQuery.fn.outer = function() {
          return $($('<div></div>').html(this.clone())).html();
        } 
    })(jQuery);
    </script>
    """


class MD2Html(Head):
    def __init__(self, md=None, title="md2html", from_str=False, encoding='utf-8'):
        """

        :param md: str markdown 文件路径或者 markdown 内容。默认为文件路径，当from_str = True 时 md 代表内容
        :param title: str 输出 html 的标题
        :param from_str: str 输入字符是否为 markdown 内容
        :param encoding: str md文件的编码方式
        """
        self.title = title
        self.head = '''
            <head>
            <title>%s</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            %s
            </head>
        ''' % (self.title, self.style + self.js)
        if from_str:
            self.md_str = md
        else:
            self.md_str = self.from_file(md, encoding)

    def from_file(self, file_path, encoding):
        """
        with open(file_path, 'r', encoding=encoding, *args, **kwargs) as fp:
            return fp.read()
        """
        with open(file_path, 'r', encoding=encoding) as fp:
            return fp.read()

    def set_head(self, html_head_str):
        """
        设置 html 文件的 <head> 内容
        :param html_head_str:  str html 文件的 <head> 内容
        :return:  None
        """
        self.head = html_head_str

    @property
    def html(self):
        """
        输出转换后的 html 字符串
        :return: str html 内容
        """
        exts = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'mdx_math',
            MathExtension(enable_dollar_delimiter=True),
        ]
        return """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
            %s
            <body>
                <div id='contain'>
                %s
                </div>
                <div id='no-print' style-"text-align: center">
                    <hr style="margin-top:50px">
                    <input type="button" onclick="printPage();" value="打印本页"/>
                </div>
                <script>
                    printPage = function(){
                        $('html').jqprint();
                    };
                </script>
            </body>
            </html>
        """ % (self.head, md.markdown(self.md_str, extensions=exts))

    def save_html(self, file_path, encoding='utf-8'):
        """
        保存 html 文件
        :param file_path: str html 文件
        :return: None
        """
        with open(file_path, 'w', encoding=encoding) as fp:
            fp.write(self.html)

