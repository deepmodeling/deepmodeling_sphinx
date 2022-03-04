from setuptools import setup

setup(
    name="deepmodeling_sphinx",
    version="0.0.3",
    packages=['deepmodeling_sphinx'],
    install_require=['sphinx'],
    package_data={
        'deepmodeling_sphinx': ['banner.html',
                                'banner.css',
                                'banner.js',
                                ],
    },
)
