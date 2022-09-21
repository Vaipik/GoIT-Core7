# Вам нужно реализовать полезную функцию для вывода списка коллег
# которых надо поздравить с днём рождения на неделе.

# У вас есть список словарей users, каждый словарь в нём обязательно имеет ключи name и birthday.
# Такая структура представляет модель списка пользователей с их именами и днями рождения.
# name — это строка с именем пользователя
# birthday — это datetime объект, в котором записан день рождения.

# Ваша задача написать функцию get_birthdays_per_week, которая получает на вход список users и 
# выводит в консоль (при помощи print) список пользователей, которых надо поздравить по дням.

# Условия приёмки
# get_birthdays_per_week выводит именинников в формате:

# Monday: Bill, Jill
# Friday: Kim, Jan

# Пользователей, у которых день рождения был на выходных, надо поздравить в понедельник.
# Для отладки удобно создать тестовый список users и заполнить его самостоятельно.
# Функция выводит пользователей с днями рождения на неделю вперед от текущего дня.
# Неделя начинается с понедельника.

from datetime import datetime, timedelta
from copy import deepcopy
from random import randint as rand


def get_birthdays_per_week(users_list:list):
    
    users = deepcopy(users_list) # To keep original list

    current_datetime = datetime.now()

    current_week_number = current_datetime.strftime('%W')
    next_week_beginning = datetime.strptime(f"{current_datetime.year}-{int(current_week_number)}-{6}", "%Y-%W-%w")
    next_week_ending = datetime.strptime(f"{current_datetime.year}-{int(current_week_number) + 1}-{5}", "%Y-%W-%w")

    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
    birthdays = {day: [] for day in days}

    for user in users:
        
        user['birthday'] = user['birthday'].replace(year=current_datetime.year)
        if next_week_beginning.date() <= user['birthday'].date() <= next_week_ending.date():
            
            day = user['birthday'].strftime('%w')
            day_name = weekday_name(day)
            
            if day_name == 'Saturday' or day_name == 'Sunday':
                birthdays['Monday'].append(user['name'])
            
            else:
                birthdays[day_name].append(user['name'])

    for k, w in birthdays.items():
        
        if w:
            print(f"{k:>9}: {', '.join(w)}")
        
        else:
            print(f"{k:>9}: no birthdays")


def user_generation(quantity:int) -> list:

    users = []
    
    for _ in range(quantity):

        user_name = ""

        # try:
        #     user_birthday = datetime(year=rand(1960, 2007), month=rand(1,12), day=rand(1, 31), hour=rand(0,23), minute=rand(0,59))
        # except ValueError:
        #     user_birthday = datetime(year=rand(1960, 2007), month=2, day=rand(1, 28), hour=rand(0,23), minute=rand(0,59))

        user_birthday = datetime(year=rand(1960, 2007), month=7, day=rand(1, 31), hour=rand(0,23), minute=rand(0,59))

        while len(user_name) <= rand(3, 9):

            if user_name:
                user_name += chr(rand(97, 122))
            
            else:
                user_name += chr(rand(65, 90))

        users.append(
            {
                'name': user_name,
                'birthday': user_birthday
            }
        )

    return users


def weekday_name(weekday_number:str) -> str:
    
    days = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
    weekday_names = {str(day_num): day for day_num, day in zip(range(7), days)}

    return weekday_names[weekday_number]


if __name__ == '__main__':

    users = user_generation(10)

    for user in users:
        print(f"{user['name']:<10} and he or she was born on {user['birthday'].strftime('%d.%m.%Y')}")

    get_birthdays_per_week(users)



