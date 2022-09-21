from pathlib import Path
import pickle

from phonebook import AddressBook, Birthday, Email, Name, Phone, Record
import errors


def input_error(func):

    def wrapper(*user_input):

        try:
            return func(*user_input)
        except errors.ContactExists as e:
            print(e)
        except IndexError:
            print('Looks like you forgot to write something.')
        except KeyError as e:
            print(e)
        except ValueError as e:
            print(e)
        except errors.WrongData as e:
            print(e)
        except errors.WrongEmail as e:
            print(e)
        except errors.WrongNumber as e:
            print(e)

    return wrapper


@input_error
def add_phone(user_input: list):  # phone username newphone

    name, new_phone = user_input[0], Phone(user_input[1])
    
    if name not in contact_book:
        raise KeyError(f"{name} does not exist in your contacts")
    
    contact_book[name].add_phone(new_phone)


@input_error    
def add_email(user_input: list):  # username newemail

    name, new_email = user_input[0], Email(user_input[1])
    
    if name not in contact_book:
        raise KeyError(f"{name} does not exist in your contacts")
    
    contact_book[name].add_email(new_email)    
    
    
@input_error
def delete_data(user_input: list) -> None:  # username datatype data

    name, data_type = user_input[0:2]

    if data_type == 'phone':
        contact_book[name].delete_phone(user_input[2])
        
    elif data_type == 'email':
        contact_book[name].delete_email(user_input[2])


@input_error
def delete_contact(user_input: list):   # name
    contact_book.delete_record(user_input[0])


def command_handler(command):
    return OPERATIONS.get(command, wrong_command)


@input_error
def change_record_data(user_input: list) -> None:  # username phone old_phone new_phone

    name, data_type, old_data = user_input[0:3]

    if data_type == 'phone':
        new_data = Phone(user_input[3])
        contact_book[name].change_phone(old_data, new_data)  # Record.change_phone
    
    elif data_type == 'email':
        new_data = Email(user_input[3])
        contact_book[name].change_email(old_data, new_data)  # Record.change_email
    

@input_error
def days_to_birthday(user_input: list):  # name

    name = user_input[0]
    contact_book[name].days_to_birthday()


@input_error
def find(user_input: list):  # data
    contact_book.find_record(user_input[0])


def help(_):

    print('add <contact name> <contact phone(s) or(and) email(s)> to create new record. Use SPACES as separator.')
    print('phone <contact name> <phone> to add new phone.')
    print('email <contact name> <email< to add new email.')
    print('birthday <contact name> to see how many days left to birthday.')
    print('change <contact name> <data type: phone or email> <old data> <new data> to change data.')
    print('clear <contact_name> <data type: phone or email> <data which should be deleted>.')
    print('delete <contact_name> to delete contact.')
    print('find <some data> to search for data.')
    print('show <records per page> to see all records.')
    print('exit, close or goodbye to stop execution.')


@input_error
def new_contact(user_input: list) -> None:  # name data...

    name = Name(user_input[0])
    
    if name.value in contact_book.keys():
        raise errors.ContactExists(f"{name.value} exists in your contacts")

    phones = [Phone(data) for data in user_input[1:] if data.isdigit()]  # Simple check for email
    emails = [Email(data) for data in user_input[1:] if '@' in data]  # Simple check for email
    for data in user_input[1:]:
        birthday = Birthday(data) if '@' not in data and not data.isdigit() else None

    record = Record(name, birthday, emails, phones)
    contact_book.add_record(record.name.value, record)


def parse_user_input(user_input: str):
    return user_input.split(' ')[0]


@input_error
def show_contacts(user_input: list):  # records_per_page

    records = contact_book.iterator(int(user_input[0])) if user_input else contact_book.iterator()
    while True:
        try:
            next(records)
        except StopIteration:
            break


def wrong_command(command: str):
    print(f">>> {command} is a wrong command. Type help to see commands list")


def main():

    stop_words = ('close', 'exit', 'goodbye')
    print("Greetings! I am CLI helper. Type help to see what can I do.")
    
    while True:
    
        user_input = input('>>> ').lower().strip()  # Caseless

        if user_input in stop_words:
            print("Thank you. Bye!")
            with open(path.absolute(), 'wb') as file:
                pickle.dump(contact_book, file)  # Write AddressBook to file
            break
        
        command = parse_user_input(user_input)
        action = command_handler(command)
        action(user_input.split(' ')[1:])  # user input without command
   

if __name__ == '__main__':

    path = Path('data')
    path.mkdir(exist_ok=True)
    path = path.joinpath('phonebook.dat')
    try:
        with open(path.absolute(), 'rb') as file:
            try:
                contact_book = pickle.load(file)
                if not isinstance(contact_book, AddressBook):  # If data not AddressBook object
                    contact_book = AddressBook()
            except EOFError:  # If file is empty
                contact_book = AddressBook()
    except FileNotFoundError:  # If file does not exist
        contact_book = AddressBook()

    OPERATIONS = {
        'add': new_contact,
        'birthday': days_to_birthday,
        'change': change_record_data,
        'clear': delete_data,
        'delete': delete_contact,
        'find': find,
        'help': help,
        'phone': add_phone,
        'email': add_email,
        'show': show_contacts,  # contact_book.show_contacts - чи можна тут записати виклик методу классу ?
        'wrong command': wrong_command,
    }

    main()
