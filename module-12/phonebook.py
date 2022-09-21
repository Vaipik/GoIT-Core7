from datetime import datetime
from collections import UserDict
from typing import Optional, List

import errors


class Field:

    def __init__(self, value) -> None:
        self._value = None  # Private not Hidden!!!
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value


class Birthday(Field):

    @Field.value.setter
    def value(self, value: str = None) -> None:  # dd-mm-yyyy -> %d-%m-%Y
        if value:
            try:
                self._value = datetime.strptime(value, '%d-%m-%Y')  # raise ValueError if wrong
            except ValueError:
                raise errors.WrongData('Data should be in format dd-mm-yyyy')

    def __str__(self):
        return self.value.strftime('%d-%m-%Y')


class Email(Field):

    @Field.value.setter
    def value(self, value: str) -> None:

        if '@' in value:
            self._value = value

        else:
            raise errors.WrongEmail(f"Looks like {value} is a wrong email")

    def __str__(self) -> str:
        return self.value


class Name(Field):

    @Field.value.setter
    def value(self, value: str) -> None:
        self._value = value

    def __str__(self) -> str:
        return self.value.title()


class Phone(Field):

    @Field.value.setter
    def value(self, value: str) -> None:

        if len(value) == 10 and value.isdigit():
            self._value = value

        else:
            raise errors.WrongNumber(f"Looks like {value} is a wrong number. It must be 10 digits")

    def __str__(self):
        return f"+38({self.value[:3]}){self.value[3:6]}-{self.value[6:8]}-{self.value[8:]}"  # +38(012)34-567-89


class Record:

    def __init__(self, name: Name, birthday: Optional[Birthday] = None, emails: Optional[List[Email]] = None,
                 phones: Optional[List[Phone]] = None) -> None:

        self.name = name
        self.phones = phones
        self.emails = emails
        self.birthday = birthday

    def add_phone(self, phone: Phone):

        if self.phones:
            self.phones.append(phone)

        else:
            self.phones = [phone]

    def add_email(self, email: Email):

        if self.emails:
            self.emails.append(email)

        else:
            self.emails = [email]

    def change_phone(self, old_phone: str, new_phone: Phone):

        for idx, phone in enumerate(self.phones):

            if phone.value == old_phone:
                self.phones[idx] = new_phone
                break
        else:
            print(f"No {old_phone} in {self.name} record")

    def change_email(self, old_email: str, new_email: Email):

        for idx, email in enumerate(self.emails):

            if email.value == old_email:
                self.emails[idx] = new_email
                break
        else:
            print(f"No {old_email} in {self.name} record")

    def days_to_birthday(self):

        if self.birthday:

            today_date = datetime.now().date()  # -> current date and time
            user_birthday = datetime(year=today_date.year, month=self.birthday.value.month,
                                     day=self.birthday.value.day).strftime('%j')  # User birthday number in a year
            today_date = datetime.now().date().strftime('%j')
            # -> current date and time -> current day -> Day number in a year
            delta = int(user_birthday) - int(today_date)

            if delta > 0:
                print(f"It is {delta} days left to {self.name} birthday")

            elif delta < 0:
                print(f"{self.name}s birthday was {-delta} days ago")

            else:
                print(f"WHOOHOO, {self.name} has a birthday today!!!")
        else:
            print("Contact has no data about birthday")

    def delete_phone(self, phone: str):

        for elem in self.phones:
            if elem.value == phone:
                self.phones.remove(elem)
                break
        else:
            print(f"No {phone} in {self.name} record")

    def delete_email(self, email: str):

        for elem in self.emails:
            if elem.value == email:
                self.emails.remove(elem)
                break
        else:
            print(f"No {email} in {self.name} record")


class AddressBook(UserDict):

    def add_record(self, contact: str, record: Record) -> None:

        if AddressBook.records < 6:

            if contact not in self.data:
                AddressBook.records += 1
            else:
                raise errors.ContactExists(f"{contact} exists in your book")

            self.data[contact] = record

        else:
            print(f"Too many records: {AddressBook.records}")

    def delete_record(self, contact: str) -> None:

        if AddressBook.records > 0:

            self.data.pop(contact)
            print(f"{contact} has been deleted")
            AddressBook.records -= 1

        else:
            print(f'No contact "{contact}" to delete')

    def find_record(self, input_data: str):

        for name, record in self.data.items():

            if input_data in name:
                print(f"Looks like you are looking for {name} record")
                self.__show_record(name, record)

            else:

                if input_data.isdigit():
                    for phone in record.phones:
                        if input_data in phone.value:
                            print(f"Looks like you are looking for {name} record")
                            self.__show_record(name, record)

                for email in record.emails:
                    if input_data in email.value:
                        print(f"Looks like you are looking for {name} record")
                        self.__show_record(name, record)

                if record.birthday and input_data in record.birthday.value.strftime('%d-%m-%Y'):
                    print(f"Looks like you are looking for {name} record")
                    self.__show_record(name, record)

    def iterator(self, record_per_page: int = 1) -> int:
        """
            One record per page by default
        """
        page = 1
        pages = len(self.data) / record_per_page if len(self.data) % record_per_page == 0 else \
            (len(self.data) // record_per_page) + 1
        records = 0  # current printed record
        records_per_page = 0

        for name, record in self.data.items():

            self.__show_record(name, record)

            records_per_page += 1
            records += 1

            if records_per_page == record_per_page:
                print(f"\n{page:>10} of {pages:.0f} pages")
                page += 1
                records_per_page = 0
                yield pages

            elif records == len(self.data):
                print(f"\n{page:>10} of {pages:.0f} pages")
                yield pages

    @staticmethod
    def __show_record(name: str, record: Record) -> None:

        if not record.phones and not record.emails and not record.birthday:
            print(f"\nContact {name.title()} has no data fields")

        else:
            print(f"\nContact {name.title()} has following data:")

        if record.phones:
            print(f"phones: {', '.join([str(phone) for phone in record.phones])}")

        if record.emails:
            print(f"emails: {', '.join([str(email) for email in record.emails])}")

        if record.birthday:
            print(f"{name}s birthday is {record.birthday}")
