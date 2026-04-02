from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True)

    # Relationships
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)
    student_profile = relationship("Student", back_populates="user", uselist=False)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    employee_id = Column(String, unique=True, index=True)
    specialization = Column(String)
    experience_years = Column(Integer)
    
    user = relationship("User", back_populates="teacher_profile")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    admission_number = Column(String, unique=True, index=True)
    grade_level = Column(String)
    parent_contact = Column(String)
    
    user = relationship("User", back_populates="student_profile")

class AcademicClass(Base):
    __tablename__ = "academic_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    section = Column(String)
    grade = Column(String)

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    code = Column(String, unique=True)

class Notice(Base):
    __tablename__ = "notices"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"))

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    class_id = Column(Integer, ForeignKey("academic_classes.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String) # Present, Absent, Late

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    exam_date = Column(DateTime)
    class_id = Column(Integer, ForeignKey("academic_classes.id"))

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    marks_obtained = Column(Integer)
    grade_letter = Column(String)
    gpa = Column(Integer)

class Timetable(Base):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("academic_classes.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    day_of_week = Column(String)
    start_time = Column(String)
    end_time = Column(String)

class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    due_date = Column(DateTime)
    class_id = Column(Integer, ForeignKey("academic_classes.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    homework_id = Column(Integer, ForeignKey("homework.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    content_url = Column(String) # Link to uploaded file
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    marks = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    reason = Column(Text)
    status = Column(String, default="pending") # pending, approved, rejected

class Alumni(Base):
    __tablename__ = "alumni"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    graduation_year = Column(Integer)
    current_occupation = Column(String)
    contact_info = Column(String)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(String, unique=True)
    total_copies = Column(Integer)
    available_copies = Column(Integer)

class BorrowLog(Base):
    __tablename__ = "borrow_logs"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    borrow_date = Column(DateTime, default=datetime.datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    event_date = Column(DateTime)

class LabEquipment(Base):
    __tablename__ = "lab_equipment"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    condition = Column(String) # Working, Maintenance, Broken
    last_inspected = Column(DateTime)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    activity_name = Column(String)
    date = Column(DateTime)

class Club(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    lead_teacher_id = Column(Integer, ForeignKey("teachers.id"))

class DisciplinaryRecord(Base):
    __tablename__ = "disciplinary_records"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    incident_description = Column(Text)
    action_taken = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)

class AdmissionApplication(Base):
    __tablename__ = "admission_applications"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    previous_school = Column(String)
    grade_applied = Column(String)
    merit_score = Column(Integer, default=0)
    status = Column(String, default="applied") # applied, review, interview, admitted, rejected

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    amount = Column(Integer)
    type = Column(String) # Admission, Monthly, Special
    due_date = Column(DateTime)
    status = Column(String, default="unpaid") # unpaid, paid, overdue

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    amount = Column(Integer)
    method = Column(String) # Stripe, Cash, Bank
    transaction_id = Column(String, unique=True)
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)

class Payroll(Base):
    __tablename__ = "payroll"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    status = Column(String, default="disbursed")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    description = Column(Text)
    amount = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)

class InventoryItem(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Integer)

class Scholarship(Base):
    __tablename__ = "scholarships"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    discount_percentage = Column(Integer)
    reason = Column(String)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Transport(Base):
    __tablename__ = "transport"
    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String)
    monthly_fee = Column(Integer)

class Hostel(Base):
    __tablename__ = "hostels"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String)
    type = Column(String) # AC, Non-AC
    monthly_fee = Column(Integer)

class StaffAppraisal(Base):
    __tablename__ = "staff_appraisals"
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer)
    comments = Column(Text)
    appraisal_date = Column(DateTime, default=datetime.datetime.utcnow)

class TransportRoute(Base):
    __tablename__ = "transport_routes"
    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String)
    stops = Column(Text)
    vehicle_no = Column(String)

class HostelRoom(Base):
    __tablename__ = "hostel_rooms"
    id = Column(Integer, primary_key=True, index=True)
    room_no = Column(String)
    capacity = Column(Integer)
    current_occupancy = Column(Integer, default=0)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    type = Column(String) # Transfer, Character, etc.
    issue_date = Column(DateTime, default=datetime.datetime.utcnow)

class PageContent(Base):
    __tablename__ = "page_content"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    title = Column(String)
    body = Column(Text)

class LessonPlan(Base):
    __tablename__ = "lesson_plans"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    topic = Column(String)
    content = Column(Text)
    week_number = Column(Integer)

class BehaviorRecord(Base):
    __tablename__ = "behavior_records"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    category = Column(String) # Psychological, Disciplinary, Positive
    details = Column(Text)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
