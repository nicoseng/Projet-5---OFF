"""This file contains the script used for creating a database."""
import config


class DbCreator:
    """This class creates all elements required for the database."""
    def __init__(self, db_connector):
        """To get elements required for creating the database."""
        self.db_connector = db_connector
        self.db_name = config.DB_NAME

        """
        To define the name of the user.

        At the begnining, the user database does not have name yet :

        - Look at the file named config.py ;
        - For the constant named DB_NAME, type a name for your own database.

        Parameter
        ---------
        db_connector : cf.db_connector.py

        """
    def create_db(self):
        """Creates the general structure of the database."""
        self.db_connector.cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {}".format(self.db_name))

    def select_db(self):
        """To select the database created."""
        self.db_connector.cursor.execute("USE {}".format(self.db_name))

    def create_category_table(self):
        """Creates the table category.

        Returns the table of the product filled.

        """
        self.db_connector.cursor.execute("CREATE TABLE IF NOT EXISTS category(\
            id_category INT NOT NULL AUTO_INCREMENT,\
            category_name VARCHAR(100) NOT NULL,\
            PRIMARY KEY (id_category))\
            ENGINE = INNODB")

        self.db_connector.cursor.execute("SELECT * FROM category")
        category_table_selected = self.db_connector.cursor.fetchall()
        return category_table_selected

    def create_product_table(self):
        """Creates the table product.

        Selects the table newly created.

        """
        self.db_connector.cursor.execute("CREATE TABLE IF NOT EXISTS product\
            (id_product INT NOT NULL AUTO_INCREMENT,\
            product_name VARCHAR(500) NOT NULL,\
            nutriscore VARCHAR(50),\
            url VARCHAR(500),\
            PRIMARY KEY (id_product))\
            ENGINE = INNODB")

        self.db_connector.cursor.execute("SELECT * FROM product")
        product_table_selected = self.db_connector.cursor.fetchall()
        return product_table_selected

    def create_store_table(self):
        """ Creates the table store.

        Selects the table of the store newly created.

        """
        self.db_connector.cursor.execute("CREATE TABLE IF NOT EXISTS store \
            (id_store INT NOT NULL AUTO_INCREMENT,\
            store_name VARCHAR(50) NOT NULL,\
            PRIMARY KEY (id_store))\
            ENGINE = INNODB")

        self.db_connector.cursor.execute("SELECT * FROM store")
        store_table_selected = self.db_connector.cursor.fetchall()

        if len(store_table_selected) == 0:

            self.db_connector.cursor.execute("INSERT INTO store\
            (store_name)\
            VALUES (%s)", ("Non renseigné", ))

        return store_table_selected

    def create_product_has_category_table(self):
        """Creates the table product has category."""
        self.db_connector.cursor.execute("CREATE TABLE IF NOT EXISTS product_has_category\
            (product_id_product INT NOT NULL,\
            category_id_category INT NOT NULL,\
            PRIMARY KEY (product_id_product, category_id_category),\
            INDEX fk_product_has_category_category_idx \
            (category_id_category ASC),\
            INDEX fk_product_has_category_product_idx \
            (product_id_product ASC),\
            CONSTRAINT fk_product_has_category_product\
            FOREIGN KEY (product_id_product)\
            REFERENCES product (id_product)\
            ON DELETE NO ACTION \
            ON UPDATE NO ACTION,\
            CONSTRAINT fk_product_has_category_category\
            FOREIGN KEY (category_id_category)\
            REFERENCES category (id_category)\
            ON DELETE NO ACTION\
            ON UPDATE NO ACTION)\
            ENGINE = INNODB")

    def create_product_has_store_table(self):
        """Creates the table product_has_shop."""
        self.db_connector.cursor.execute("CREATE TABLE IF NOT EXISTS product_has_store(\
            product_id_product INT NOT NULL,\
            store_id_store INT NOT NULL,\
            PRIMARY KEY (product_id_product, store_id_store),\
            INDEX fk_product_has_store_store_idx (store_id_store ASC),\
            INDEX fk_product_has_store_product_idx (product_id_product ASC),\
            CONSTRAINT fk_product_has_store_product\
            FOREIGN KEY (product_id_product)\
            REFERENCES product (id_product)\
            ON DELETE NO ACTION\
            ON UPDATE NO ACTION,\
            CONSTRAINT fk_product_has_store_store\
            FOREIGN KEY (store_id_store)\
            REFERENCES store(id_store)\
            ON DELETE NO ACTION\
            ON UPDATE NO ACTION)\
            ENGINE = INNODB")

    def create_product_has_substitute_table(self):
        """Creates the table product has substitute.

        Selects the table of the product_has_substitute newly created.

        """
        self.db_connector.cursor.execute("CREATE TABLE IF NOT EXISTS product_has_substitute (\
            product_id_product INT NOT NULL,\
            product_id_substitute INT NOT NULL,\
            PRIMARY KEY (product_id_product, product_id_substitute),\
            INDEX fk_product_has_product_substitute_idx \
            (product_id_substitute ASC),\
            INDEX fk_product_has_product_product_idx \
            (product_id_product ASC),\
            CONSTRAINT fk_product_has_product_product\
            FOREIGN KEY (product_id_product)\
            REFERENCES product (id_product)\
            ON DELETE NO ACTION\
            ON UPDATE NO ACTION,\
            CONSTRAINT fk_product_has_product_substitute \
            FOREIGN KEY (product_id_substitute)\
            REFERENCES product (id_product)\
            ON DELETE NO ACTION\
            ON UPDATE NO ACTION)\
            ENGINE = INNODB")

        self.db_connector.cursor.execute(
            "SELECT * FROM product_has_substitute")
        substitute_table_selected = self.db_connector.cursor.fetchall()
        return substitute_table_selected
