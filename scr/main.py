'''
основной файл для работы с программой
'''

import engine


def mane():
    phone_book = engine.BankApp()
    phone_book.welcome()
    phone_book.help()

    while True:
        print(
            "Выберите число от 1 до {} или нажмите любую другую клавишу для окончания работы программы\n<1> - help"
            .format(len(phone_book.commands_to_execute)))
        user_input = input("Ваш выбор? \n")

        if user_input in [str(x) for x in range(len(phone_book.commands_to_execute) + 1)]:
            phone_book.run(number=int(user_input))
            print("Ваше следующее действие?\n")
        else:
            print("До свиданья!")
            break


if __name__ == "__main__":
    mane()
