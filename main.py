from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from geojson import Feature, Point
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from shapely.geometry import Point

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base = declarative_base()


class Lake(Base):
    __tablename__ = 'lake'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry('POLYGON'))


# Replace these values with your database connection string
DATABASE_URL = "postgresql://postgres:postgres@localhost/FastAPI"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def lake(name, geom):
    existing_lake = session.query(Lake).filter(Lake.name == name).first()
    if existing_lake is None:
        new_lake = Lake(name=name, geom=geom)
        session.add(new_lake)
        session.commit()
    session.close()
lake(name = "Garde", geom = "POLYGON((1 0,3 0,3 2,1 2,1 0))")
lake(name = 'Orta', geom = "POLYGON((3 0,6 0,6 3,3 3,3 0))")
lake(name = 'Majeur', geom = "POLYGON((0 0,1 0,1 1,0 1,0 0))")
