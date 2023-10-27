from collections import UserDict
from datetime import datetime
from collections import defaultdict
from errors import PhoneError


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)


class Birthday:
    def __init__(self, value):
        self.value = datetime.strptime(value, '%d.%m.%Y')


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        for ph in self.phones:
            if phone == ph.value:
                raise PhoneError
        self.phones.append(Phone(phone))

    def clear_phones(self):
        self.phones = []

    def add_birthday(self, value):
        self.birthday = value

    def __str__(self):
        return f"Contact: name: {self.name.value}; phones: [{', '.join(phone.value for phone in self.phones)}]; birthday: {self.birthday.value.date().strftime('%d.%m.%Y') if self.birthday != None else 'Not specified.'}"


class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        self.data[name] = record

    def find(self, name):
        return self.get(name, None)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)

    def get_birthdays_per_week(self):
        next_week_birthdays = defaultdict(list)

        today = datetime.today().date()

        for name, value in self.data.items():
            if value.birthday == None:
                continue

            birthday = value.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days
            if delta_days > 6:
                continue

            day_of_week = birthday_this_year.strftime("%A")
            if day_of_week == "Saturday" or day_of_week == "Sunday":
                next_week_birthdays["Monday"].append(name)
            else:
                next_week_birthdays[day_of_week].append(name)

        return next_week_birthdays
