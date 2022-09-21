from collections import UserDict
from typing import List

import errors


class Field:
    
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value


class Email(Field):
    pass


class Name(Field):

    def __str__(self) -> str:
        return self.value.title()
    

class Phone(Field):
    pass
    
        
class Record:

    def __init__(self, name:Name, emails: List[Email] = [], phones: List[Phone] = []) -> None:
        
        self.name = name
        self.phones = phones
        self.emails = emails     
        
    def add_phone(self, phone: Phone):
        self.phones.append(phone)
        
    def add_email(self, email: Email):
        self.emails.append(email)
    
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
                
    def delete_phone(self, phone:str):
        
        for elem in self.phones:
            if elem.value == phone:
                self.phones.remove(elem)
                break
        else:
            print(f"No {phone} in {self.name} record")
                
    def delete_phones(self):
        self.phones.clear()
                
    def delete_email(self, email:str):
        
        for elem in self.emails:
            if elem.value == email:
                self.emails.remove(elem)
                break
        else:
            print(f"No {email} in {self.name} record")

    def delete_emails(self):
        self.emails.clear()
       
       
class AddressBook(UserDict):
    
    records = 0

    def add_record(self, contact:str, record:Record) -> None:
        
        if AddressBook.records < 3:

            if contact not in self.data:  
                AddressBook.records += 1
            else:
                raise errors.ContactExists
            
            self.data[contact] = record

        else:
            print(f"Too many records: {AddressBook.records}")

    def delete_record(self, contact:str) -> None:

        if AddressBook.records > 0:

            if contact not in self.data:
                raise errors.NoContact
            
            self.data.pop(contact)
            print(f"{contact} has been deleted")
            AddressBook.records -= 1
        
        else:
            print(f'No contact "{contact}" to delete')

    def show_data(self, contact: str = None) -> None:
        """
            If no contact name will be given method will show all contacts
        """
        end_flag = False # To show exact contact
        for name, record in self.data.items():
            
            if contact is not None: 
                
                if contact not in self.data:
                    raise errors.NoContact
                
                if name != contact: 
                    continue
                
                end_flag = True # Desired contact has been found
                
            if not record.phones and not record.emails:
                print(f"Contact {name} has no data fields")
            
            else:
                print(f"Contact {name} has following data:")
            
            if record.phones:
                data = [elem.value for elem in record.phones]
                print(f"phones: {', '.join(data)}")
            
            if record.emails:
                data = [elem.value for elem in record.emails]
                print(f"emails: {', '.join(data)}")
                

            if end_flag: # Stop printing 
                break
            