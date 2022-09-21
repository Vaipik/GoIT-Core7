from phonebook import AddressBook, Email, Name, Phone, Record

import errors


def input_error(func):

    def wrapper(user_input):
        
        try:
            string = user_input.split(' ')
            func(user_input)
        except errors.NoContact:
            print(f'Looks like there are no such contact "{string[1].title()}".')
        except errors.ContactExists:
            print(f'Looks like contact "{string[1].title()}" already exists. Try to change it if you want.')
        except IndexError:
            print(f"Looks like you forgot to enter something")
        except KeyError:
            print(f"Looks like there are no {string[1].title()} in your phonebook")
        except ValueError:
            print(f"No field")
        
    return wrapper


@input_error
def add_phone(user_input:str): # phone username newphone
    
    user_input: list = user_input.split(' ')
    name, new_phone = user_input[1], Phone(user_input[2])
    contact_book[name].add_phone(new_phone)


@input_error    
def add_email(user_input:str): # email username newemail
    
    user_input: list = user_input.split(' ')
    name, new_email = user_input[1], Email(user_input[2])
    contact_book[name].add_email(new_email)    
    
    
@input_error
def delete_data(user_input:str) -> None: # delete username datatype 

    user_input: list = user_input.split(' ')
    name, data_type = user_input[1:3]

    if data_type == 'phones':
        contact_book[name].delete_phones()

    elif data_type == 'phone':
        contact_book[name].delete_phone(user_input[3])
        
    elif data_type == 'emails':
        contact_book[name].delete_emails()
    
    elif data_type == 'email':
        contact_book[name].delete_email(user_input[3])
    


@input_error
def delete_contact(user_input:str):

    string = user_input.split(' ')
    name = string[1]
    contact_book.delete_record(name)


def command_handler(command):
    return OPERATIONS.get(command, wrong_command)


@input_error
def change_record_data(user_input:str) -> None: # change username phone old_phone new_phone

    user_input = user_input.split(' ')
    name, data_type, old_data = user_input[1:4]

        
    if data_type == 'phone':
        print(data_type)
        new_data = Phone(user_input[4])
        contact_book[name].change_phone(old_data, new_data) # Record.change_phone
    
    elif data_type == 'email':
        new_data = Email(user_input[4])
        contact_book[name].change_email(old_data, new_data) # Record.change_email
    

def help(_):

    print('add <contact name> <contact phone(s) or(and) email(s)> to create new record. Use SPACES as separator')
    print('new phone <contact name> <phone> to add new phone.')
    print('new email <contact name> <email< to add new email.')
    print('change <contact name> <data type: phone or email> <old data> <new data> to change data') 
    print('clear <contact_name> <data type: phone or email> <data which should be deleted, to delete all field leave empty>')
    print('delete <contact_name> to delete contact')
    print('show <contact_name> to get contact data')
    print('show all to get all contacts data')
    print('exit, close or goodbye to stop execution')


@input_error
def new_contact(user_input:str) -> Record:
    
    user_input = user_input.split(' ')
    
    name = Name(user_input[1])
    phones = [Phone(elem) for elem in user_input if elem.isdigit()]
    emails = [Email(elem) for elem in user_input if '@' in elem]
    
    if name.value in contact_book.keys():
        raise errors.ContactExists
    
    record = Record(name, phones=phones, emails=emails)
    contact_book.add_record(record.name.value, record)


def parse_user_input(user_input:str):
    return user_input if user_input == 'show all' else user_input.split(' ')[0]


def show_contacts(_):
    contact_book.show_data()    


@input_error
def show_contact_data(user_input:str):

    string = user_input.split(' ')
    name = string[1]
    contact_book.show_data(name) # Access to record    
    

def wrong_command(command):
    print(f">>> {command} is a wrong command")


def main():

    stop_words = ('close', 'exit', 'goodbye')
    print("Greetings! I am CLI helper. Type help to see what can I do.")
    while True:
    
        user_input = input('>>> ').lower().strip() # Caseless
        
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
        'change': change_record_data,
        'clear': delete_data,
        'delete': delete_contact,
        'help': help,
        'phone': add_phone,
        'email': add_email,
        'show': show_contact_data,
        'show all': show_contacts, # contact_book.show_contacts - чи можна тут записати виклик методу классу ?
        'wrong command': wrong_command,
    }

    main()
