import types
from typing import Dict, Any
import os

import htmlmin
from jsmin import jsmin
from cssmin import cssmin
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


def insert_icp(app, pagename, templatename, context, doctree):
    if (
        not hasattr(app.builder.templates.render, '_deepmodeling_icp_patched')
    ):
        old_render = app.builder.templates.render

        def render(self, template, render_context):
            content = old_render(template, render_context)
            comment_begin = r"<!--deepmodeling icp begin-->"
            comment_end = r"<!--deepmodeling icp end-->"
            if comment_begin in content:
                return content
            footer = content.lower().find('</footer>')
            icp_footer = '<p><a href="https://beian.miit.gov.cn" target="_blank">京ICP备20010051号-8</a></p>'
            if footer != -1:
                content = content[:footer] + comment_begin + \
                    icp_footer + comment_end + content[footer:]
            return content

        render._deepmodeling_icp_patched = True
        app.builder.templates.render = types.MethodType(render,
                                                        app.builder.templates)


def minify_html_files(app, pagename, templatename, context, doctree):
    if (
        not hasattr(app.builder.templates.render, '_deepmodeling_minified')
    ):
        old_render = app.builder.templates.render

        def render(self, template, render_context):
            content = old_render(template, render_context)
            return htmlmin.minify(content)

        render._deepmodeling_minified = True
        app.builder.templates.render = types.MethodType(render,
                                                        app.builder.templates)


def minify_js_files(app, exception):
    if not hasattr(app.builder, "script_files"):
        # not html builder
        return
    for js in app.builder.script_files:
        fn = os.path.join(app.builder.outdir, js)
        if os.path.isfile(fn):
            with open(fn, 'r+') as f:
                minified_js = jsmin(f.read())
                f.seek(0)
                f.write(minified_js)
                f.truncate()


def minify_css_files(app, exception):
    if not hasattr(app.builder, "css_files"):
        # not html builder
        return
    for css in app.builder.css_files:
        fn = os.path.join(app.builder.outdir, css)
        if os.path.isfile(fn):
            with open(fn, 'r+') as f:
                minified_css = cssmin(f.read())
                f.seek(0)
                f.write(minified_css)
                f.truncate()


def setup(app: Sphinx) -> Dict[str, Any]:
    app.connect('builder-inited', copy_custom_files)
    app.connect('html-page-context', insert_sidebar)
    app.connect('html-page-context', insert_icp)
    app.connect('build-finished', minify_js_files)
    app.connect('build-finished', minify_css_files)

    return {'parallel_read_safe': True}
