import os
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from dotenv import load_dotenv

from backend import models
from backend import schemas


app = FastAPI()

# dependency


def get_db():
    load_dotenv('.env')
    engine = create_engine(os.environ.get('DB_URL'))

    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@app.post("/institutions", response_model=schemas.Institution)
def create_institution(institution: schemas.InstitutionCreate, db: Session = Depends(get_db)):
    institution = models.Institution(**institution.dict())
    db.add(institution)
    db.commit()
    db.refresh(institution)
    return schemas.Institution.from_orm(institution)


@app.post("/admins")
def create_admin(admin: schemas.UserCreate, db: Session = Depends(get_db)):
    admin = models.User(**admin.dict())
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return schemas.User.from_orm(admin)


@app.put("/admins/{admin_id}/institution")
def assign_admin_to_institution(admin_id: int, institution_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.User).filter(
        models.User.userID == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    admin.institutionID = institution_id
    db.commit()
    return {"message": "Admin assigned to the institution successfully"}
