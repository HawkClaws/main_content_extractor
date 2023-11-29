import re
import xml.etree.ElementTree as ET
import trafilatura

class TrafilaturaExtends:

    @staticmethod
    def extract(
        html: str,
    ) -> str:
        """
        Extracts content from HTML using Trafilatura library.
        Args:
            html: The HTML string to extract content from.
        Returns:
            The extracted content as a string.
        """
        data = trafilatura.extract(
            html,
            output_format="xml",
            include_tables=True,
            include_images=True,
            include_links=True,
        )

        if data == None:
            return None
        data = TrafilaturaExtends._replace_tags(data)
        data = TrafilaturaExtends._convert_xml_to_html(data)
        return data

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
                TrafilaturaExtends._replace_function,
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
