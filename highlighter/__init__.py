"""Flask module
file: __init__.py
date: 12.12.2012
author smith@example.com
license: MIT"""

from flask import Flask, render_template, request, Markup
import re

def create_app():
    """Create flask app for binding."""
    app = Flask(__name__)

    template_file_name = 'index.html'

    @app.route('/', methods=['GET'])
    def index(): #pylint: disable=w0612
        return render_template(template_file_name)

    @app.route('/', methods=['POST'])
    def process():#pylint: disable=w0612
        search_text = request.form['search']
        case_sensitive = int(request.form['case_sensitive'])
        text = request.form['text']
        highlighted_text = highlight_text(text, search_text, case_sensitive)
        result = {'text': text,
                  'highlighted_text': Markup(highlighted_text),
                  }
        return render_template(template_file_name, **result)

    def markup_text(text):
        """Markup given text.
        This is supplementary method that helps you to wrap marked text in tags.
        @:param text - string text to be marked
        @:return marked text, e.g., <mark>highlighted text</mark>."""
        result = "<mark>" + text + "</mark>"
        return result

    def highlight_text(text, expr, case_sensitive):
        """Markup searched string in given text.
        @:param text - string text to be processed (e.g., 'The sun in the sky')
        @:param expr - string pattern to be searched in the text (e.g., 'th')
        @:return marked text, e.g., "<mark>Th</mark>e sun in <mark>th</mark>e sky"."""
#         if expr in text:
#             text = text.replace(expr, markup_text(expr))
#         result = text
#         return result
        if case_sensitive == 0:
            if expr in text:
                text = text.replace(expr, markup_text(expr))
        elif case_sensitive == 1:
            if expr.lower() in text.lower():
                insensitive_hippo = re.compile(re.escape(expr), re.IGNORECASE)
                text = insensitive_hippo.sub(markup_text(expr), text)
        result = text
        return result        

    return app
