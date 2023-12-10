# main_content_extractor

## Description

This library is designed for extracting only the main content from HTML.<br>
It was developed for obtaining information related to LLM and for data input to LangChain and LlamaIndex.<br>
<br>
Since this library contains element information and hierarchy information of HTML, it is useful when utilizing them.<br>
For example, it can be helpful in obtaining a list of links or headers from the main content.<br>
<br>
While `trafilatura` is an excellent library for main content extraction, it has issues such as missing necessary data or inability to output HTML.<br>
To address these problems, this library exists.<br>
<br>
The sequence of main content extraction is as follows:<br>
<br>
![image](https://raw.githubusercontent.com/HawkClaws/main_content_extractor/main/content_extraction_sequence.png)
<br>
In addition to HTML format, output in Text format and Markdown format is also supported. This is to make it easier to output data in a format that is more convenient for LLM.<br>
<br>
The extraction of main content uses `trafilatura`.<br>
Since `trafilatura` cannot output in HTML format, it is output in XML format containing HTML information and then converted to HTML.<br>
The conversion from XML to HTML is irreversible and does not perfectly match the original data.<br>
<br>

## Installation

`pip install MainContentExtractor`

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
extracted_markdown = MainContentExtractor.extract(content, output_format="markdown")
```