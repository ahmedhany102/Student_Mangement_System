class Student:
    def __init__(self, sid: str, name: str, age: int, grade: int):
        self.id = sid
        self.name = name
        self.age = age
        self.grade = grade

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
        }

    @staticmethod
    def from_dict(data: dict) -> "Student":
        return Student(
            sid=data["id"],
            name=data["name"],
            age=int(data["age"]),
            grade=int(data["grade"]),
        )
