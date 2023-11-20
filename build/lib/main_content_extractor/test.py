from main_content_extractor import MainContentExtractor
import requests

url = "https://www.freecodecamp.org/japanese/news/html-tables-table-tutorial-with-css-example-code/"
# url = "https://nanson3.com/washing-carp/"
# url = "https://sorae.info/astronomy/20220111-j1533-2727.html"

# url = "https://www.freecodecamp.org/japanese/news/html-tables-table-tutorial-with-css-example-code/"
# url = "https://nanson3.com/washing-carp/"
url = "https://sorae.info/astronomy/20220111-j1533-2727.html"

response = requests.get(url, headers=None)
response.encoding = "utf-8"
data = MainContentExtractor.extract(
    response.text, output_format="markdown", include_images=True, include_links=True
)

with open("trafilatura_raw.html", "w", encoding="utf-8") as file:
    # ファイルにデータを書き込む
    file.write(response.text)


print(data)
with open("trafilatura.html", "w", encoding="utf-8") as file:
    # ファイルにデータを書き込む
    file.write(data)


# with open("trafilatura.md", "w", encoding="utf-8") as file:
#     # ファイルにデータを書き込む
#     file.write(markdown)
