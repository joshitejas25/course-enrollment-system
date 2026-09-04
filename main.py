from app.database import create_tables
from app.ui import application_menu, show_welcome_message


def main():
    create_tables()
    show_welcome_message()
    application_menu()


if __name__ == "__main__":
    main()