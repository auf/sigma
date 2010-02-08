from setuptools import setup, find_packages

import sys, os

version = '1.0'

setup(
    name='sigma.wcs',
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
    namespace_packages=['sigma', 'sigma.wcs'], 
    include_package_data=True,
    zip_safe=False,
    install_requires=['django'],
    entry_points={'django.apps': 'sigma.wcs = sigma.wcs'},
)
