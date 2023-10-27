from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Please write a 10-digit number.")
        super().__init__(phone)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_instance = Phone(phone)
        self.phones.append(phone_instance)

    def remove_phone(self, new_phone):
        for phone in self.phones:
            if phone.value == new_phone:
                self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone_to_find):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(phone.value for phone in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        self.data[name] = record

    def find(self, name):
        return self.get(name, None)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
