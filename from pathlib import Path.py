import sys
import pprint
from pathlib import Path
from colorama import Fore, Style, init

# Ініціалізація colorama для кольорового виводу в консолі
init(autoreset=True)


# ЗАВДАННЯ 1:


def total_salary(path: str) -> tuple[float, float]:
    path_obj = Path(path)
    if not path_obj.exists():
        print(f"{Fore.RED}Помилка: Файл {path} не знайдено.")
        return (0.0, 0.0)

    total = 0.0
    count = 0

    try:
        with open(path_obj, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    name, salary = line.split(",")
                    total += float(salary)
                    count += 1
        
        average = total / count if count > 0 else 0.0
        return total, average

    except Exception as e:
        print(f"{Fore.RED}Сталася помилка при читанні файлу: {e}")
        return (0.0, 0.0)

# ЗАВДАННЯ 2


def get_cats_info(path: str) -> list[dict]:
    cats_info = []
    path_obj = Path(path)
    
    if not path_obj.exists():
        print(f"{Fore.RED}Помилка: Файл {path} не знайдено.")
        return []

    try:
        with open(path_obj, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    cat_id, name, age = line.split(",")
                    cats_info.append({
                        "id": cat_id,
                        "name": name,
                        "age": age
                    })
        return cats_info

    except Exception as e:
        print(f"{Fore.RED}Сталася помилка при обробці даних про котів: {e}")
        return []


# ЗАВДАННЯ 3:

def list_directory_contents(path: Path, prefix: str = ""):

    try:
        if not path.exists() or not path.is_dir():
            return


        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "┗ " if is_last else "┣ "
            
            if item.is_dir():
                print(f"{prefix}{connector}{Fore.BLUE}📂 {item.name}{Style.RESET_ALL}")
                # Рекурсивний виклик для підпапок
                new_prefix = prefix + ("  " if is_last else "┃ ")
                list_directory_contents(item, new_prefix)
            else:
                print(f"{prefix}{connector}{Fore.GREEN}📜 {item.name}{Style.RESET_ALL}")
                
    except PermissionError:
        print(f"{prefix}┗ {Fore.RED}[Доступ заборонено]")


# ЗАВДАННЯ 4: 

def parse_input(user_input):
    """
    Розбирає введений рядок на команду та аргументи.
    """
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args
    except ValueError:
        return None, None

def add_contact(args, contacts):
    if len(args) < 2:
        return "Error: Give me name and phone please."
    name, phone = args
    contacts[name] = phone
    return "Contact added."

def change_contact(args, contacts):
    if len(args) < 2:
        return "Error: Give me name and phone please."
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        return f"Error: Contact '{name}' not found."

def show_phone(args, contacts):
    if not args:
        return "Error: Enter user name."
    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        return f"Error: Contact '{name}' not found."

def show_all(contacts):
    if not contacts:
        return "Contact list is empty."
    
    result = []
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)

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
            print(show_all(contacts))

        else:
            print("Invalid command.")





def main():
    contacts = {}
    print(f"{Fore.CYAN}Ласкаво просимо до бота-помічника!")
    
   
    with open("salary_test.txt", "w", encoding="utf-8") as f:
        f.write("Alex Korp,3000\nNikita Borisenko,2000\nSitarama Raju,1000")
    
    with open("cats_test.txt", "w", encoding="utf-8") as f:
        f.write("60b90c1c1,Tayson,3\n60b90c242,Vika,1\n60b90c2e3,Barsik,2")

    while True:
        user_input = input("\nВведіть команду: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{Fore.MAGENTA}До побачення!")
            break
        
        elif command == "hello":
            print("Чим я можу допомогти?")
        
        elif command == "add":
            print(add_contact(args, contacts))
            
        elif command == "change":
            print(change_contact(args, contacts))
            
        elif command == "phone":
            print(show_phone(args, contacts))
            
        elif command == "all":
            if not contacts:
                print("Список контактів порожній.")
            for name, phone in contacts.items():
                print(f"{Fore.CYAN}{name}: {phone}")
        
        # Відповіді на завдання 
        elif command == "test_salary":
            total, avg = total_salary("salary_test.txt")
            print(f"Сума: {total}, Середня: {avg}")
            
        elif command == "test_cats":
            pprint.pprint(get_cats_info("cats_test.txt"), sort_dicts=False)
            
        elif command == "test_dir":
            print(f"{Fore.CYAN}Структура поточної папки:")
            list_directory_contents(Path("."))
            
        elif command is None:
            continue
            
        else:
            print(f"{Fore.RED}Невідома команда.")

if __name__ == "__main__":
    main()