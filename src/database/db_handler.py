from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Job
from config.config import Config

engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)

def save_job(job_data):
    existing_job = session.query(Job).filter(Job.url == job_data["url"]).first()
    if not existing_job:
        new_job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            url=job_data["url"]
        )
        session.add(new_job)
        session.commit()