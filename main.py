

# HW 11 + 9

from collections import UserDict
from datetime import date, datetime
import sys
import re


def normalize_phone(phone):
    numbers = re.findall('\d+', str(phone))
    phone = (''.join(numbers))
    if len(phone) == 10 :
        return phone
    else:
        return None


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.value = value
  

class Birthday(Field):
    def __init__(self, value):
        self.value = value
  

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.__phones = []
        self.__birthday = Birthday(None)

    @property
    def phones(self):
        return self.__phones

    @phones.setter
    def add_phone(self, phone: str) -> None:
        phone = normalize_phone(phone)
        if not phone:
            print (f"Invalid phone number format != 10digit")
        else:
            self.phones.append(Phone(phone))
    
    def remove_phone(self, phone_number: str) -> None | str:
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break
        else:
            raise ValueError(f'phone {phone_number} not found ')

    def edit_phone(self, *args):
        old_phone = args[0]
        new_phone = args[1]
        for id, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[id] = Phone(new_phone)
                break
        else:
            raise ValueError(f'phone {phone} not found in the record')        
      
    def find_phone(self, phone_number: str) -> Phone | str:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        else:
            # raise ValueError(f'phone {phone_number} not found in the record')   
            return (f'phone {phone_number} not found in the record')          

    def days_to_birthday(self) :
        if self.__birthday.value:
            current_date = date.today()
            birth_date = self.__birthday.value
            birth_date = datetime(year=current_date.year, month=birth_date.month,day=birth_date.day).date() 
            delta = birth_date - current_date
            if delta.days >=0:
                return(f"{delta.days} days to birthday")
            else:
                birth_date = datetime(year=current_date.year+1, month=birth_date.month,day=birth_date.day).date() 
                delta = birth_date - current_date
                return(f"{delta.days} days to birthday")
        else:
            return('No birthday date')


    @property
    def birthday(self):
        return f'{self.name.value} birthday {self.__birthday.value}'

    @birthday.setter
    def add_birthday(self, *args):
        try:
            birthday = datetime.strptime(str(args[0]), '%Y-%m-%d')
            self.__birthday = Birthday(birthday.date()) 
        except ValueError:
            print('Error input - Enter birthday in format YYYY-mm-dd')


    def __str__(self):
        return f"Contact: {self.name.value}; phones: {'; '.join(p.value for p in self.phones)}{'; Birthday '+ str(self.__birthday.value) if self.__birthday.value else '' }{';  '+ Record.days_to_birthday(self) if self.__birthday.value else '' }"


class AddressBook(UserDict):
    def add_record(self, *args): 
        name = args[0].name.value
        self.data[name] = args[0]
        self.idx = 0

    def find(self, *args):
        name = args[0]
        if name in self.data:
            return  self.data[name]
        else:
            return None

    def delete(self, *args):
        if self.data.get(args[0]):
            self.data.pop(args[0])


    def __iter__(self):
        self.lst =[]
        for i in self.data.keys():
            self.lst.append(i)     # list of al contacts for iter
        return self

    def __next__(self):
        if self.idx < len(book.data):
            self.idx += 1
            return book.data[self.lst[self.idx-1]]
        else:
            self.idx = 0
            raise StopIteration


  

# ============================================================================================


# decor
def errors(func):
    def inner(*args):
        try:
            return func(*args)
        except :                  #any errors
            return "Give me valid data !!!"
    return inner


# greetings
def greeting(_):
    return ("How can I help you?")


# add contact
@errors
def add(text=""):
    text = text.removeprefix("add ")  #remove command
    name = text.split()[0].title()    #get Name
    text = text.removeprefix(name.lower())    #remove Name
    if not len(text) >9:
        return 'Enter valid  phone'
    phone = normalize_phone(text)
    if not phone:
        return 'Enter valid phone'
    if not book.find(name):
        name = Record(name)
        name.add_phone = phone
        book.add_record(name)
        return name.name.value+" saved with number "+ phone
    name = book.find(name)
    name.add_phone = phone
    book.add_record(name)
    return  name.name.value+' added phone '+ phone


# add birthday
@errors
def birthday(text=""):
    text = text.removeprefix("birthday ")         #remove command
    name = text.split()[0].title()               #get Name
    text = text.removeprefix(name.lower())       #remove Name
    birthday = text.strip()
    if book.data[name]:
        book.data[name].add_birthday = (birthday)
        return book.data[name]
    else:
        return 'no'+name




