# Импортируем необходимые классы из модуля course_platform:
# - ProgrammingCourse: курс по программированию
# - DesignCourse: курс по дизайну
# - Platform: образовательная платформа для управления курсами
from course_platform import ProgrammingCourse, DesignCourse, Platform

# === СОЗДАНИЕ КУРСОВ ===

# Создаём экземпляр курса по программированию на Python.
# Передаём все обязательные параметры через именованные аргументы.
python_course = ProgrammingCourse(
    title="Python for Beginners",       # Название курса
    instructor="Ivanov I.I.",           # Имя преподавателя
    start_date="2025-01-10",            # Дата начала курса (в формате ГГГГ-ММ-ДД)
    end_date="2025-04-10",              # Дата окончания курса
    max_students=30,                    # Максимальное число студентов на курсе
    language="Python"                   # Язык программирования (доп. атрибут для ProgrammingCourse)
)

# Создаём экземпляр курса по UI/UX дизайну.
design_course = DesignCourse(
    title="UI/UX Design",               # Название курса
    instructor="Petrova A.S.",          # Имя преподавателя
    start_date="2025-02-01",            # Дата начала
    end_date="2025-05-01",              # Дата окончания
    max_students=25,                    # Максимум студентов
    software="Figma"                    # Программное обеспечение, используемое на курсе
)

# === ДОБАВЛЕНИЕ СТУДЕНТОВ НА КУРСЫ ===

# Добавляем двух конкретных студентов на курс Python вручную.
python_course.add_student("Sidorov Petr")   # Добавление студента по имени
python_course.add_student("Kozlova Anna")   # Добавление ещё одного студента

# Добавляем 10 студентов с именами "Student 1", "Student 2", ..., "Student 10"
# Используем цикл for и f-строку для генерации имён.
for i in range(10):
    python_course.add_student(f"Student {i+1}")  # i+1, чтобы нумерация начиналась с 1

# Добавляем 15 студентов на курс дизайна с именами "Designer 1", ..., "Designer 15"
for i in range(15):
    design_course.add_student(f"Designer {i+1}")

# === СОЗДАНИЕ ПЛАТФОРМЫ И ДОБАВЛЕНИЕ КУРСОВ ===

# Создаём объект образовательной платформы с названием "SuperLearn"
platform = Platform("SuperLearn")

# Добавляем созданные ранее курсы на платформу
platform.add_course(python_course)   # Регистрация курса Python на платформе
platform.add_course(design_course)   # Регистрация курса дизайна на платформе

# === ВЫВОД САМЫХ ПОПУЛЯРНЫХ КУРСОВ ===

# Печатаем заголовок перед списком популярных курсов
print("Most popular courses:")

# Получаем 2 самых популярных курса (по количеству студентов)
# Метод get_most_popular(2) возвращает список из 2 курсов, отсортированных по убыванию числа студентов
for course in platform.get_most_popular(2):
    print(course)  # Вывод полной информации о курсе (благодаря переопределённому __str__)
    # Выводим процент заполненности курса с точностью до 1 знака после запятой
    print(f"Completion rate: {course.completion_rate():.1f}%")
    # Выводим разделительную линию из 40 дефисов для читаемости
    print("-" * 40)

# === СОХРАНЕНИЕ ДАННЫХ В JSON-ФАЙЛ ===

# Сохраняем все курсы платформы в файл platform_data.json в формате JSON
# Метод save_to_json сериализует объекты курсов в словари и записывает их в файл
platform.save_to_json("platform_data.json")

# === ЗАГРУЗКА ДАННЫХ ИЗ JSON-ФАЙЛА ===

# Создаём новую платформу (для демонстрации загрузки данных)
new_platform = Platform("NewSuperLearn")

# Загружаем курсы из ранее сохранённого JSON-файла
# Метод load_from_json читает файл, десериализует данные и воссоздаёт объекты курсов
new_platform.load_from_json("platform_data.json")

# Печатаем заголовок для загруженных данных
print("\nLoaded from JSON:")  # \n добавляет пустую строку перед текстом

# Выводим все курсы, загруженные из JSON
for course in new_platform.get_all_courses():
    print(course)           # Полная информация о курсе
    print("-" * 40)         # Разделитель
