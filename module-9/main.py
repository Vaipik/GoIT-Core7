# Напишіть консольного бота помічника, який розпізнаватиме команди, що вводяться з клавіатури,
# і відповідати відповідно до введеної команди.

# Бот помічник повинен стати для нас прототипом додатка-асистента. 
# Додаток-асистент в першому наближенні повинен уміти працювати з книгою контактів і календарем.
# У цій домашній роботі зосередимося на інтерфейсі самого бота. 
# Найбільш простий і зручний на початковому етапі розробки інтерфейс - це консольний додаток CLI (Command Line Interface).
# CLI досить просто реалізувати. Будь-який CLI складається з трьох основних елементів:

# Парсер команд. Частина, яка відповідає за розбір введених користувачем рядків, виділення з рядка ключових слів та модифікаторів команд.
# Функції обробники команд — набір функцій, які ще називають handler, вони відповідають за безпосереднє виконання команд.
# Цикл запит-відповідь. Ця частина програми відповідає за отримання від користувача даних
# та повернення користувачеві відповіді від функції-handlerа.

# На першому етапі наш бот-асистент повинен вміти зберігати ім'я та номер телефону, знаходити номер телефону за ім'ям, 
# змінювати записаний номер телефону, виводити в консоль всі записи, які зберіг. Щоб реалізувати таку нескладну логіку, скористаємося словником.
# У словнику будемо зберігати ім'я користувача як ключ і номер телефону як значення.

# Умови

#     Бот повинен перебувати в безкінечному циклі, чекаючи команди користувача.
#     Бот завершує свою роботу, якщо зустрічає слова: .
#     Бот не чутливий до регістру введених команд.
#     Бот приймає команди:
#         "hello", відповідає у консоль "How can I help you?"
#         "add ...". За цією командою бот зберігає у пам'яті (у словнику наприклад) новий контакт. 
#         Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
#         "change ..." За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту.
#         Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
#         "phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту.
#         Замість ... користувач вводить ім'я контакту, чий номер треба показати.
#         "show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
#         "good bye", "close", "exit" по будь-якій з цих команд бот завершує свою роботу після того, як виведе у консоль "Good bye!".
#     Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error.
#     Цей декоратор відповідає за повернення користувачеві повідомлень виду "Enter user name", "Give me name and phone please" і т.п.
#     Декоратор input_error повинен обробляти винятки, що виникають у функціях-handler (KeyError, ValueError, IndexError)
#     та повертати відповідну відповідь користувачеві.
#     Логіка команд реалізована в окремих функціях і ці функції приймають на вхід один або декілька рядків та повертають рядок.
#     Вся логіка взаємодії з користувачем реалізована у функції main, всі print та input відбуваються тільки там.


def input_error(func):

    def wrapper(user_input:str):
        
            try:
                string = user_input.split(' ')
                func(user_input)
            except KeyError:
                print(f'Looks like there are no {string[1]} in your phonebook.')
            except ValueError:
                print(f'{string[2]} - is a wrong number. Only digits are available.')
            except IndexError:
                print('Looks like you forgot to write something.')
                      
    return wrapper


@input_error
def add_contact(user_input:str):
    
    string = user_input.split(' ')
    int(string[2])
    phone_book[string[1]] = string[2]


@input_error
def change_phone(user_input:str):

    string = user_input.split(' ')
    if string[1] not in phone_book: # If no such contact in phonebook
        raise KeyError 

    phone_book[string[1]] = string[2]


def command_handler(command):
    return OPERATIONS.get(command, wrong_command)


def greeting(_):
    print('> How can i help you?')


def parse_user_input(user_input:str):
    return user_input if user_input == 'show all' else user_input.split(' ')[0]


def show_all(_):

    if len(phone_book) == 0:
        print('No contacts were added')
    
    for k, w in phone_book.items():
        print(f"{k.title()}'s phone number is: {w}")


@input_error
def show_phone(user_input:str):

    string = user_input.split(' ')
    print(f"{string[1].title()}'s phone is {phone_book[string[1]]}")

def wrong_command(command):
    print(f"{command} is a wrong command ")
    

def main():

    stop_words = ('close', 'exit', 'good bye')

    while True:

        user_input = input('>>> ').lower()
        
        if user_input in stop_words or '.' in user_input or '.'  in user_input:
            print('Good bye!')
            break

        command = parse_user_input(user_input)

        action = command_handler(command)
        action(user_input)


if __name__ == '__main__':
    
    OPERATIONS = {
    'hello': greeting,
    'add': add_contact,
    'change': change_phone,
    'phone': show_phone,
    'show all': show_all,
    'wrong command': wrong_command,
    }

    phone_book = {}

    main()








