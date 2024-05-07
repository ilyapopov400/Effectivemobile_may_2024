'''
основной файл для работы с программой
'''

import engine


def mane():
    bank_app = engine.BankApp()
    bank_app.welcome()
    bank_app.help()

    while True:
        print(
            "Выберите число от 1 до {} или нажмите любую другую клавишу для окончания работы программы\n<1> - help"
            .format(len(bank_app.commands_to_execute)))
        user_input = input("Ваш выбор? \n")

        if user_input in [str(x) for x in range(len(bank_app.commands_to_execute) + 1)]:
            bank_app.run(number=int(user_input))
            print("Ваше следующее действие?\n")
        else:
            print("До свиданья!")
            break


if __name__ == "__main__":
    mane()
