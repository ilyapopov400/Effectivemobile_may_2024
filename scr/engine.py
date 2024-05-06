import csv
import datetime


class ImportCheckData:
    """
    класс для ввода и проверки вводимых пользователем данных
    """

    @staticmethod
    def data() -> str | bool:
        date = input("введите дату в формате 'yyyy-mm-dd'\n")
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            return False

    @staticmethod
    def category() -> str | bool:
        category = input("Введите категорию поступления денежных средств: Доход - 1, Расход - 2\n")
        if category == "1":
            return "Доход"
        elif category == "2":
            return "Расход"
        return False

    @staticmethod
    def summa() -> str | bool:
        summa = input("Введите денежную сумму\n")
        try:
            return str(float(summa))
        except ValueError:
            return False

    @staticmethod
    def description() -> str | bool:
        description = input("введите описание, не более 20 символов")
        if 0 < len(description) <= 20:
            return description
        return False


class BankApp:
    path_db = "./db_bank.csv"  # путь к файлу с базой данных

    def __init__(self):
        with open(self.path_db, encoding='utf-8') as file:
            rows = csv.reader(file, delimiter=',', quotechar='"')
            self.table = list()
            self.head = next(rows)
            for line in rows:
                self.table.append(line)

        self.commands_to_execute = {
            1: ["Список вызываемых команд", self.help],
            2: ["Вывод баланса: Показать текущий баланс, а также отдельно доходы и расходы", self.all_money],
            3: ["Добавление записи: Возможность добавления новой записи о доходе или расходе", self.add_note],
            4: ["Поиск по записям: Поиск записей по категории, дате или сумме", self.search],
        }

    @staticmethod
    def welcome():
        '''
        приветствие пользователя
        :return: None
        '''
        print("Welcome to the Bank App!\n")

    def help(self):
        '''
        возвращает возможные команды
        :return: None
        '''
        for key, volume in self.commands_to_execute.items():
            print(f'{key}:  {volume[0]}')

    @staticmethod
    def _show_one_line_head(line: list):
        '''
        вывод одной форматированной строки заголовка таблицы
        :param line:
        :return: None
        '''
        print('{:^20}|{:^20}|{:^20}|{:^20}'.format(*line))

    @staticmethod
    def _show_one_line_table(line: list):
        '''
        вывод одной форматированной строки тела таблицы
        :param line:
        :return: None
        '''
        print('{:^20}|{:^20}|{:^20.2f}|{:^20}'.format(line[0], line[1], float(line[2]), line[3]))

    def _check_for_duplicate_entries(self, line: list) -> bool:  # TODO нужно ли?
        '''
        проверка на дублирование записи в таблице
        :param line:
        :return:
        '''
        if line in self.table:
            print("Такая запись уже существует\n")
            return False
        return True

    def _writing_table(self):
        '''
        запись таблицы в файл
        :return: None
        '''
        with open(self.path_db, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.head)  # запись заголовков
            for row in self.table:  # запись строк
                writer.writerow(row)

    def all_money(self):
        '''
        Вывод баланса: Показать текущий баланс, а также отдельно доходы и расходы
        :return: None
        '''
        self._show_one_line_head(line=self.head)
        for line in self.table:
            self._show_one_line_table(line=line)
        current_balance, income, expenses = 0, 0, 0
        for row in self.table:
            if row[1] == "Расход":
                current_balance -= float(row[2])
                expenses += float(row[2])
            elif row[1] == "Доход":
                current_balance += float(row[2])
                income += float(row[2])
        print("Текущий баланс составляет: {:.2f}".format(current_balance))
        print("Текущие доходы составляют: {:.2f}".format(income))
        print("Текущие расходы составляют: {:.2f}\n".format(expenses))

    def add_note(self):
        '''
        Добавление записи: Возможность добавления новой записи о доходе или расходе
        :return: None
        '''
        print(
            "Добавьте данные\nдата, категория, сумма, описание\n")

        while True:
            data = ImportCheckData.data()
            category = ImportCheckData.category()
            summa = ImportCheckData.summa()
            description = ImportCheckData.description()
            line = [data, category, summa, description]
            if all(map(lambda x: bool(x), line)):
                self.table.append(line)
                break

        self._writing_table()  # запись таблицы
        print("Ваша запись добавлена в таблицу")

    def search(self) -> list:
        '''
        Поиск записей по одной или нескольким характеристикам
        :return: number_rows -> list: номера найденных строк в self.table
        '''
        result = list()
        number_rows = list()  # номера найденных строк в self.table

        data = ImportCheckData.data()
        category = ImportCheckData.category()
        summa = ImportCheckData.summa()
        description = ImportCheckData.description()

        search_list = [data, category, summa, description]

        for number, line in enumerate(self.table):
            for el, element in enumerate(line):
                if bool(search_list[el]) and search_list[el] != line[el]:
                    break
            else:
                result.append(line)
                number_rows.append(number)

        print('Количество найденных записей: {}'.format(len(result)))
        for line in result:
            self._show_one_line_table(line=line)
        print(number_rows)
        return number_rows

    # def editing_post(self):
    #     '''
    #     редактироване имеющейся записи в телефонном справочнике
    #     :return: None
    #     '''
    #     print("Выберите критерии поиска для редактируемой записи: ")
    #     lines = self.search()
    #     if bool(lines):
    #         number_of_edit_line = int(input("Выберите номер по порядку редактируемой записи: 1 или 2 и т.д.: "))
    #         number_of_edit_line = lines[number_of_edit_line - 1]
    #         new_line = list()
    #         for old_entry in self.table[number_of_edit_line]:
    #             if new_entry := input(
    #                     "Впишите новое значение вместо <{}>, или нажмите ввод, если не хотите менять это значение: ".format(
    #                         old_entry)):
    #                 new_line.append(new_entry)
    #             else:
    #                 new_line.append(old_entry)
    #         if self._check_line(line=new_line) and self._check_for_duplicate_entries(
    #                 line=new_line):  # проверка правильности заполнения и дубля
    #             del self.table[number_of_edit_line]
    #             self.table.append(new_line)
    #             self._writing_table(path=self.path_db, head=self.head, table=self.table)  # запись таблицы
    #             print("Ваша запись в телефонный справочник обновлена")
    #         else:
    #             print("Вы неверно ввели новые значения")
    #
    #     else:
    #         print("Под Ваши критерии не подходит ни одна запись в телефонном справочнике")

    def run(self, number: int):
        '''
        запускает выполнение метода класса по порядковому номеру
        :param number:
        :return:
        '''
        self.commands_to_execute.get(number)[1]()


if __name__ == "__main__":
    a = BankApp()
    a.run(number=4)
    # b = ImportCheckData.summa()
    # print(b)
