import types
from typing import Dict, Any
import os
from pathlib import Path

import htmlmin
from jsmin import jsmin
from cssmin import cssmin
from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file
from jinja2 import Template


from .config import sitemap, active_class, icp_no


def render_banner(current_site='Docs') -> str:
    """Use jinja2 to render banner.
    
    Returns
    -------
    str
        HTML content of banner.
    """
    source = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'banner.html',
    )
    with open(source) as f:
        template = Template(f.read())
    for item in sitemap:
        if item['title'] == current_site:
            item['class'] = active_class
    return template.render(
        items=sitemap,
    )


def copy_custom_files(app):
    if not app.config.enable_deepmodeling:
        return
    if app.builder.format == 'html':
        staticdir = os.path.join(app.builder.outdir, '_static')
        cwd = Path(__file__).parent.absolute()
        banner_css = cwd / 'banner.css'
        banner_js = cwd / 'banner.js'
        dark_css = cwd / 'dark_rtd.css'
        os.makedirs(staticdir, exist_ok=True)
        staticdir = os.path.join(app.builder.outdir, '_static')
        copy_asset_file(str(banner_css), staticdir)
        copy_asset_file(str(banner_js), staticdir)
        copy_asset_file(str(dark_css), staticdir)


def insert_sidebar(app, pagename, templatename, context, doctree):
    if not app.config.enable_deepmodeling:
        return
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
            banner = render_banner(current_site=app.config.deepmodeling_current_site)
            if begin_body != -1:
                content = content[:begin_body] + comment_begin + \
                    banner + comment_end + content[begin_body:]
            return content

        render.__dict__.update(old_render.__dict__)
        render._deepmodeling_patched = True
        app.builder.templates.render = types.MethodType(render,
                                                        app.builder.templates)


def insert_icp(app, pagename, templatename, context, doctree):
    if not app.config.enable_deepmodeling:
        return
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
            footer = content.lower().rfind('</footer>')
            icp_footer = '<p><a href="https://beian.miit.gov.cn" target="_blank">%s</a></p>' % icp_no
            if footer != -1:
                content = content[:footer] + comment_begin + \
                    icp_footer + comment_end + content[footer:]
            return content

        render.__dict__.update(old_render.__dict__)
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

        render.__dict__.update(old_render.__dict__)
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


def enable_dark_mode(app, config):
    """Enable dark mode if the theme is sphinx_rtd_theme."""
    if config.html_theme == 'sphinx_rtd_theme':
        app.add_css_file('dark_rtd.css')


def setup(app: Sphinx) -> Dict[str, Any]:
    # enable deepmodeling sidebar and icp
    # if the repo is outside the deepmodeling, disable it
    app.add_config_value('enable_deepmodeling', True, 'html')
    app.add_config_value('deepmodeling_current_site', 'Docs', 'html')
    app.connect('builder-inited', copy_custom_files)
    app.connect('html-page-context', insert_sidebar)
    app.connect('html-page-context', insert_icp)
    app.connect('html-page-context', minify_html_files)
    app.connect('build-finished', minify_js_files)
    app.connect('build-finished', minify_css_files)
    # dark mode for rtd theme
    app.connect('config-inited', enable_dark_mode)    

    return {'parallel_read_safe': True}
