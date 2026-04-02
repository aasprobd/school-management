from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, get_db

from routers import auth, notices, academic, users, attendance, timetable, materials, homework, staff, library, misc, admission, finance, payroll, inventory, hr, logistics, cms, notifications, analytics

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ESMS - Global International School & College API")

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(notices.router)
app.include_router(academic.router)
app.include_router(users.router)
app.include_router(attendance.router)
app.include_router(timetable.router)
app.include_router(materials.router)
app.include_router(homework.router)
app.include_router(staff.router)
app.include_router(library.router)
app.include_router(misc.router)
app.include_router(admission.router)
app.include_router(finance.router)
app.include_router(payroll.router)
app.include_router(inventory.router)
app.include_router(hr.router)
app.include_router(logistics.router)
app.include_router(cms.router)
app.include_router(notifications.router)
app.include_router(analytics.router)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred", "detail": str(exc)},
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to ESMS API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
