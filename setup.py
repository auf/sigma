import ez_setup

ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "sigma",
    version = "0.1",
    packages = find_packages(),
    author = "",
    author_email = "",
    url = "",
    install_requires=[
        "Django",
        "Babel",
        "BeautifulSoup",
    ],
    include_package_data = True,
)

