
#Код написал студент ПГНИУ, ИКНТ, 1 курс, группа ИТ-8, Антипин Дмитрий

from utils import (
    load_students, save_students, insertion_sort, print_students,
    is_valid_name, is_valid_date, is_valid_class
)

DATA_FILE = "students.txt"
students = []

def main():
    global students
    students = load_students(DATA_FILE)

    while True:
        print("="*50)
        print("     Меню управления базой учеников")
        print("="*50)
        print("1. Показать всю базу")
        print("2. Добавить ученика")
        print("3. Удалить ученика")
        print("4. Редактировать ученика")
        print("5. Список по классу + фамилии")
        print("6. Именинники по временам года")
        print("7. Ученики в параллели")
        print("0. Выход")
        print("-"*50)

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("До свидания!")
            break
        elif choice == "1":
            print_students(students, "Вся база учеников")
        elif choice == "2":
            add_student()
        elif choice == "3":
            remove_student()
        elif choice == "4":
            edit_student()
        elif choice == "5":
            list_sorted_by_class_and_surname()
        elif choice == "6":
            list_birthdays_by_season()
        elif choice == "7":
            list_by_grade()
        else:
            print("Неверный выбор. Введите число от 0 до 7.")

def add_student():
    print("--- Добавление нового ученика ---")
    surname = ""
    name = ""
    day, month, year = 0, 0, 0
    class_input = ""
    #Фамилия - только буквы, еще раз ввод при ошибке
    while not surname:
        surname = input("Фамилия: ").strip().title()
        if not is_valid_name(surname):
            print("Ошибка: фамилия должна содержать только буквы и не быть пустой.")
            surname = ""

    #Имя
    while not name:
        name = input("Имя: ").strip().title()
        if not is_valid_name(name):
            print("Ошибка: имя должно содержать только буквы и не быть пустым.")
            name = ""

    #Дата рождения - проверяем, что числа и корректная дата
    while True:
        day_input = input("День рождения: ").strip()
        month_input = input("Месяц рождения (1–12): ").strip()
        year_input = input("Год рождения: ").strip()

        if not (day_input.isdigit() and month_input.isdigit() and year_input.isdigit()):
            print("Ошибка: день, месяц и год должны быть числами.")
            continue 

        day, month, year = int(day_input), int(month_input), int(year_input)

        if not is_valid_date(day, month, year):
            print("Ошибка: некорректная дата. Проверьте диапазоны и високосный год.")
            continue
        break

    #Класс - число и буква (9А, 10Б и т.д.)
    while not class_input:
        class_input = input("Класс (например, 9А): ").strip().upper()
        if not is_valid_class(class_input):
            print("Ошибка: формат класса — число и буква (например, 9А).")
            class_input = ""

    students.append({
        'фамилия': surname,
        'имя': name,
        'дата_рождения': {'день': day, 'месяц': month, 'год': year},
        'класс': class_input
    })
    save_students(students, DATA_FILE)
    print(f"Ученик {surname} {name} успешно добавлен.")

def remove_student():
    print_students(students, "Текущий список учеников")
    if not students:
        return

    idx_input = input("Введите номер ученика для удаления: ").strip()
    if not idx_input.isdigit():
        print("Ошибка: введите число.")
        return

    idx = int(idx_input) - 1
    if idx < 0 or idx >= len(students):
        print("Ошибка: неверный номер.")
        return

    #Удаляем по индексу и сохраняем
    removed = students.pop(idx)
    save_students(students, DATA_FILE)
    print(f"Ученик {removed['фамилия']} {removed['имя']} удалён.")

