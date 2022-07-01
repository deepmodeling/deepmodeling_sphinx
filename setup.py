from setuptools import setup

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
)
