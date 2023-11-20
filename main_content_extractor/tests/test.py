

import unittest

# テスト対象の関数やクラスなどを記述するファイルをインポート
from main_content_extractor import MainContentExtractor


class TestMainContentExtractor(unittest.TestCase):
    def test_extract_html(self):
        html = MainContentExtractor.extract(INPUT_TESTDATA)
        self.maxDiff = None
        self.assertEqual(html, EXPECTED1)

    def test_extract_markdown(self):
        markdown = MainContentExtractor.extract(INPUT_TESTDATA,output_format="markdown")
        self.maxDiff = None
        self.assertEqual(markdown, EXPECTED2)

    def test_extract_html_options(self):
        html = MainContentExtractor.extract(INPUT_TESTDATA, include_images=True, include_links=True)
        self.maxDiff = None
        self.assertEqual(html, EXPECTED3)

INPUT_TESTDATA = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WordPress記事のサンプル</title>
</head>
<body>

    <header>
        <h1>WordPress記事のサンプル</h1>
    </header>

    <article>
        <h2>記事のタイトル</h2>
        <p>これはWordPressの記事のサンプルです。ここに記事の本文が表示されます。</p>

        <ul>
            <li>リストアイテム1</li>
            <li>リストアイテム2</li>
            <li>リストアイテム3</li>
        </ul>

        <p>画像の挿入も可能です。</p>
        <img src="https://example.com/wp-content/uploads/2023/01/sample-image.jpg" alt="サンプル画像">

        <p>引用も挿入できます。</p>
        <blockquote>
            これは引用の例です。引用文がここに表示されます。
        </blockquote>

        <p>カテゴリやタグなどのメタ情報も含めて記事を充実させることができます。</p>
        <a href="https://example.com/page1">ページ１</a>
        <footer>
            <p>投稿日: 2023年1月1日</p>
            <p>カテゴリ: <a href="https://example.com/category">カテゴリ名</a></p>
            <p>タグ: <a href="https://example.com/tag">タグ1</a>, <a href="#">タグ2</a></p>
        </footer>
    </article>

    <footer>
        <p>&copy; 2023 WordPressのサンプルサイト</p>
    </footer>

</body>
</html>

"""

EXPECTED1 = """<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <meta content="WordPress記事のサンプル" name="title"/>
  <meta content="2023-01-01" name="date"/>
  <meta content="2e4dd90dab2076aa" name="fingerprint"/>
  <title>
   WordPress記事のサンプル
  </title>
 </head>
 <body>
  <h2>
   記事のタイトル
  </h2>
  <p>
   これはWordPressの記事のサンプルです。ここに記事の本文が表示されます。
  </p>
  <ul>
   <li>
    リストアイテム1
   </li>
   <li>
    リストアイテム2
   </li>
   <li>
    リストアイテム3
   </li>
  </ul>
  <p>
   画像の挿入も可能です。
  </p>
  <p>
   引用も挿入できます。
  </p>
  <quote>
   これは引用の例です。引用文がここに表示されます。
  </quote>
  <p>
   カテゴリやタグなどのメタ情報も含めて記事を充実させることができます。
  </p>
  ページ１
  <p>
   これはWordPressの記事のサンプルです。ここに記事の本文が表示されます。
  </p>
  <p>
   画像の挿入も可能です。
  </p>
  <p>
   引用も挿入できます。
  </p>
  <quote>
   これは引用の例です。引用文がここに表示されます。
  </quote>
  <p>
   カテゴリやタグなどのメタ情報も含めて記事を充実させることができます。
  </p>
  ページ１
 </body>
</html>
"""


EXPECTED2 = """##  記事のタイトル 

これはWordPressの記事のサンプルです。ここに記事の本文が表示されます。 

  * リストアイテム1 
  * リストアイテム2 
  * リストアイテム3 



画像の挿入も可能です。 

引用も挿入できます。 

これは引用の例です。引用文がここに表示されます。 

カテゴリやタグなどのメタ情報も含めて記事を充実させることができます。 

ページ１ 

これはWordPressの記事のサンプルです。ここに記事の本文が表示されます。 

画像の挿入も可能です。 

引用も挿入できます。 

これは引用の例です。引用文がここに表示されます。 

カテゴリやタグなどのメタ情報も含めて記事を充実させることができます。 

ページ１ 
"""

EXPECTED3 ="""<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <meta content="WordPress記事のサンプル" name="title"/>
  <meta content="2023-01-01" name="date"/>
  <meta content="3e6fd92ffbe277ba" name="fingerprint"/>
  <title>
   WordPress記事のサンプル
  </title>
 </head>
 <body>
  <h2>
   記事のタイトル
  </h2>
  <p>
   これはWordPressの記事のサンプルです。ここに記事の本文が表示されます。
  </p>
  <ul>
   <li>
    リストアイテム1
   </li>
   <li>
    リストアイテム2
   </li>
   <li>
    リストアイテム3
   </li>
  </ul>
  <p>
   画像の挿入も可能です。
  </p>
  <img alt="サンプル画像" src="https://example.com/wp-content/uploads/2023/01/sample-image.jpg"/>
  <p>
   引用も挿入できます。
  </p>
  <quote>
   これは引用の例です。引用文がここに表示されます。
  </quote>
  <p>
   カテゴリやタグなどのメタ情報も含めて記事を充実させることができます。
  </p>
  <p>
   <a href="https://example.com/page1">
    ページ１
   </a>
  </p>
  <p>
   これはWordPressの記事のサンプルです。ここに記事の本文が表示されます。
  </p>
  <p>
   画像の挿入も可能です。
  </p>
  <p>
   引用も挿入できます。
  </p>
  <quote>
   これは引用の例です。引用文がここに表示されます。
  </quote>
  <p>
   カテゴリやタグなどのメタ情報も含めて記事を充実させることができます。
  </p>
 </body>
</html>
"""

if __name__ == "__main__":
    unittest.main()
