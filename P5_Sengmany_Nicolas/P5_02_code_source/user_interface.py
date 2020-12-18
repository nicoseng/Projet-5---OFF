"""imports"""
import random
import sys
import db_connector
import db_creator
import db_display
import db_filler


class UserInterface:

    """This class aims to articulate all elements of the application."""

    def __init__(self):

        """To get the user interface."""

        # To get the connection
        self.db_connector = db_connector.DbConnector()

        # Creation of the database and tables we need
        self.load_db = db_creator.DbCreator(self.db_connector)
        self.load_db.create_db()
        self.load_db.select_db()

        category_table_selected = self.load_db.create_category_table()
        product_table_selected = self.load_db.create_product_table()

        self.load_db.create_store_table()
        self.load_db.create_product_has_category_table()
        self.load_db.create_product_has_store_table()

        self.load_db.create_product_has_substitute_table()

        if len(category_table_selected) == 0:

            self.fill_table = db_filler.DbFiller(self.db_connector)
            self.fill_table.fill_category_table()

        db_display_fetched = db_display.DbDisplay(self.db_connector)

        category_table_selected = db_display_fetched.select_category_table()

        if len(product_table_selected) == 0:

            self.fill_table = db_filler.DbFiller(self.db_connector)
            self.fill_table.fill_product_table()

        product_table_selected = db_display_fetched.select_product_table()

    @staticmethod
    def manage_welcome_menu():

        """Returns the name of the user."""

        while True:

            user_name = input("Veuillez saisir votre nom : ")

            if user_name.isalpha():

                #  We want the first letter in capital letter
                #  and other letters in small letters.
                user_name = user_name.capitalize()
                print("-----------------------------------")
                print("Bienvenue {} dans notre application Pur Beurre !".
                      format(user_name))
                print("-----------------------------------")
                return

            print("Ce nom est invalide."
                  "Veuillez recommencer votre saisie.")

    def manage_main_menu(self):

        """To invite the user to choose a menu"""

        user_input = True

        while user_input:

            menu_choice = \
                input("Quel aliment voulez-vous remplacer ?"
                      "Pour ce faire, tapez 1."
                      "\nPour retrouver vos aliments substitués enregistrés,"
                      "tapez 2."
                      "\nTapez ici le numéro de votre choix : \n")

            try:

                menu_choice = int(menu_choice)

                if menu_choice <= 0 or menu_choice > 2:
                    print("-----------------------------------")
                    print("Le numéro saisi ne convient pas."
                          "\nVeuillez recommencer votre saisie.")
                    print("-----------------------------------")

            except ValueError:

                print("-----------------------------------")
                print("Vous n'avez pas saisi un nombre."
                      "\nVeuillez recommencer votre saisie.")
                print("-----------------------------------")
                menu_choice = 0

            if menu_choice == 1:

                print("-----------------------------------")
                print("MENU CATEGORIES")
                print("-----------------------------------")

                print("VOICI LES CATEGORIES DISPONIBLES:")
                print("-----------------------------------")

                db_display_fetched = \
                    db_display.DbDisplay(self.db_connector)
                category_table_fetched = \
                    db_display_fetched.select_category_table()

                for category in category_table_fetched:

                    print(str(category["id_category"]) +
                          "." +
                          str(category["category_name"]))
                    print("-----------------------------------")

                self.manage_category_menu(category_table_fetched)

            if menu_choice == 2:

                self.manage_substitute_basket()

    def manage_substitute_basket(self):

        """Displays the list of substitute saved by the user."""

        db_display_fetched = db_display.DbDisplay(self.db_connector)
        substitute_list_in_table = db_display_fetched.display_substitute_basket()

        if len(substitute_list_in_table) == 0:

            print("Panier vide.\n")

            self.manage_main_menu()

        else:

            print("-----------------------------------")
            print("VOICI VOS ALIMENTS SUBSTITUES ENREGISTRES : ")
            print("-----------------------------------")

            for substitute in substitute_list_in_table:
                print("-----------------------------------")
                print("N° du produit : " +
                      str(substitute["product_id_substitute"]) +
                      "\n" +
                      "Nom : " +
                      str(substitute["product_name"]) +
                      "\n" +
                      "Nutriscore : " +
                      str(substitute["nutriscore"]) +
                      "\n" +
                      "Store : " +
                      str(substitute["store_name"]) +
                      "\n" +
                      "url: " +
                      str(substitute["url"]))
                print("-----------------------------------")

            user_input = True

            while user_input:

                delete_choice = \
                    input("Souhaitez-vous supprimer votre panier (O/N)?")

                if delete_choice == "o":

                    db_display_fetched = \
                        db_display.DbDisplay(self.db_connector)
                    db_display_fetched.delete_susbstitute_basket()
                    print("Votre panier a bien été vidé.")
                    self.manage_main_menu()

                elif delete_choice == "n":

                    self.manage_main_menu()

                else:
                    print("Nous n'avons pas compris votre choix."
                          "\nVeuillez recommencer votre saisie.")

    def manage_category_menu(self, category_table):

        """Returns the list of products according to the category selected.

        Parameter
        ---------
        category_table : type tuple
            The name of the category table.

        """

        #  At the beginning, we don't make choice yet.
        #  So we write category_number = 0
        category_number = 0

        # We choose to limit the categories until 10 categories max
        while category_number <= 0 \
                or category_number > len(category_table):

            category_number = \
                input("\nEntrez un chiffre associé à la catégorie souhaitée: ")

            try:
                category_number = int(category_number)
                if category_number <= 0 \
                        or category_number > len(category_table):

                    print("Le numéro saisi ne convient pas."
                          "\nVeuillez recommencer votre choix.")

            except ValueError:
                print("Vous n'avez pas saisi un nombre."
                      "\nVeuillez recommencer votre saisie.")
                category_number = 0
                continue

            if 0 <= category_number <= len(category_table):

                db_display_fetched = db_display.DbDisplay(self.db_connector)
                product_by_category_and_store = \
                    db_display_fetched.\
                    display_product_by_category_and_store(category_number)

                if len(product_by_category_and_store) == 0:
                    print("La categorie choisie est actuellement vide.")
                    self.manage_category_menu(category_table)

                else:

                    print("Vous avez choisi la catégorie numéro {}.\n".
                          format(category_number))
                    print("---------------------------------")
                    print("MENU PRODUITS")
                    print("---------------------------------")
                    print("Voici la liste des produits:")
                    print("---------------------------------")

                    for product in product_by_category_and_store:
                        print("N° du produit : " +
                              str(product["id_product"]) +
                              "\n" +
                              "Nom : " +
                              str(product["product_name"]) +
                              "\n" +
                              "Nutriscore : " +
                              str(product["nutriscore"]) +
                              "\n" +
                              "Store : " +
                              str(product["store_name"]) +
                              "\n" +
                              "url : " +
                              str(product["url"]))
                        print("---------------------------------")

        self.manage_product_choice_menu(product_by_category_and_store)

    def manage_product_choice_menu(self, product_table):

        """Returns the product selected by the user.

        Parameter
        ---------
        product_table : type tuple
            The name of the product table.

        """

        product_id_selected_list = []

        for product in product_table:
            id_product = product["id_product"]
            product_id_selected_list.append(id_product)

        product_number = 0

        while product_number not in product_id_selected_list:

            product_number = \
                input("\nVeuillez entrer le numéro du produit souhaitée :")

            try:
                product_number = int(product_number)

            except ValueError:
                print("Vous n'avez pas saisi un nombre."
                      "\nVeuillez recommencer votre saisie.")
                product_number = 0
                continue

            if product_number in product_id_selected_list:

                print("-------------------------------------------")
                print("VOUS AVEZ SELECTIONNE LE PRODUIT SUIVANT :")
                print("-------------------------------------------")

                db_display_fetched = db_display.DbDisplay(self.db_connector)
                product_list_selected = \
                    db_display_fetched.display_product_selected(product_number)

                for product in product_list_selected:

                    print("N° du produit : " +
                          str(product["id_product"]) +
                          "\n" +
                          "Nom : " +
                          str(product["product_name"]) +
                          "\n" +
                          "Nutriscore : " +
                          str(product["nutriscore"]) +
                          "\n" +
                          "Store : " +
                          str(product["store_name"]) +
                          "\n" +
                          "URL: " +
                          str(product["url"]))
                    print("---------------------------------")

            else:
                print("Le numéro de produit saisi"
                      " ne figure pas dans le tableau."
                      "\nVeuillez recommencer votre saisie.")

        self.manage_substitute_menu(product["id_product"],
                                    product_list_selected,
                                    product_table)

    def manage_substitute_menu(self,
                               produit_selected_id,
                               product_list_selected,
                               product_table):

        """Returns a product with a better nutriscore.

        Parameters
        ----------
        produit_selected_id : type int
            The number(id) of the product selected.
        product_list_selected : type list
            The list of the product selected bu the user.
        product_table : type tuple
            The table of all the products from the table called product.

        """

        available_nutriscore_list = ["a", "b", "c", "d", "e"]
        selected_product_nutriscore = product_list_selected[0]["nutriscore"]
        selected_nutriscore_index = \
            available_nutriscore_list.index(selected_product_nutriscore)

        best_nutriscore_list = \
            available_nutriscore_list[0:selected_nutriscore_index]

        available_best_products_list = []

        for product in product_table:

            if product["nutriscore"] in best_nutriscore_list:

                best_product_dict = {"id_product": "",
                                     "product_name": "",
                                     "nutriscore": "",
                                     "store_name ": "",
                                     "url": ""}

                best_product_dict["id_product"] = product["id_product"]
                best_product_dict["product_name"] = product["product_name"]
                best_product_dict["nutriscore"] = product["nutriscore"]
                best_product_dict["store_name"] = product["store_name"]
                best_product_dict["url"] = product["url"]
                available_best_products_list.append(best_product_dict)

        if len(available_best_products_list) == 0:
            print(
                "Cet article possède déjà"
                " le meilleur nutriscore possible de la catégorie.")

        else:
            substitute_proposed = random.choice(available_best_products_list)
            print("---------------------------------------- ")
            print("SUBSTITUT PROPOSE :")
            print("---------------------------------------- ")
            print("N° du produit : " +
                  str(substitute_proposed["id_product"]) +
                  "\n" +
                  "Nom : " +
                  str(substitute_proposed["product_name"]) +
                  "\n" +
                  "Nutriscore : " +
                  str(substitute_proposed["nutriscore"]) +
                  "\n" +
                  "Store : " +
                  str(substitute_proposed["store_name"]) +
                  "\n" +
                  "url : " +
                  str(substitute_proposed["url"]))
            print("---------------------------------------- ")

            self.record_substitute_choice(
                produit_selected_id,
                substitute_proposed["id_product"])

        self.exit_menu()

    def record_substitute_choice(self, id_product, id_substitute):

        """Records the product selected.

        Parameters
        ----------
        id_product : type int
            The number(id) of the product selected.
        id_substitute : type int
            The number(id) of the substitute selected.

        """

        while True:

            record_choice = input(
                    "Voulez-vous enregistrer le substitut proposé (O/N)?")
            record_choice = record_choice.lower()

            if record_choice == "o":

                # We check if the id of the substitute selected
                # is not already in the table product_has_substitute

                db_filler_fetched = db_filler.DbFiller(self.db_connector)
                substitute_result = db_filler_fetched.check_substitute(
                    id_substitute)

                if substitute_result is None:

                    db_filler_fetched = db_filler.DbFiller(self.db_connector)
                    db_filler_fetched.add_or_get_substitute(
                        id_product, id_substitute)
                    print("Produit bien enregistré")

                else:

                    if substitute_result[
                        "product_id_substitute"] == \
                            id_substitute:

                        print("Cette combinaison produit/substitut"
                              "existe déjà dans votre panier.")

            elif record_choice == "n":

                print("Produit non enregistré.")

            else:
                print("Nous n'avons pas compris."
                      "\nVeuillez recommencer votre saisie.")
                continue

            self.exit_menu()

    def exit_menu(self):

        """ To exit to the application"""

        while True:

            exit_choice = input("Souhaitez-vous quitter l'application (O/N)?")

            if exit_choice == "o":

                print("Vous avez quitté l'application."
                      "Merci et à bientôt sur Pur Beurre !")
                sys.exit()

            elif exit_choice == "n":

                self.manage_main_menu()

            else:
                print("Nous n'avons pas compris votre choix."
                      "\nVeuillez recommencer votre saisie.")
                continue
