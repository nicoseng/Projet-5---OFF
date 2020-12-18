
"""This file contains all the elements to select

and display the different tables for the user.

"""
class DbDisplay:
    """To display the tables for the user."""

    def __init__(self, db_connector):
        """ To connect to the database.

        Parameter
        ---------
        db_connector : cf.db_connector.py

        """
        self.db_connector = db_connector

    def select_category_table(self):
        """To fetch the category table"""
        self.db_connector.cursor.execute("SELECT * FROM category")
        category_table_fetched = self.db_connector.cursor.fetchall()
        return category_table_fetched

    def select_product_table(self):
        """To fetch the product table"""
        self.db_connector.cursor.execute("SELECT * FROM product")
        product_table_fetched = self.db_connector.cursor.fetchall()
        return product_table_fetched

    def select_store_table(self):
        """To fetch the store table"""
        self.db_connector.cursor.execute("SELECT * FROM store")
        store_table_fetched = self.db_connector.cursor.fetchall()
        return store_table_fetched

    def select_substitute_table(self):
        """Checks if there is not the same product in the table."""
        self.db_connector.cursor.execute(
            "SELECT * FROM product_has_substitute")
        product_has_substitute_table_fetched = \
            self.db_connector.cursor.fetchall()
        self.db_connector.connection.commit()
        return product_has_substitute_table_fetched

    def display_product_by_category_and_store(self, category_number):
        """Display the table called

        display_product_by_category_and_store for the user.

        Parameter
        ---------
        category_number : type int
            the number(id) of the category.

        Returns product datas with his category and his store.

        """
        self.db_connector.cursor.execute(
            "SELECT *\
            FROM product\
            INNER JOIN product_has_category\
            ON id_product = product_has_category.product_id_product\
            INNER JOIN product_has_store\
            ON id_product = product_has_store.product_id_product\
            INNER JOIN store\
            ON product_has_store.store_id_store = store.id_store\
            WHERE category_id_category = (%s)", (category_number,))

        product_by_category_and_store = self.db_connector.cursor.fetchall()
        self.db_connector.connection.commit()
        return product_by_category_and_store

    def display_product_selected(self, product_number):
        """Display the table called

        display_product_selected for the user.

        Parameter
        ---------
        product_number : type int
            the number(id) of the category.

        Returns product datas with his category and his store.

        """
        self.db_connector.cursor.execute(
            "SELECT *\
            FROM product\
            INNER JOIN product_has_category\
            ON id_product = product_has_category.product_id_product\
            INNER JOIN product_has_store\
            ON id_product = product_has_store.product_id_product\
            INNER JOIN store\
            ON product_has_store.store_id_store = store.id_store\
            WHERE id_product = (%s)", (product_number,))

        product_list_selected = self.db_connector.cursor.fetchall()
        self.db_connector.connection.commit()
        return product_list_selected

    def display_substitute_basket(self):
        """Display the substitute table saved by the user.

        Returns the list of substitute

        in the table product_has_substitute.
        """
        self.db_connector.cursor.execute("SELECT * FROM product_has_substitute\
            INNER JOIN product\
            ON product_id_substitute = product.id_product\
            INNER JOIN product_has_store\
            ON id_product = product_has_store.product_id_product\
            INNER JOIN store\
            ON product_has_store.store_id_store = store.id_store")

        substitute_list_in_table = self.db_connector.cursor.fetchall()
        self.db_connector.connection.commit()
        return substitute_list_in_table

    def delete_susbstitute_basket(self):
        """To empty the substitute table."""
        self.db_connector.cursor.execute("DELETE FROM product_has_substitute")
        self.db_connector.connection.commit()
