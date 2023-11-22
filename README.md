# main_content_extractor

## Description

This library is designed to extract only the main content from HTML.<br>
Developed for information on LLM and for feeding data into LangChain and LlamaIndex.<br>
<br>
The `trafilatura` is used to extract the main content.<br>
Since `trafilatura` does not allow output in HTML format, the output is in XML format with HTML information and then converted to HTML.<br>
The XML to HTML conversion is irreversible and does not completely match the original data.<br>
<br>
This library contains HTML element and hierarchical information, which is useful when using these elements.<br>
For example, it is useful to get a list of links or headings for the main content.<br>
<br>
It also supports output in Markdown format. This is intended to allow data to be output in a format more easily handled by LLM.

## Installration

`pip install git+https://github.com/HawkClaws/main_content_extractor.git`

## HowToUse

```python
import requests
from main_content_extractor import MainContentExtractor

# Get HTML using requests
url = "https://developer.mozilla.org/ja/docs/Web"
response = requests.get(url)
response.encoding = 'utf-8'
content = response.text

# Get HTML with main content extracted from HTML
extracted_html = MainContentExtractor.extract(content)

# Get HTML with main content extracted from Markdown
extracted_markdown = MainContentExtractor.extract(content,output_format="markdown")

# Get HTML with main content extracted from HTML 
# (using trafilatura arguments include_images and include_links)
extracted_html = MainContentExtractor.extract(INPUT_TESTDATA, include_images=True, include_links=True)

```

The `**kwargs` argument of `extract` is passed directly to `extract` in `trafilatura`.<br>
Therefore, all available arguments for `extract` in `trafilatura` are available.<br>
See [trafilatura-doc](https://trafilatura.readthedocs.io/en/latest/corefunctions.html#extraction) for specific arguments.<br>
<br>
However, `trafilatura`'s `extract` argument, `output_format`, is fixed to `xml` and cannot be passed as an argument to `trafilatura`.