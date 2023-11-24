
# web HW 1 

from abc import ABC, abstractmethod
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from collections import UserDict
from datetime import date, datetime
import pickle
import sys
import re

file_name = 'book.bin'

def normalize_phone(phone):
    numbers = re.findall('\d+', str(phone))
    phone = (''.join(numbers))
    if len(phone) == 10 :
        return phone
    else:
        return None


class Field(ABC):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    @abstractmethod
    def __getitem__(self):
        pass


class Name(Field):
    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        birthday = datetime.strptime(str(value), '%Y-%m-%d')
        birthday = birthday.date()
        self.__value = birthday
        if not self.__value:
            raise ValueError  (f"Invalid  format  birthday")

    def __str__(self):
        return str(self.value)

    def __getitem__(self):
        return self.value
  

class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
        # super().__init__(self.__value)  #???

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        self.__value = normalize_phone(value)
        if not self.__value:
            raise ValueError  (f"Invalid phone number format != 10digit")

    def __getitem__(self):
        return self.value


class MailField(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, mail):
        iterator = re.finditer(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", mail)
        for match in iterator:
            self.__value = match.group()
        if not self.__value:
            raise ValueError(f"{mail} isn't valid mail")

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __getitem__(self):
        return self.value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.mails = []
        self.__birthday = None

    def add_phone(self, phone: str) -> None:
        if phone not in self.phones:
            self.phones.append(Phone(phone))
            return f"Phone number {phone} add to contact {self.name}"
        print (f"Phone number {phone} present in contact {self.name}")

    def add_mail(self, mail: str) -> None:
        if mail not in self.mails:
            self.mails.append(MailField(mail))
            return f"Mail {mail} added to contact {self.name}"
        print (f"Mail {mail} present in contact {self.name}")

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

    def add_birthday(self, *args):
        try:
            self.__birthday = Birthday(args[0]) 
        except ValueError:
            print('Error input - Enter birthday in format YYYY-mm-dd')

    def __str__(self):
        return f"Contact: {self.name.value}; phones: {'; '.join(p.value for p in self.phones)}{'; Birthday '+ str(self.__birthday.value) if self.__birthday else '' }{';  '+ Record.days_to_birthday(self) if self.__birthday else '' }"


class AddressBook(UserDict):
    def add_record(self, *args): 
        name = args[0].name.value
        self.data[name] = args[0]
        self.idx = 0

    def load(self) -> None:
        # load contacts from file
        try:
            with open(file_name, 'rb') as file:
                self = pickle.load(file)
                print('Book loadeed from file ')
                return self
        except:
            print('No book file yet')

    def save(self):
        with open(file_name, 'wb') as file:
            pickle.dump(book, file)
       
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

class Printing:
    def __init__(self) -> None:
        pass



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
    text = text.strip()
    name = text.split()[0].title()  # get Name
    text = text.removeprefix(name.lower())  # remove Name
    if not len(text) > 9:
        return 'Enter valid  phone 10dig'
    phone = normalize_phone(text)
    # phone = text
    if not phone:
        return 'Enter valid phone 10 dig'
    if not book.find(name):
        name = Record(name)
        name.add_phone(phone)
        book.add_record(name)
        return name.name.value+" saved with number " + phone
    name = book.find(name)
    name.add_phone(phone)
    book.add_record(name)
    return name.name.value+' added phone ' + phone

# add contact


@errors
def add_mail(text=""):
    text = text.strip()
    name = text.split()[0].title()  # get Name
    text = text.removeprefix(name.lower())  # remove Name
    mail = text.strip()
    if not len(mail) > 5:
        return 'Enter valid  mail > to short'
    if not book.find(name):
        return name.name.value +" not in book "  
    name = book.find(name)
    name.add_mail(mail)
    book.add_record(name)
    return name.name.value+' added mail ' + mail

# add birthday
@errors
def birthday(text=""):
    text = text.strip()
    name = text.split()[0].title()               #get Name
    text = text.removeprefix(name.lower())       #remove Name
    birthday = text.strip()
    if book.data.get(name):
        book.data[name].add_birthday(birthday)
        return book.data[name]
    else:
        return 'no '+name+' in book, add phone first'

# change contact if exist
@errors
def change(text=""):
    text = text.strip()
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
        return name.name.value+" change number to "+ phone
    else:
        return (f"no {name} in phone book")

# search contact 
def phone(text=""):
    text = text.strip()
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
    
# little HELP
def help(_):
    return """ 
    "help" for help 
    "add" for add contact
    "find" for find in book
    "hi" or "hello" for greeting
    "birthday" to add birthday for exiting contact 
    "change" for change number
    "phone" for look  phone in contact
    "show all" to show all book
    "show" to show part of book    'show 2' - example
    "exit" or "close" or "good bye" for exit and save book changes in file
    """


# iter in book and compare with FIND_text
def find(text):
    text = text.strip()
    if not len(text) > 2:
        return 'Enter more then 2 simbols to find'
    list = ''
    for cont in book:
        if text in str(cont).lower():
            list += str(cont) +'\r\n'
    return list if len(list) > 1 else 'Cant find it'


# exit program and save book to hhd
def exit(_):
    book.save()
    return sys.exit('Good bye!\n')


# dict for commands
dic = { 
    "help":help,
    "find ":find,
    "hi":greeting,
    "hello":greeting,
    "birthday ":birthday,     #adding birthday
    "add phone ":add,
    "add mail ": add_mail,
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
            return kee, text.removeprefix(kee)
    return None


def tips():
    # створення списку підказок
    variants = {}
    for i in dic.keys():
        variants[i] = None
    # Створення об'єкта WordCompleter для автодоповнення
    completer = NestedCompleter.from_nested_dict(variants)
    return completer


book = AddressBook()

def main():
    print("I'm Phone_Book_BOT, HELLO!!!")
    # loop forever
    while True:
        user_input = (prompt(">>>", completer = tips()))
        comand, user_input = find_command(user_input)
        if not comand:
            print("Do not undestend, try again or use 'help'")
        else:
            out = dic[comand](user_input)
            print(out)


# ========================================
# ========================================

if __name__ == "__main__":
    # book = book.load()
    # n = book.data['Nina']
    # n.name.__getitem__()
    main()






