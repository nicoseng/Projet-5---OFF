"""This file contains elements for connecting to mysql."""

import config
import mysql.connector



class DbConnector:

    """To manipulate the database."""

    def __init__(self):

        """To connect to the database."""

        self.connection = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD)

        # To "open" the access
        self.cursor = self.connection.cursor(
            buffered=True, dictionary=True)
