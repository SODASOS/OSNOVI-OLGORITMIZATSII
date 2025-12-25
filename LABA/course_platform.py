# Импорт необходимых модулей
import json                     # Для сериализации/десериализации данных в формат JSON
from datetime import datetime   # Для работы с датами и вычисления продолжительности курса
from typing import List, Optional  # Для аннотаций типов (улучшает читаемость и поддержку IDE)

# === ПОЛЬЗОВАТЕЛЬСКОЕ ИСКЛЮЧЕНИЕ ===

class CourseFullError(Exception):
    """Исключение, возникающее при попытке добавить студента на заполненный курс."""
    pass  # Пустой класс, наследуется от базового Exception


# === БАЗОВЫЙ КЛАСС COURSE ===

class Course:
    """Базовый класс, описывающий учебный курс."""

    def __init__(
        self,
        title: str,           # Название курса
        instructor: str,      # Имя преподавателя
        start_date: str,      # Дата начала (в формате "YYYY-MM-DD")
        end_date: str,        # Дата окончания
        max_students: int     # Максимальное число студентов
    ) -> None:
        # Приватные атрибуты (инкапсуляция)
        self.__title = title
        self.__instructor = instructor
        self.__start_date = start_date
        self.__end_date = end_date
        self.__max_students = max_students
        self.__students: List[str] = []  # Список зачисленных студентов

    # === СВОЙСТВА (GETTER'ы) ДЛЯ ДОСТУПА К ПРИВАТНЫМ АТРИБУТАМ ===

    @property
    def title(self) -> str:
        """Возвращает название курса."""
        return self.__title

    @property
    def instructor(self) -> str:
        """Возвращает имя преподавателя."""
        return self.__instructor

    @property
    def start_date(self) -> str:
        """Возвращает дату начала курса."""
        return self.__start_date

    @property
    def end_date(self) -> str:
        """Возвращает дату окончания курса."""
        return self.__end_date

    @property
    def max_students(self) -> int:
        """Возвращает максимальное количество студентов."""
        return self.__max_students

    @property
    def students(self) -> List[str]:
        """Возвращает копию списка студентов (для безопасного доступа)."""
        return self.__students.copy()  # или просто self.__students, если разрешено прямое чтение

    # === МЕТОДЫ ===

    def add_student(self, name: str) -> None:
        """Добавляет студента на курс. Вызывает CourseFullError, если курс заполнен."""
        if len(self.__students) >= self.__max_students:
            raise CourseFullError(f"Course '{self.__title}' is full.")
        self.__students.append(name)

    def completion_rate(self) -> float:
        """Возвращает процент заполненности курса (от 0.0 до 100.0)."""
        if self.__max_students == 0:
            return 0.0
        return (len(self.__students) / self.__max_students) * 100

    def duration_days(self) -> int:
        """Вычисляет продолжительность курса в днях. Требует корректный формат даты."""
        try:
            start = datetime.strptime(self.__start_date, "%Y-%m-%d")
            end = datetime.strptime(self.__end_date, "%Y-%m-%d")
            return (end - start).days
        except ValueError as e:
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.") from e

    def __str__(self) -> str:
        """Возвращает человекочитаемое строковое представление курса."""
        return (
            f"Course: {self.__title}\n"
            f"Instructor: {self.__instructor}\n"
            f"Dates: {self.__start_date} - {self.__end_date} ({self.duration_days()} days)\n"
            f"Students: {len(self.__students)}/{self.__max_students}"
        )

    def to_dict(self) -> dict:
        """Преобразует объект курса в словарь для сериализации в JSON."""
        return {
            "type": self.__class__.__name__,      # Сохраняем тип курса для восстановления
            "title": self.__title,
            "instructor": self.__instructor,
            "start_date": self.__start_date,
            "end_date": self.__end_date,
            "max_students": self.__max_students,
            "students": self.__students,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Course":
        """Создаёт объект курса из словаря (для десериализации из JSON)."""
        course_type = data.get("type")
        # Воссоздаём объект нужного подкласса в зависимости от типа
        if course_type == "ProgrammingCourse":
            course = ProgrammingCourse(
                title=data["title"],
                instructor=data["instructor"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                max_students=data["max_students"],
                language=data.get("language", "")
            )
        elif course_type == "DesignCourse":
            course = DesignCourse(
                title=data["title"],
                instructor=data["instructor"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                max_students=data["max_students"],
                software=data.get("software", "")
            )
        elif course_type == "ScienceCourse":
            course = ScienceCourse(
                title=data["title"],
                instructor=data["instructor"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                max_students=data["max_students"],
                field=data.get("field", "")
            )
        else:
            # Если тип неизвестен — создаём базовый Course
            course = Course(
                title=data["title"],
                instructor=data["instructor"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                max_students=data["max_students"]
            )
        # Восстанавливаем список студентов (он не задаётся в конструкторе)
        course._Course__students = data.get("students", [])
        return course


# === НАСЛЕДУЕМЫЕ КЛАССЫ ===

class ProgrammingCourse(Course):
    """Курс по программированию с указанием языка программирования."""

    def __init__(
        self,
        title: str,
        instructor: str,
        start_date: str,
        end_date: str,
        max_students: int,
        language: str
    ) -> None:
        # Вызываем конструктор родительского класса
        super().__init__(title, instructor, start_date, end_date, max_students)
        self.__language = language  # Дополнительный приватный атрибут

    @property
    def language(self) -> str:
        """Возвращает язык программирования курса."""
        return self.__language

    def __str__(self) -> str:
        """Расширяет строковое представление базового класса информацией о языке."""
        base = super().__str__()
        return f"{base}\nProgramming language: {self.__language}"


class DesignCourse(Course):
    """Курс по дизайну с указанием используемого программного обеспечения."""

    def __init__(
        self,
        title: str,
        instructor: str,
        start_date: str,
        end_date: str,
        max_students: int,
        software: str
    ) -> None:
        super().__init__(title, instructor, start_date, end_date, max_students)
        self.__software = software

    @property
    def software(self) -> str:
        """Возвращает ПО, используемое на курсе."""
        return self.__software

    def __str__(self) -> str:
        """Расширяет строковое представление базового класса информацией о ПО."""
        base = super().__str__()
        return f"{base}\nSoftware: {self.__software}"


class ScienceCourse(Course):
    """Научный курс с указанием области науки."""

    def __init__(
        self,
        title: str,
        instructor: str,
        start_date: str,
        end_date: str,
        max_students: int,
        field: str
    ) -> None:
        super().__init__(title, instructor, start_date, end_date, max_students)
        self.__field = field

    @property
    def field(self) -> str:
        """Возвращает научную область курса."""
        return self.__field

    def __str__(self) -> str:
        """Расширяет строковое представление базового класса информацией о научной области."""
        base = super().__str__()
        return f"{base}\nScientific field: {self.__field}"


# === КЛАСС PLATFORM — ОБРАЗОВАТЕЛЬНАЯ ПЛАТФОРМА ===

class Platform:
    """Класс для управления коллекцией курсов на образовательной платформе."""

    def __init__(self, name: str) -> None:
        self.name = name  # Название платформы (публичный атрибут)
        self.__courses: List[Course] = []  # Приватный список курсов

    def add_course(self, course: Course) -> None:
        """Добавляет курс в список платформы."""
        self.__courses.append(course)

    def remove_course(self, title: str) -> bool:
        """Удаляет курс по названию. Возвращает True, если курс найден и удалён."""
        for i, course in enumerate(self.__courses):
            if course.title == title:
                del self.__courses[i]
                return True
        return False

    def find_course(self, title: str) -> Optional[Course]:
        """Находит курс по названию. Возвращает объект курса или None."""
        for course in self.__courses:
            if course.title == title:
                return course
        return None

    def get_all_courses(self) -> List[Course]:
        """Возвращает копию списка всех курсов (защита от внешнего изменения)."""
        return self.__courses.copy()

    def get_most_popular(self, n: int = 3) -> List[Course]:
        """Возвращает n самых популярных курсов по количеству студентов (по убыванию)."""
        return sorted(self.__courses, key=lambda c: len(c.students), reverse=True)[:n]

    def save_to_json(self, filename: str) -> None:
        """Сохраняет все курсы платформы в JSON-файл с читаемым форматированием."""
        data = [course.to_dict() for course in self.__courses]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename: str) -> None:
        """Загружает курсы из JSON-файла и заменяет текущий список."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Преобразуем каждый словарь обратно в объект курса
            self.__courses = [Course.from_dict(item) for item in data]
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except json.JSONDecodeError:
            print(f"Error reading JSON from {filename}.")

    def __str__(self) -> str:
        """Возвращает краткое описание платформы."""
        return f"Platform: {self.name}, courses: {len(self.__courses)}"
