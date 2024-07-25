from sqlalchemy import create_engine , DATE, Integer, Column, String, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib import parse
from sqlalchemy import URL 
from sqlConnect import connection_url




engine = create_engine(connection_url, echo=True)
Base = declarative_base()


class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True , autoincrement=True) 
    jobTitle = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(String(50), nullable=False)
    time = Column(String(50), nullable=False)
    serviceType = Column(String(50), nullable=False)
    location = Column(String(50), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    proposedPayAmount = Column(Float, nullable=False)
    duration = Column(String(50), nullable=False)



class Service(Base):
    __tablename__ = 'services'

    service_id = Column(Integer, primary_key=True, autoincrement=True)  # Assuming a unique identifier for each service
    serviceName = Column(String(50), nullable=False)
    serviceType = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    rate = Column(String(50), nullable=True)  # Freelancer charge rate
    isAvailable = Column(Boolean, nullable=False, default=True)
    location = Column(String(50), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

new_job = Job(
    jobTitle="Example Job",
    description="This is an example job description.",
    date="2024-07-25",
    time="14:00",
    serviceType="Example Service",
    location="Example Location",
    latitude=0.0,
    longitude=0.0,
    proposedPayAmount=100.0,
    duration="2 hours"
)


new_service = Service(
    serviceName="Example Service",
    serviceType="Example Type",
    description="This is an example service description.",
    rate="50",
    isAvailable=True,
    location="Example Location",
    latitude=0.0,
    longitude=0.0,
    rating=5.0
)


session.add(new_job)
session.add(new_service)


session.commit()
