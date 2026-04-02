import datetime

class DocumentService:
    @staticmethod
    def generate_certificate_metadata(student_name: str, certificate_type: str):
        return {
            "title": f"{certificate_type.capitalize()} Certificate",
            "student": student_name,
            "institution": "Global International School & College",
            "date": str(datetime.date.today()),
            "status": "Official Record"
        }

    @staticmethod
    def generate_transcript_summary(student_name: str, grades: list):
        total_gpa = sum([g.gpa for g in grades]) / len(grades) if grades else 0
        return {
            "student": student_name,
            "gpa": round(total_gpa, 2),
            "records": [{"subject": g.exam.title, "marks": g.marks_obtained, "grade": g.grade_letter} for g in grades],
            "issued_at": str(datetime.datetime.now())
        }
