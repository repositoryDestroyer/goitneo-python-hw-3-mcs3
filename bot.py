
from address_book import AddressBook, Birthday, Record
from errors import BirthdayError, EmptyListError, IvalidArgsNumberError, PhoneError

book = AddressBook()


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct data."
        except KeyError:
            return "Such a user does not exist."
        except EmptyListError:
            return "Contacts list is empty."
        except IvalidArgsNumberError:
            return "Invalid number of arguments."
        except BirthdayError:
            return "Invalid input format. Birthday should be in the format DD.MM.YYYY"
        except PhoneError:
            return "Invalid input format. Phone number must be in digital format, have 10 characters and not repeat an existing one."
    return inner


@input_error_handler
def add_contact(args, contacts):
    if len(args) != 2:
        raise IvalidArgsNumberError

    name, phone = args
    if not phone.isdigit() or len(phone) != 1:
        raise PhoneError

    recCon = contacts.find(name)
    if recCon != None:
        recCon.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
    return "Contact added."


@input_error_handler
def change_contact(args, contacts):
    if len(args) != 2:
        raise IvalidArgsNumberError
    name, phone = args
    recCon = contacts.find(name)

    if recCon != None:
        recCon.clear_phones()
        recCon.add_phone(phone)
        return "Contact updated."
    raise KeyError


@input_error_handler
def show_phone(args, contacts):
    if len(args) != 1:
        raise IvalidArgsNumberError
    name = args[0]
    recCon = contacts.find(name)
    if recCon == None:
        raise KeyError
    else:
        return ', '.join([f"{phone}" for phone in recCon.phones])


@input_error_handler
def show_all(args, contacts):
    if len(args) != 0:
        raise IvalidArgsNumberError

    if len(contacts.keys()) < 1:
        raise EmptyListError

    contacts_list = []

    for record in contacts.values():
        contacts_list.append(f"{record}")

    return '\n'.join(contacts_list)


@input_error_handler
def add_birthday(args, contacts):
    if len(args) != 2:
        raise IvalidArgsNumberError

    name, date = args
    recCon = contacts.find(name)

    if recCon == None:
        raise KeyError
    try:
        recCon.add_birthday(Birthday(date))
    except:
        raise BirthdayError
    return "Birthday added."


@input_error_handler
def show_birthday(args, contacts):
    if len(args) != 1:
        raise IvalidArgsNumberError
    name = args[0]
    recCon = contacts.find(name)

    if recCon == None:
        raise KeyError
    elif recCon.birthday == None:
        return "Birthday not specified."

    return recCon.birthday.value.date().strftime('%d.%m.%Y')


def birthdays(contacts):
    upcoming = contacts.get_birthdays_per_week()
    if upcoming:
        return "\n".join([f"{week_day}: {', '.join(names)}" for week_day, names in upcoming.items()])
    return "No birthdays next week."


def main():
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
