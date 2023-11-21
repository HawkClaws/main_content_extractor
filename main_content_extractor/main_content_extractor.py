import re
import xml.etree.ElementTree as ET
import trafilatura
import html2text
from bs4 import BeautifulSoup


class MainContentExtractor:
    @staticmethod
    def extract(filecontent: str, output_format="html", **kwargs) -> str:
        data = trafilatura.extract(filecontent, output_format="xml", **kwargs)
        if data == None:
            return None
        data = MainContentExtractor._replace_tags(data)
        data = MainContentExtractor._convert_xml_to_html(data)
        data = MainContentExtractor._prettify_html(data)
        if output_format == "html":
            return data
        elif output_format == "markdown":
            return MainContentExtractor._html_to_markdown(data)

    @staticmethod
    def _html_to_markdown(html_string: str) -> str:
        h = html2text.HTML2Text()
        h.body_width = 0

        markdown_text = h.handle(html_string)
        return markdown_text

    @staticmethod
    def _prettify_html(html_string: str) -> str:
        soup = BeautifulSoup(html_string, "html.parser")
        return soup.prettify()

    @staticmethod
    def _replace_function(match) -> str:
        # dd-1 などの-1を取り除く
        rend_value = match.group(1)
        if "-" in rend_value:
            rend_value = rend_value.split("-")[0]
        return f"<{rend_value}>{match.group(2)}</{rend_value}>"

    @staticmethod
    def _replace_tags(input_string: str):
        patterns = [
            (r'<list rend="([^"]*)">([\s\S]*?)</list>', r"<\1>\2</\1>"),
            (
                r'<item rend="([^"]+)">([\s\S]*?)</item>',
                MainContentExtractor._replace_function,
            ),
            (r"<item>([\s\S]*?)</item>", r"<li>\1</li>"),
            (r"<lb\s*/>", "<br />"),
            (r'<head rend="([^"]+)">([\s\S]*?)</head>', r"<\1>\2</\1>"),
            (r"<row.*?>([\s\S]*?)</row>", r"<tr>\1</tr>"),
            (r'<cell role="head">([\s\S]*?)</cell>', r"<th>\1</th>"),
            (r"<cell>([\s\S]*?)</cell>", r"<td>\1</td>"),
            (r"<graphic (.*?)>", lambda match: f"<img {match.group(1)}>"),
            (r'<ref target="([\s\S]*?)">([\s\S]*?)</ref>', r'<a href="\1">\2</a>'),
            (r"<main>([\s\S]*?)</main>", r"\1"),
            (r"<main\s*/>", ""),
            (r"<comments>([\s\S]*?)</comments>", r"\1"),
            (r"<comments\s*/>", ""),
        ]

        for pattern, replacement in patterns:
            input_string = re.sub(pattern, replacement, input_string)

        return input_string

    @staticmethod
    def _convert_xml_to_html(xml_string: str) -> str:
        # 解析してHTMLに変換
        root = ET.fromstring(xml_string)
        title = root.get("title") or ""
        author = root.get("author") or ""
        date = root.get("date") or ""
        url = root.get("url") or ""
        description = root.get("description") or ""
        categories = root.get("categories") or ""
        tags = root.get("tags") or ""
        fingerprint = root.get("fingerprint") or ""

        # コンテンツを取得
        content = "".join(ET.tostring(child, encoding="unicode") for child in root)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {''.join(f'<meta name="{key}" content="{value}">' for key, value in [
                ("title", title),
                ("author", author),
                ("date", date),
                ("url", url),
                ("description", description),
                ("categories", categories),
                ("tags", tags),
                ("fingerprint", fingerprint)
            ] if value)}
            <title>{title}</title>
        </head>
        <body>
            {content}
        </body>
        </html>
        """

        return html_content
