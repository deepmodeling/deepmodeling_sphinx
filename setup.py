from setuptools import setup
from pathlib import Path

readme_file = Path(__file__).parent / "README.md"
readme = readme_file.read_text(encoding="utf-8")

setup(
    name="deepmodeling_sphinx",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=['deepmodeling_sphinx'],
    install_requires=[
        'sphinx',
        'htmlmin',
        'jsmin',
        'cssmin',
        'jinja2',
    ],
    package_data={
        'deepmodeling_sphinx': ['banner.html',
                                'banner.css',
                                'banner.js',
                                ],
    },
    long_description=readme,
    long_description_content_type="text/markdown",
)
