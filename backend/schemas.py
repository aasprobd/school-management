from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str = "student"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class NoticeBase(BaseModel):
    title: str
    content: str

class NoticeCreate(NoticeBase):
    pass

class Notice(NoticeBase):
    id: int
    created_at: datetime
    author_id: int

    class Config:
        from_attributes = True

class AcademicClassBase(BaseModel):
    name: str
    section: str
    grade: str

class AcademicClassCreate(AcademicClassBase):
    pass

class AcademicClass(AcademicClassBase):
    id: int
    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    title: str
    code: str

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int
    class Config:
        from_attributes = True

class TeacherBase(BaseModel):
    employee_id: str
    specialization: str
    experience_years: int

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    admission_number: str
    grade_level: str
    parent_contact: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    student_id: int
    class_id: int
    date: datetime
    status: str

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    class Config:
        from_attributes = True

class ExamBase(BaseModel):
    title: str
    description: str
    exam_date: datetime
    class_id: int

class ExamCreate(ExamBase):
    pass

class Exam(ExamBase):
    id: int
    class Config:
        from_attributes = True

class GradeBase(BaseModel):
    student_id: int
    exam_id: int
    marks_obtained: int
    grade_letter: str
    gpa: float

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    id: int
    class Config:
        from_attributes = True

class TimetableBase(BaseModel):
    class_id: int
    subject_id: int
    teacher_id: int
    day_of_week: str
    start_time: str
    end_time: str

class TimetableCreate(TimetableBase):
    pass

class Timetable(TimetableBase):
    id: int
    class Config:
        from_attributes = True

class HomeworkBase(BaseModel):
    title: str
    description: str
    due_date: datetime
    class_id: int
    subject_id: int

class HomeworkCreate(HomeworkBase):
    pass

class Homework(HomeworkBase):
    id: int
    teacher_id: int
    class Config:
        from_attributes = True

class SubmissionBase(BaseModel):
    homework_id: int
    content_url: str

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    student_id: int
    submitted_at: datetime
    marks: Optional[int]
    feedback: Optional[str]
    class Config:
        from_attributes = True

class LeaveRequestBase(BaseModel):
    start_date: datetime
    end_date: datetime
    reason: str

class LeaveRequest(LeaveRequestBase):
    id: int
    user_id: int
    status: str
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    total_copies: int

class Book(BookBase):
    id: int
    available_copies: int
    class Config:
        from_attributes = True

class EventBase(BaseModel):
    title: str
    description: str
    event_date: datetime

class Event(EventBase):
    id: int
    class Config:
        from_attributes = True

class LabEquipmentBase(BaseModel):
    name: str
    condition: str
    last_inspected: datetime

class LabEquipment(LabEquipmentBase):
    id: int
    class Config:
        from_attributes = True

class ActivityLogBase(BaseModel):
    student_id: int
    activity_name: str
    date: datetime

class ActivityLog(ActivityLogBase):
    id: int
    class Config:
        from_attributes = True

class ClubBase(BaseModel):
    name: str
    description: str
    lead_teacher_id: int

class Club(ClubBase):
    id: int
    class Config:
        from_attributes = True

class DisciplinaryRecordBase(BaseModel):
    student_id: int
    incident_description: str
    action_taken: str

class DisciplinaryRecord(DisciplinaryRecordBase):
    id: int
    date: datetime
    class Config:
        from_attributes = True

class AdmissionApplicationBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    previous_school: str
    grade_applied: str

class AdmissionApplication(AdmissionApplicationBase):
    id: int
    merit_score: int
    status: str
    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    student_id: int
    amount: int
    type: str
    due_date: datetime

class Invoice(InvoiceBase):
    id: int
    status: str
    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    invoice_id: int
    amount: int
    method: str
    transaction_id: str

class Payment(PaymentBase):
    id: int
    payment_date: datetime
    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    category: str
    description: str
    amount: int

class Expense(ExpenseBase):
    id: int
    date: datetime
    class Config:
        from_attributes = True

class PayrollBase(BaseModel):
    user_id: int
    amount: int
    month: int
    year: int

class Payroll(PayrollBase):
    id: int
    status: str
    class Config:
        from_attributes = True

class InventoryItemBase(BaseModel):
    name: str
    quantity: int
    unit_price: int

class InventoryItem(InventoryItemBase):
    id: int
    class Config:
        from_attributes = True

class ScholarshipBase(BaseModel):
    student_id: int
    discount_percentage: int
    reason: str

class Scholarship(ScholarshipBase):
    id: int
    class Config:
        from_attributes = True

class AuditLog(BaseModel):
    id: int
    action: str
    user_id: int
    details: str
    timestamp: datetime
    class Config:
        from_attributes = True

class StaffAppraisalBase(BaseModel):
    staff_id: int
    score: int
    comments: str

class StaffAppraisal(StaffAppraisalBase):
    id: int
    appraisal_date: datetime
    class Config:
        from_attributes = True

class NotificationBase(BaseModel):
    user_id: int
    message: str

class Notification(NotificationBase):
    id: int
    is_read: bool
    timestamp: datetime
    class Config:
        from_attributes = True

class TransportRouteBase(BaseModel):
    route_name: str
    stops: str
    vehicle_no: str

class TransportRoute(TransportRouteBase):
    id: int
    class Config:
        from_attributes = True

class PageContentBase(BaseModel):
    slug: str
    title: str
    body: str

class PageContent(PageContentBase):
    id: int
    class Config:
        from_attributes = True

class LessonPlanBase(BaseModel):
    subject_id: int
    topic: str
    content: str
    week_number: int

class LessonPlan(LessonPlanBase):
    id: int
    teacher_id: int
    class Config:
        from_attributes = True

class BehaviorRecordBase(BaseModel):
    student_id: int
    category: str
    details: str

class BehaviorRecord(BehaviorRecordBase):
    id: int
    recorded_at: datetime
    class Config:
        from_attributes = True
