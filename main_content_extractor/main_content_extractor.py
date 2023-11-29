from bs4 import BeautifulSoup, Tag
from typing import List, Union
from html2text import html2text
from .trafilatura_extends import TrafilaturaExtends

REMOVE_ELEMENT_LIST_DEFAULT: List[str] = [
    "script",
    "style",
    "aside",
    "footer",
    "header",
    "hgroup",
    "nav",
    "search",
]


class MainContentExtractor:
    def extract(
        html: str,
        output_format: str = "html",
        include_links: bool = True,
        ref_extraction_method: dict = {},
    ) -> str:
        """
        Extracts the main content from an HTML string.

        Args:
            html: The HTML string to extract the main content from.
            output_format: The format of the extracted content (html, text, markdown).
            include_links: Whether to include links in the extracted content.
            ref_extraction_method: A dictionary to store the reference to the extraction method.
            
        Returns:
            The extracted main content as a string.
        """
        valid_formats = ["html", "text", "markdown"]
        
        if output_format not in valid_formats:
            raise ValueError(f"Invalid output_format: {output_format}. Valid formats are: {', '.join(valid_formats)}.")
    
        soup = BeautifulSoup(html, "html.parser")
        soup = MainContentExtractor._remove_elements(soup, REMOVE_ELEMENT_LIST_DEFAULT)

        main_content = soup.find("main")

        result_html = None
        extraction_method = None

        if main_content:
            extraction_method = "main_element"
            articles = main_content.find_all("article")

            if articles:
                result_html = "".join(str(article) for article in articles)
            else:
                result_html = str(main_content)
        else:
            extraction_method = "article_element"
            articles = soup.find_all("article")

            if articles:
                result_html = "".join(str(article) for article in articles)
            else:
                main_content = MainContentExtractor._get_deepest_element_data(
                    soup, ["contents", "main"]
                )
                if main_content:
                    extraction_method = "deepest_element_data"
                    result_html = str(main_content)
                else:
                    extraction_method = "trafilatura_extract"
                    result_html = TrafilaturaExtends.extract(str(soup))

        if result_html:
            soup = BeautifulSoup(result_html, "html.parser")

            if ref_extraction_method is not None:
                ref_extraction_method["extraction_method"] = extraction_method

            if output_format == "text":
                return soup.get_text(strip=True)
            
            if include_links == False:
                soup = MainContentExtractor._remove_elements_keep_text(soup, ["a","img"])
            if output_format == "html":
                return soup.prettify()
            elif output_format == "markdown":
                return html2text(str(soup))

    def extract_links(html_content: str, **kwargs) -> dict:
        """
        Extracts links from HTML content and returns a dictionary with link information.

        Args:
            html_content (str): The HTML content from which to extract links.

        Returns:
            dict: A dictionary containing link information with link URLs as keys and a dictionary
            with link text and URL as values.
        """
        extracted_html = MainContentExtractor.extract(html_content, **kwargs)
        soup = BeautifulSoup(extracted_html, "html.parser")

        links = {}
        for a_tag in soup.find_all("a"):
            link_text = a_tag.get_text(strip=True)
            if not link_text:
                continue
            link_url = a_tag.get("href")
            if not link_url:
                continue
            links[link_url] = {"text": link_text, "url": link_url}

        return links

    def extract_images(html_content: str, **kwargs) -> dict:
        """
        Extracts images from HTML content and returns a dictionary with image information.

        Args:
            html_content (str): The HTML content from which to extract images.

        Returns:
            dict: A dictionary containing image information with image URLs as keys and a dictionary
            with image alt text and URL as values.
        """
        extracted_html = MainContentExtractor.extract(html_content, **kwargs)
        soup = BeautifulSoup(extracted_html, "html.parser")

        images = {}
        for img_tag in soup.find_all("img"):
            image_alt = img_tag.get("alt", "")
            image_url = img_tag.get("src")
            images[image_url] = {"alt": image_alt, "url": image_url}

        return images

    def _remove_elements(soup: BeautifulSoup, elements: List[str]) -> BeautifulSoup:
        """
        Removes specified elements from a BeautifulSoup object.
        Args:
            soup (BeautifulSoup): The BeautifulSoup object to modify.
            elements (List[str]): The list of elements to remove.
        Returns:
            BeautifulSoup: The modified BeautifulSoup object.
        """

        def remove_element(element: Tag) -> None:
            if element.name in elements:
                element.decompose()

        for element in soup.find_all():
            remove_element(element)

        return soup

    def _remove_elements_keep_text(
        soup: BeautifulSoup, target_element_list: List[str]
    ) -> BeautifulSoup:
        for element in soup.find_all():
            if element.name in target_element_list:
                element.unwrap()
        return soup

    def _get_deepest_element_data(
        soup: BeautifulSoup, target_ids: List[str]
    ) -> Union[BeautifulSoup, None]:
        """
        Finds the deepest element in the given BeautifulSoup object with the specified target IDs.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML.
            target_ids (List[str]): The list of target IDs to search for.

        Returns:
            Union[BeautifulSoup, None]: The deepest element found, or None if no matching element is found.
        """
        deepest_element = None
        deepest_depth = 0

        def find_deepest_element(element: BeautifulSoup, current_depth: int) -> None:
            nonlocal deepest_element, deepest_depth

            if element.has_attr("id") and element["id"] in target_ids:
                if current_depth > deepest_depth:
                    deepest_element = element
                    deepest_depth = current_depth

            for child in element.children:
                if child.name is not None:
                    find_deepest_element(child, current_depth + 1)

        find_deepest_element(soup, 0)

        return deepest_element
