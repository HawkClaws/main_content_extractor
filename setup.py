from setuptools import setup, find_packages

with open("README.md", "r") as fp:
    readme = fp.read()

DESCRIPTION = "A library to extract the main content from html. Developed for information on LLM and for feeding data into LangChain and LlamaIndex."

setup(
    name="MainContentExtractor",
    version="0.0.4",
    author="HawkClaws",
    packages=find_packages(),
    install_requires=[
        "trafilatura>=1.6.2",
        "html2text>=2020.1.16",
        "beautifulsoup4>=4.12.2",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    url="https://github.com/HawkClaws/main_content_extractor",
    project_urls={"Source Code": "https://github.com/HawkClaws/main_content_extractor"},
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type='text/markdown',
    license="MIT",
)
