"""Internal imports"""

import category_extractor
import product_extractor


class DbFiller:
    """To fill the tables in the database."""

    def __init__(self, db_connector):
        """
        To connect to the database so as to fill it.

        Parameters
        ----------
        db_connector : cf. db_connector.py

        """
        self.db_connector = db_connector

    def fill_category_table(self):
        """To fill the table category"""
        categories_extracted = category_extractor.CategoriesExtractor()
        categories_extracted_list = \
            categories_extracted.extract_categories_datas()

        for category in categories_extracted_list:
            self.db_connector.cursor.execute("INSERT INTO category\
                (category_name)\
                VALUES (%s)", (category["category_name"],))

        self.db_connector.cursor.execute("SELECT * FROM category")
        filled_category_table_fetched = self.db_connector.cursor.fetchall()
        self.db_connector.connection.commit()
        return filled_category_table_fetched

    def fill_product_table(self):
        """To fill the table product."""
        # We fetch the name of each category with their id
        self.db_connector.cursor.execute("SELECT * FROM category")
        category_data_in_table = self.db_connector.cursor.fetchall()

        whole_products_list = []
        for category in category_data_in_table:

            products_extracted = product_extractor.ProductExtractor()
            new_category_url = \
                products_extracted.get_new_category_url(
                    10, category["category_name"])
            one_category_products_list = \
                products_extracted.extract_products_datas(
                    category["id_category"], new_category_url, 0, 10)

            for pack in one_category_products_list:

                whole_products_list.append(pack)

        for product in whole_products_list:

            self.db_connector.cursor.execute(
                "INSERT INTO product\
                (product_name,nutriscore,url)\
                VALUES (%s,%s,%s)",
                (product["product_name"],
                 product["nutriscore"],
                 product["url"]))
            id_product = self.db_connector.cursor.lastrowid

            self.fill_product_has_category_table(
                id_product, product["id_category"])

            id_store = self.add_or_get_store(product["stores"])

            self.fill_product_has_store_table(id_store, id_product)

        self.db_connector.connection.commit()
        return whole_products_list

    def add_or_get_store(self, stores):

        """Insert the name of a store of a product

        in the table store.

        Parameters
        ----------
        stores : type str
            The name of the stores we fetch.

        Returns the number(id) of the store.

        """

        stores_splitted = stores.split(",")
        first_store = stores_splitted[0]

        if first_store == "":

            return 1

        self.db_connector.cursor.execute(
            "SELECT id_store \
            FROM store \
            WHERE store_name = (%s)",
            (first_store,))
        store_result = self.db_connector.cursor.fetchone()

        if store_result is None:

            self.db_connector.cursor.execute(
                "INSERT INTO store\
                (store_name)\
                VALUES (%s)", (first_store,))
            self.db_connector.connection.commit()

            store_row = self.db_connector.cursor.lastrowid
            return store_row

        return store_result["id_store"]

    def fill_product_has_category_table(self, id_product, id_category):

        """Inserts the id matching between

        a product and his category in product_has_category_table.

        Parameters
        ----------
        id_product : type int
            The number(id) of the product.
        id_category : type int
            The number(id) of the category of the product.

        """

        self.db_connector.cursor.execute("INSERT INTO product_has_category\
           (product_id_product, category_id_category)\
            VALUES (%s,%s)", (id_product, id_category))
        self.db_connector.connection.commit()

    def fill_product_has_store_table(self, id_store, id_product):

        """Insert the id matching between

        a product and his store in product_has_store_table.

        Parameters
        ----------
        id_store : type int
            The number(id) of the store.
        id_product : type int
            The number(id) of the product.

        """

        self.db_connector.cursor.execute("INSERT INTO product_has_store\
           (store_id_store,product_id_product)\
            VALUES (%s,%s)", (id_store, id_product))
        self.db_connector.connection.commit()

    def check_substitute(self, id_substitute):

        """Checks if a substitute already exists or not.

        Parameters
        ----------
        id_substitute : type int
            The number(id) of the substitute.

        Returns the number(id) of the substitute.

        """
        self.db_connector.cursor.execute(
            "SELECT product_id_substitute \
            FROM product_has_substitute \
            WHERE product_id_substitute = (%s)",
            (id_substitute,))

        substitute_result = self.db_connector.cursor.fetchone()
        return substitute_result

    def add_or_get_substitute(self, id_product, id_substitute):
        """ Inserts a substitute in product_has_substitute table.

        Parameters
        ----------
        id_product : type int
            The number(id) of the product.
        id_substitute : type int
            The number(id) of the substitute.

        """
        self.db_connector.cursor.execute("INSERT INTO product_has_substitute\
       (product_id_product,product_id_substitute)\
        VALUES (%s,%s)", (id_product, id_substitute))
        self.db_connector.connection.commit()
