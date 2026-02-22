import sys
import pprint
from pathlib import Path
from typing import Tuple, List, Dict, Optional
from colorama import Fore, Style, init

# Ініціалізація colorama для кольорового виводу в консолі
init(autoreset=True)

# ЗАВДАННЯ 1:

def total_salary(path: str) -> Tuple[float, float]:
    
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

def get_cats_info(path: str) -> List[Dict[str, str]]:

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

def list_directory_contents(path: Path, prefix: str = "") -> None:
    """Рекурсивно виводить структуру директорії у вигляді дерева."""
    try:
        if not path.exists() or not path.is_dir():
            return

        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "┗ " if is_last else "┣ "
            
            if item.is_dir():
                print(f"{prefix}{connector}{Fore.BLUE}📂 {item.name}{Style.RESET_ALL}")
                new_prefix = prefix + ("  " if is_last else "┃ ")
                list_directory_contents(item, new_prefix)
            else:
                print(f"{prefix}{connector}{Fore.GREEN}📜 {item.name}{Style.RESET_ALL}")
                
    except PermissionError:
        print(f"{prefix}┗ {Fore.RED}[Доступ заборонено]")


def parse_input(user_input: str) -> Tuple[Optional[str], List[str]]:
    """Розбирає введений рядок на команду та аргументи."""
    if not user_input.strip():
        return None, []
    
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args


def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """Додає новий контакт до словника."""
    if len(args) < 2:
        return f"{Fore.YELLOW}Error: Give me name and phone please."
    name, phone = args
    contacts[name] = phone
    return f"{Fore.GREEN}Contact added."


def change_contact(args: List[str], contacts: Dict[str, str]) -> str:

    if len(args) < 2:
        return f"{Fore.YELLOW}Error: Give me name and phone please."
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return f"{Fore.GREEN}Contact updated."
    else:
        return f"{Fore.RED}Error: Contact '{name}' not found."


def show_phone(args: List[str], contacts: Dict[str, str]) -> str:

    if not args:
        return f"{Fore.YELLOW}Error: Enter user name."
    name = args[0]
    if name in contacts:
        return f"{Fore.CYAN}{contacts[name]}"
    else:
        return f"{Fore.RED}Error: Contact '{name}' not found."


def show_all(contacts: Dict[str, str]) -> None:

    if not contacts:
        print(f"{Fore.YELLOW}Contact list is empty.")
        return
    
    for name, phone in contacts.items():
        print(f"{Fore.CYAN}{name}: {phone}")


def main() -> None:
    
    contacts: Dict[str, str] = {}
    print(f"{Fore.CYAN}Ласкаво просимо до бота-помічника!")
    
    with open("salary_test.txt", "w", encoding="utf-8") as f:
        f.write("Alex Korp,3000\nNikita Borisenko,2000\nSitarama Raju,1000")
    
    with open("cats_test.txt", "w", encoding="utf-8") as f:
        f.write("60b90c1c1,Tayson,3\n60b90c242,Vika,1\n60b90c2e3,Barsik,2")

    while True:
        user_input = input("\nВведіть команду: ")
        command, args = parse_input(user_input)

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
            show_all(contacts)
        
        # Блок команд для тестування попередніх завдань
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