import types
from typing import Dict, Any
import os

import minify_html
from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file


def copy_custom_files(app):
    if app.builder.format == 'html':
        staticdir = os.path.join(app.builder.outdir, '_static')
        banner_css = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'banner.css',
        )
        banner_js = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'banner.js',
        )
        try:
            os.makedirs(staticdir)
        except OSError:
            pass
        copy_asset_file(banner_css, staticdir)
        copy_asset_file(banner_js, staticdir)


def insert_sidebar(app, pagename, templatename, context, doctree):
    app.add_js_file("banner.js")
    app.add_css_file("banner.css")
    if (
        not hasattr(app.builder.templates.render, '_deepmodeling_patched')
    ):
        old_render = app.builder.templates.render

        def render(self, template, render_context):
            content = old_render(template, render_context)
            comment_begin = r"<!--deepmodeling begin-->"
            comment_end = r"<!--deepmodeling end-->"
            if comment_begin in content:
                return content
            begin_body = content.lower().find('</head>')
            source = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'banner.html',
            )
            with open(source) as f:
                banner = f.read()
            if begin_body != -1:
                content = content[:begin_body] + comment_begin + \
                    banner + comment_end + content[begin_body:]
            return content

        render._deepmodeling_patched = True
        app.builder.templates.render = types.MethodType(render,
                                                        app.builder.templates)


def minify_html_files(app, pagename, templatename, context, doctree):
    if (
        not hasattr(app.builder.templates.render, '_deepmodeling_minified')
    ):
        old_render = app.builder.templates.render

        def render(self, template, render_context):
            content = old_render(template, render_context)
            return minify_html.minify(content, minify_css=True, minify_js=True,
                                      keep_comments=True,
                                      keep_html_and_head_opening_tags=True,
                                      keep_spaces_between_attributes=True)

        render._deepmodeling_minified = True
        app.builder.templates.render = types.MethodType(render,
                                                        app.builder.templates)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.connect('builder-inited', copy_custom_files)
    app.connect('html-page-context', insert_sidebar)
    app.connect('html-page-context', minify_html_files)

    return {'parallel_read_safe': True}
