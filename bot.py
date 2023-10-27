class EmptyListError(Exception):
    pass


class IvalidArgsNumberError(Exception):
    pass


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Such a user does not exist."
        except EmptyListError:
            return "Contacts list is empty."
        except IvalidArgsNumberError:
            return "Invalid number of arguments."
    return inner


@input_error_handler
def add_contact(args, contacts):
    if len(args) != 2:
        raise IvalidArgsNumberError
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error_handler
def change_contact(args, contacts):
    if len(args) != 2:
        raise IvalidArgsNumberError
    name, phone = args
    contacts[name] = phone
    return "Contact updated."


@input_error_handler
def show_phone(args, contacts):
    if len(args) != 1:
        raise IvalidArgsNumberError
    name = args[0]
    if name not in contacts:
        raise KeyError
    else:
        return contacts[name]


@input_error_handler
def show_all(args, contacts):
    if len(args) != 0:
        raise IvalidArgsNumberError

    if len(contacts.keys()) < 1:
        raise EmptyListError

    contacts_list = []

    for name, phone in contacts.items():
        contacts_list.append(f"{name}: {phone}")

    return '\n'.join(contacts_list)


def main():
    contacts = {}
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
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
