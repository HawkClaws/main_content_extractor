from setuptools import setup, find_packages

setup(
    name="MainContentExtractor",
    version="0.0.1",
    author="HawkClaws",
    packages=find_packages(),
    install_requires=["trafilatura","html2text"],
    include_package_data=True,
    url=""
)
