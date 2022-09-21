from phonebook import AddressBook, Birthday, Email, Name, Phone, Record
import errors


def input_error(func):

    def wrapper(user_input):

        try:
            string = user_input.split(' ')
            func(user_input)
        except errors.ContactExists:
            print(f'Looks like contact "{string[1].title()}" already exists. Try to change it if you want.')
        except IndexError:
            print(f"Looks like you forgot to enter something")
        except KeyError:
            print(f"Looks like there are no {string[1].title()} in your phonebook")
        except ValueError:
            print(f"You entered something wrong")
        except errors.WrongData:
            print("Data should be dd-mm-yyyy. Try again")
        except errors.WrongEmail:
            print("Wrong email. Try again.")
        except errors.WrongNumber:
            print("Wrong phone. Must be equal to 10 digits.")    

    return wrapper


@input_error
def add_phone(user_input: str):  # phone username newphone
    
    user_input: list = user_input.split(' ')
    name, new_phone = user_input[1], Phone(user_input[2])
    
    if name not in contact_book:
        raise KeyError
    
    contact_book[name].add_phone(new_phone)


@input_error    
def add_email(user_input: str):  # email username newemail
    
    user_input: list = user_input.split(' ')
    name, new_email = user_input[1], Email(user_input[2])
    
    if name not in contact_book:
        raise KeyError
    
    contact_book[name].add_email(new_email)    
    
    
@input_error
def delete_data(user_input: str) -> None:  # delete username datatype

    user_input: list = user_input.split(' ')
    name, data_type = user_input[1:3]

    if data_type == 'phone':
        contact_book[name].delete_phone(user_input[3])
        
    elif data_type == 'email':
        contact_book[name].delete_email(user_input[3])


@input_error
def delete_contact(user_input: str):

    string = user_input.split(' ')
    name = string[1]
    contact_book.delete_record(name)


def command_handler(command):
    return OPERATIONS.get(command, wrong_command)


@input_error
def change_record_data(user_input: str) -> None:  # change username phone old_phone new_phone

    user_input = user_input.split(' ')
    name, data_type, old_data = user_input[1:4]

    if data_type == 'phone':
        new_data = Phone(user_input[4])
        contact_book[name].change_phone(old_data, new_data)  # Record.change_phone
    
    elif data_type == 'email':
        new_data = Email(user_input[4])
        contact_book[name].change_email(old_data, new_data)  # Record.change_email
    

@input_error
def days_to_birthday(user_input: str):
    
    user_input = user_input.split(' ')
    name = user_input[1]
    contact_book[name].days_to_birthday()


def help(_):

    print('add <contact name> <contact phone(s) or(and) email(s)> to create new record. Use SPACES as separator')
    print('phone <contact name> <phone> to add new phone.')
    print('email <contact name> <email< to add new email.')
    print('birthday <contact name> to see how many days left to birthday')
    print('change <contact name> <data type: phone or email> <old data> <new data> to change data') 
    print('clear <contact_name> <data type: phone or email> <data which should be deleted>')
    print('delete <contact_name> to delete contact')
    print('show <records per page> to see all records')
    print('exit, close or goodbye to stop execution')


@input_error
def new_contact(user_input: str) -> None:

    user_input = user_input.split(' ')
    
    name = Name(user_input[1])
    
    if name.value in contact_book.keys():
        raise errors.ContactExists

    phones = [Phone(data) for data in user_input[2:] if data.isdigit()]  # Simple check for email
    emails = [Email(data) for data in user_input[2:] if '@' in data]  # Simple check for email
    birthday = [Birthday(data) for data in user_input[2:] if '@' not in data and not data.isdigit()]
    record = Record(name, birthday[0], emails, phones)
    contact_book.add_record(record.name.value, record)


def parse_user_input(user_input: str):
    return user_input.split(' ')[0]


@input_error
def show_contacts(user_input: str):
    
    user_input = user_input.split(' ')
    records: contact_book.iterator = contact_book.iterator(int(user_input[1])) if user_input[1:] else contact_book.iterator()
    while True:
        try:
            next(records)
        except StopIteration:
            break
    

def wrong_command(command):
    print(f">>> {command} is a wrong command. Type help to see commands list")


def main():

    stop_words = ('close', 'exit', 'goodbye')
    print("Greetings! I am CLI helper. Type help to see what can I do.")
    
    while True:
    
        user_input = input('>>> ').lower().strip()  # Caseless
        
        if user_input in stop_words:
            print("Thank you. Bye!")
            break
        
        command = parse_user_input(user_input)
        action = command_handler(command)
        action(user_input)
   

if __name__ == '__main__':
    
    contact_book = AddressBook()
    
    OPERATIONS = {
        'add': new_contact,
        'birthday': birthday,
        'change': change_record_data,
        'clear': delete_data,
        'delete': delete_contact,
        'help': help,
        'phone': add_phone,
        'email': add_email,
        'show': show_contacts,  # contact_book.show_contacts - чи можна тут записати виклик методу классу ?
        'wrong command': wrong_command,
    }

    main()
