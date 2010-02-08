from setuptools import setup, find_packages

import sys, os

version = '1.0'

setup(
    name='sigma.references',
    version=version,
    description="",
    long_description="""\
""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Davin Baragiotta',
    author_email='davin.baragiotta@auf.org',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        ],
    entry_points={'django.apps': 'sigma.references = sigma.references'},
)
