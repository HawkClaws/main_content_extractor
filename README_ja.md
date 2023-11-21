# main_content_extractor

最新情報は英語の[README.md](README.md)です。

## Description

このライブラリは、HTMLからメインコンテンツのみを抽出するためのものです。<br>
LLMに関する情報や、LangChainやLlamaIndexへのデータ投入用に開発しました。<br>
<br>
メインコンテンツの抽出には`trafilatura`が使用されています。<br>
`trafilatura`ではHTML形式での出力ができないため、HTML情報が含まれたXML形式で出力され、その後HTMLに変換されています。<br>
XMLからHTMLへの変換は不可逆的なものであり、完全に元のデータと一致するわけではありません。<br>
<br>
本ライブラリはHTMLの要素情報や階層情報が含まれているため、これらを利用する際に有用です。<br>
例えば、メインコンテンツのリンク一覧や見出しを取得する際に役立ちます。<br>
<br>
また、Markdown形式での出力もサポートしています。これは、よりLLMで扱いやすい形式でデータを出力できるようにするためのものです。

## Installration

`pip install git+https://github.com/HawkClaws/main_content_extractor.git`

## HowToUse

```python

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

extractの引数である`**kwargs`は、直接`trafilatura`の`extract`に渡されます。<br>
そのため、`trafilatura`の`extract`で使用可能な引数はすべて利用できます。<br>
具体的な引数については[trafilatura-doc](https://trafilatura.readthedocs.io/en/latest/corefunctions.html#extraction)を参照してください。<br>
<br>
extractの引数の`**kwargs`は直接`trafilatura`の`extract`に渡されます。<br>
ただし、`trafilatura`の`extract`の引数である`output_format`は`xml`に固定されていますので、これを`trafilatura`の引数として渡すことはできません。