def edit_student():
    print_students(students, "Текущий список учеников")
    if not students:
        print("Список учеников пуст.")
        return

    #Выбираем номер ученика - повторяем, пока не введут корректный
    while True:
        idx_input = input("Введите номер ученика для редактирования: ").strip()
        if not idx_input.isdigit():
            print("Ошибка: введите число.")
            continue
        idx = int(idx_input) - 1
        if idx < 0 or idx >= len(students):
            print("Ошибка: номер вне диапазона.")
            continue
        break

    s = students[idx]
    print(f"Текущие данные: {s['фамилия']} {s['имя']}, "
          f"{s['дата_рождения']['день']}.{s['дата_рождения']['месяц']}.{s['дата_рождения']['год']}, {s['класс']}")

    print("Введите новые данные (оставьте пустым, чтобы не менять):")

    #Редактируем фамилию, если ввели что-то новое
    new_surname = input(f"Фамилия ({s['фамилия']}): ").strip().title()
    if new_surname:
        while True:
            if is_valid_name(new_surname):
                s['фамилия'] = new_surname
                break
            else:
                print("Ошибка: фамилия должна содержать только буквы.")
                new_surname = input("Введите фамилию ещё раз: ").strip().title()

    #То же для имени
    new_name = input(f"Имя ({s['имя']}): ").strip().title()
    if new_name:
        while True:
            if is_valid_name(new_name):
                s['имя'] = new_name
                break
            else:
                print("Ошибка: имя должно содержать только буквы.")
                new_name = input("Введите имя ещё раз: ").strip().title()

    #Дата рождения - если изменили, проверяем всё заново
    day_input = input(f"День ({s['дата_рождения']['день']}): ").strip()
    month_input = input(f"Месяц ({s['дата_рождения']['месяц']}): ").strip()
    year_input = input(f"Год ({s['дата_рождения']['год']}): ").strip()

    if day_input or month_input or year_input:
        while True:
            if not (day_input.isdigit() and month_input.isdigit() and year_input.isdigit()):
                print("Ошибка: день, месяц, год должны быть числами.")
            else:
                day, month, year = int(day_input), int(month_input), int(year_input)
                if is_valid_date(day, month, year):
                    s['дата_рождения']['день'] = day
                    s['дата_рождения']['месяц'] = month
                    s['дата_рождения']['год'] = year
                    break
                else:
                    print("Ошибка: некорректная дата.")
            day_input = input("День: ").strip()
            month_input = input("Месяц: ").strip()
            year_input = input("Год: ").strip()

    #Класс
    new_class = input(f"Класс ({s['класс']}): ").strip().upper()
    if new_class:
        while True:
            if is_valid_class(new_class):
                s['класс'] = new_class
                break
            else:
                print("Ошибка: формат класса — число и буква (например, 9А).")
                new_class = input("Введите класс ещё раз: ").strip().upper()

    save_students(students, DATA_FILE)
    print("Данные ученика успешно обновлены.")

def list_sorted_by_class_and_surname():
    #Ключ сортировки - сначала по классу (число, потом буква) потом по фамилии
    def key(s):
        class_num = int(s['класс'][:-1])
        class_letter = s['класс'][-1]
        return (class_num, class_letter, s['фамилия'])
    sorted_list = insertion_sort(students.copy(), key)
    print_students(sorted_list, "1. Список по классу + фамилии")

def list_birthdays_by_season():
    #Определяем в какое время года какой месяц
    seasons = {
        1: "Зима", 2: "Зима", 3: "Весна", 4: "Весна", 5: "Весна",
        6: "Лето", 7: "Лето", 8: "Лето", 9: "Осень", 10: "Осень",
        11: "Осень", 12: "Зима"
    }
    print("Выберите время года:")
    print("1 — Весна (март, апрель, май)")
    print("2 — Лето (июнь, июль, август)")
    print("3 — Осень (сентябрь, октябрь, ноябрь)")
    print("4 — Зима (декабрь, январь, февраль)")

    choice = input("Ваш выбор (1-4): ").strip()
    if not choice.isdigit() or choice not in "1234":
        print("Ошибка: введите число от 1 до 4.")
        return

    target_season = {
        "1": "Весна",
        "2": "Лето",
        "3": "Осень",
        "4": "Зима"
    }[choice]

    months = [m for m, s in seasons.items() if s == target_season]
    season_students = [s for s in students if s['дата_рождения']['месяц'] in months]

    #Сортируем - сначала по месяцу, потом по дню, потом по фамилии
    def key(s):
        b = s['дата_рождения']
        return (b['месяц'], b['день'], s['фамилия'])

    sorted_list = insertion_sort(season_students, key)
    print_students(sorted_list, f"2. Именинники в {target_season.lower()}: по месяцу → дню → фамилии")

def list_by_grade():
    #Фильтрация по параллели (например, все 9-классники)
    grade_input = input("Введите номер класса (8, 9, 10, 11): ").strip()
    if not grade_input.isdigit():
        print("Ошибка: введите число.")
        return
    grade = int(grade_input)
    if grade not in [8, 9, 10, 11]:
        print("Ошибка: класс должен быть 8, 9, 10 или 11.")
        return

    grade_students = [s for s in students if int(s['класс'][:-1]) == grade]
    if not grade_students:
        print(f"Нет учеников {grade} класса.")
        return

    def key(s):
        b = s['дата_рождения']
        return (b['месяц'], b['день'], s['фамилия'])

    sorted_list = insertion_sort(grade_students, key)
    print_students(sorted_list, f"3. Ученики {grade} класса: по месяцу → дню → фамилии")

if __name__ == "__main__":
    main()

