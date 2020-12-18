"""Internal imports"""

import requests


class CategoriesLoader:
    """
    Loads categories of products from the API OpenFoodFacts(OFF).

    """
    @staticmethod
    def load_categories(first_category_number, last_category_number, retry=3):
        """This function loads the categories datas

        from the URL address in OFF.

        Parameters
        ----------
        first_category_number : type int
            The number of the first category we want to load
        last_category_number : type int
            The number of the last category we want to load
        retry : type int
            The number of attempts if there are errors.

        """
        categories_loaded_list = []

        try:

            categories_url = "https://fr.openfoodfacts.org/categories&json=1"
            request = requests.get(categories_url)

            # To get the json format
            categories_url_json = request.json()
            categories_loaded_list = categories_url_json["tags"][
                first_category_number:last_category_number]

        except requests.exceptions.RequestException:

            if retry > 0:
                return CategoriesLoader.load_categories(
                    first_category_number, last_category_number, retry - 1)

        return categories_loaded_list
