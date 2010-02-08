from setuptools import setup, find_packages

import sys, os

version = '1.0'

setup(
    name='sigma.www',
    version=version,
    description="",
    long_description="""\
""",
    classifiers=[],
    keywords='',
    author='Mathieu Leduc-Hamel',
    author_email='mathieu.leduc-hamel@savoirfairelinux.com',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['sigma', 'sigma.www'], 
    include_package_data=True,
    zip_safe=False,
    install_requires=['sigma.references', 'sigma.wcs'],
    entry_points={'django.apps': 'sigma.www = sigma.www'},
)
