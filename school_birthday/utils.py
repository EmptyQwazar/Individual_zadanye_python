
#Код написал студент ПГНИУ, ИКНТ, 1 курс, группа ИТ-8, Антипин Дмитрий

#валидаторы
def is_valid_name(text):
    return bool(text) and text.isalpha() and text.strip() == text

def is_valid_date(day, month, year):
    if not all(isinstance(x, int) for x in [day, month, year]):
        return False
    if not (1 <= month <= 12):
        return False
    if not (1 <= day <= 31):
        return False
    if not (1990 <= year <= 2015):
        return False

    if month in [4, 6, 9, 11] and day > 30:
        return False
    if month == 2:
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_day = 29 if is_leap else 28
        if day > max_day:
            return False
    return True

def is_valid_class(class_str):
    if not isinstance(class_str, str) or len(class_str) < 2:
        return False
    class_part = class_str[:-1]
    letter_part = class_str[-1]
    return class_part.isdigit() and letter_part.isalpha()

#работа с students.txt 

def load_students(filename="students.txt"):

    students = []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ОШИБКА: Файл '{filename}' не найден.")
        print("Создайте файл students.txt или поместите файл students.txt в ту же папку, что и программу.")
        exit(1)

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if line.startswith("Фамилия;") or line.startswith("#"):
            continue

        parts = line.split(";")
        if len(parts) != 6:
            print(f"Пропущена строка {i+1}: неверный формат (не 6 полей)")
            continue

        surname, name, day_str, month_str, year_str, class_name = parts

        if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
            print(f"Пропущена строка {i+1}: день/месяц/год должны быть числами")
            continue

        day, month, year = int(day_str), int(month_str), int(year_str)

        if not is_valid_name(surname):
            print(f"Пропущена строка {i+1}: некорректная фамилия — '{surname}'")
            continue
        if not is_valid_name(name):
            print(f"Пропущена строка {i+1}: некорректное имя — '{name}'")
            continue
        if not is_valid_date(day, month, year):
            print(f"Пропущена строка {i+1}: некорректная дата — {day}.{month}.{year}")
            continue
        if not is_valid_class(class_name):
            print(f"Пропущена строка {i+1}: некорректный класс — '{class_name}'")
            continue

        students.append({
            'фамилия': surname,
            'имя': name,
            'дата_рождения': {'день': day, 'месяц': month, 'год': year},
            'класс': class_name
        })

    if not students:
        print("Внимание: загружено 0 учеников. Проверьте формат файла.")
    else:
        print(f"Успешно загружено {len(students)} учеников из {filename}")

    return students

#сохранение списка
def save_students(students, filename="students.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Фамилия;Имя;День;Месяц;Год;Класс")
            for s in students:
                b = s['дата_рождения']
                line = f"{s['фамилия']};{s['имя']};{b['день']};{b['месяц']};{b['год']};{s['класс']}"
                f.write(line)
        print("Данные сохранены в students.txt")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

#сортировка вставками
def insertion_sort(arr, key_func):
    result = arr.copy()
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        try:
            key_current = key_func(current)
        except:
            continue
        while j >= 0:
            try:
                key_prev = key_func(result[j])
            except:
                j -= 1
                continue
            if key_current >= key_prev:
                break
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result

#вывод списка
def print_students(lst, title="Список учеников"):
    if not isinstance(lst, list) or len(lst) == 0:
        print("Список пуст.")
        return

    print(f"{title}")
    print("-" * 100)
    print(f"{'№':<3} {'Фамилия':<12} {'Имя':<12} {'Дата рождения':<15} {'Класс':<7}")
    print("-" * 100)

    for idx, s in enumerate(lst, 1):
        if not isinstance(s, dict):
            continue
        surname = s.get('фамилия', '???')
        name = s.get('имя', '???')
        b = s.get('дата_рождения', {})
        day = b.get('день', '?')
        month = b.get('месяц', '?')
        year = b.get('год', '?')
        class_name = s.get('класс', '???')

        try:
            birth = f"{int(day):02d}.{int(month):02d}.{int(year)}"
        except:
            birth = "???.???.????"

        print(f"{idx:<3} {str(surname):<12} {str(name):<12} {birth:<15} {str(class_name):<7}")
    print("-" * 100)

