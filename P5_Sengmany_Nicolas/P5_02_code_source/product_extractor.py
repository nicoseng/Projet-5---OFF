"""Internal imports"""

import requests


class ProductExtractor:

    """

    To extract the product datas for each category

    from the file called category_extractor.py

    """

    @staticmethod
    def get_new_category_url(page_size, category_name, retry=3):

        """

        To return URL of each category

        with the number of products we want to extract.

        Parameters
        ----------
        page_size : type int
            The number of product we want to extract for each category.
        category_name: type str
            The name of each category.
        retry : type int
            The number of attempts if there are errors.

        """
        try:
            category_url = "https://fr.openfoodfacts.org/categorie/" +\
                str(category_name)
            param = {"page_size": page_size, "json": "1"}
            new_category_link = requests.get(category_url, params=param)

        except requests.exceptions.RequestException:

            if retry > 0:
                return ProductExtractor.get_new_category_url(
                    page_size, category_name, retry - 1)

        return new_category_link.url

    @staticmethod
    def extract_products_datas(id_category, category_url,
                               start_product_nb, last_product_nb):

        """To extract the product data from each category.

        Parameters
        ----------

        id_category : type int
            The number(id) of the category of the product.
        category_url : type str
            The URL link of the category.
        start_product_nb and last_product_nb : 
            Indicate the numbers of position of the products in the category
        start_product_nb : type int
            The first number of the interval.
        last_product_nb : type int
            The last number of the interval.

        """

        products_list = []

        while start_product_nb <= last_product_nb:

            try:
                product_page_url = requests.get(category_url)
                product_page_json = product_page_url.json()

                product_dict = {"id_category": id_category,
                                "product_name": "", "nutriscore": "",
                                "stores": "", "url": ""}

                product_name = product_page_json["products"][
                    start_product_nb]["product_name"]
                product_dict["product_name"] = product_name

                nutriscore = product_page_json["products"][
                    start_product_nb]["nutrition_grades"]
                product_dict["nutriscore"] = nutriscore

                stores = product_page_json["products"][
                    start_product_nb]["stores"]
                product_dict["stores"] = stores

                url = product_page_json["products"][start_product_nb]["url"]
                product_dict["url"] = url

                products_list.append(product_dict)

            # To avoid empty field from OpenFoodFacts
            except KeyError:
                pass
            except IndexError:
                pass

            start_product_nb += 1
        return products_list