# change contact if exist
@errors
def change(text=""):
    text = text.removeprefix("change ")
    name = text.split()[0].title()
    text = text.removeprefix(name.lower())
    if not len(text) >9:
        return 'Enter valid name & phone'
    phone = normalize_phone(text)
    if not phone:
        return 'Enter valid phone'
    if name in book.data.keys():
        name = book.data[name]
        old_phone =  name.phones[0].value  #name.phones.value
        name.edit_phone(old_phone, phone)
        # print(name)
        return name.name.value+" change number to "+ phone
    else:
        return (f"no {name} in phone book")


# search contact 
def phone(text=""):
    text = text.removeprefix("phone ")
    name = text.split()[0].title()
    if name in book.data.keys():
        return  book.data[name]
    else:
        return name+' not exist in phone book!!!' 


# show all iter
def show_all(_):
    list = ''
    for cont in book:
        list += str(cont) +'\r\n'
    return list



# show digit
def show(text):
    text = text.removeprefix("show")
    text = text.strip()
    if text.isdigit():
        counter = int(text)        
    count = counter 
    for cont in book:
        print(cont)
        if count > 1:
            count -= 1
        else:
            input("Press Enter for next records >>>")
            count = counter
    return 'finish '
    


# exit program
def exit(_):
    return sys.exit('Good bye!\n')


# dict for commands
dic = { 
    "hi":greeting,
    "hello":greeting,
    "birthday ":birthday,     #adding birthday
    "add ":add,
    "change ":change,
    "phone ":phone,
    "show all":show_all,
    "show":show,            # show 2 -- for iter
    "exit":exit,
    "close":exit,
    "good bye":exit,
}


# find command in text > return dict key
def find_command(text=""): 
    text = text.lower()
    for kee in dic.keys():
        if kee in text:
            return kee
    return None



book = AddressBook()

def main():
    print("I'm Phone_Book_BOT, HELLO!!!")
    # loop forever
    while True:
        user_input =  (input(">>>"))
        comand = find_command(user_input)
        if not comand:
            print("Do not undestend, try again")
        else:
            out = dic[comand](user_input)
            print(out)



# ========================================
if __name__ == "__main__":
    main()







    # john_record2 = Record("John1")
    # john_record2.add_phone = ("1234567892")
    # john_record3 = Record("John2")
    # john_record3.add_phone = ("1234567893")
    # john_record4 = Record("John3")
    # john_record4.add_phone = ("1234567894")
    # john_record4.add_birthday = ("1944-11-14")
    # john_record5 = Record("John4")
    # john_record5.add_phone = ("1234567895")
    # john_record6 = Record("John5")
    # john_record6.add_phone = ("1234567896")
    # book.add_record(john_record2)
    # book.add_record(john_record3)
    # book.add_record(john_record4)
    # book.add_record(john_record5)
    # book.add_record(john_record6)


    # john_record2 = Record("John2")
    # john_record2.add_phone = ("1234567892")
    # # Створення запису для John3
    # john_record3 = Record("John3")
    # john_record3.add_phone = ("1234567893")
    # # Створення запису для John4
    # john_record4 = Record("John4")
    # john_record4.add_phone = ("1234567894")
    # john_record4.add_birthday = ("1944-11-14")
    # # Створення запису для John5
    # john_record5 = Record("John5")
    # john_record5.add_phone = ("1234567895")
    # # Створення запису для John6
    # john_record6 = Record("John6")
    # john_record6.add_phone = ("1234567896")

    # # Додавання запису John до адресної книги
    # book.add_record(john_record)
    # # Додавання запису John до адресної книги
    # book.add_record(john_record2)
    # # Додавання запису John до адресної книги
    # book.add_record(john_record3)
    # # Додавання запису John до адресної книги
    # book.add_record(john_record4)
    # # Додавання запису John до адресної книги
    # book.add_record(john_record5)
    # # Додавання запису John до адресної книги
    # book.add_record(john_record6)

    # # Створення та додавання нового запису для Jane
    # jane_record = Record("Jane")
    # jane_record.add_phone ="9876543210"
    # # add birthday
    # jane_record.add_birthday = ("1988-11-6")
    # book.add_record(jane_record)

    # # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)

    # # Знаходження та редагування телефону для John
    # john = book.find("John")
    # john.edit_phone("5555555555", "1112223333")

    # print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555


    # # Пошук unknown телефону у записі John
    # found_phone = john.find_phone("5555155555")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # # Пошук конкретного телефону у записі John
    # found_phone = john.find_phone("1112223333")
    # print(f"{john.name}: {found_phone}")  

    # print('\r\n\n')
    