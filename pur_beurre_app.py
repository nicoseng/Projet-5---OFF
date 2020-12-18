"""Internal imports """
import user_interface


def main():

    """To load the application."""

    load_interface = user_interface.UserInterface()
    load_interface.manage_welcome_menu()
    load_interface.manage_main_menu()


if __name__ == "__main__":
    main()
