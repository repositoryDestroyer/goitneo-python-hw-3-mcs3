from collections import UserDict
from datetime import datetime
from collections import defaultdict
from errors import PhoneError, BirthdayError


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 or value.isdigit()):
            raise PhoneError("Invalid input format. Phone number must be in digital format, have 10 characters")
        super().__init__(value)


class Birthday:
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise BirthdayError("Invalid input format. Birthday should be in the format DD.MM.YYYY")
    
    def __str__(self) -> str:
        return self.value.strftime('%d.%m.%Y')



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        for ph in self.phones:
            if phone == ph.value:
                raise PhoneError("Invalid input format. Phone number must not repeat an existing one.")
        self.phones.append(Phone(phone))

    def clear_phones(self):
        self.phones = []

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def __str__(self):
        phones = ', '.join(phone.value for phone in self.phones)
        return f"Contact: name: {self.name.value}; phones: {phones}; birthday: {self.birthday if self.birthday else 'Not specified.'}"


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
            if not value.birthday:
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
