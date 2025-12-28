from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import Patient, PatientCreate, PatientUpdate, User, UserCreate
from typing import List
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="Patient Management System")

# Secret key for JWT tokens
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Mock database (replace with real database in production)
patients_db = {}
users_db = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication functions
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in users_db:
            raise credentials_exception
        return users_db[username]
    except jwt.PyJWTError:
        raise credentials_exception

# Authentication endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user.password != form_data.password:  # In production, use proper password hashing
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# User management endpoints
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    users_db[user.username] = user
    return user

# Patient management endpoints
@app.post("/patients/", response_model=Patient)
async def create_patient(patient: PatientCreate, current_user: User = Depends(get_current_user)):
    if patient.id in patients_db:
        raise HTTPException(status_code=400, detail="Patient ID already registered")
    patients_db[patient.id] = patient
    return patient

@app.get("/patients/", response_model=List[Patient])
async def read_patients(skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)):
    return list(patients_db.values())[skip : skip + limit]

@app.get("/patients/{patient_id}", response_model=Patient)
async def read_patient(patient_id: str, current_user: User = Depends(get_current_user)):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients_db[patient_id]

@app.put("/patients/{patient_id}", response_model=Patient)
async def update_patient(
    patient_id: str, patient: PatientUpdate, current_user: User = Depends(get_current_user)
):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    update_data = patient.dict(exclude_unset=True)
    stored_patient = patients_db[patient_id]
    for field, value in update_data.items():
        setattr(stored_patient, field, value)
    return stored_patient

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt