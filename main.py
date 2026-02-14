from modules import app_obj, main_window


def main():
    try:
        main_window.show()
        app_obj.exec()
    except Exception as error:
        print(f"Помилка під час запуску проєкту: {error}")


if __name__ == "__main__":
    main()
