from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import DB_CONFIG
from database import OracleDatabase
from metadata_loader import MetadataLoader
from metadata_index import MetadataIndex
from parser import QueryParser
from sql_builder import SQLBuilder

# ----------------------------------------
# Initialize FastAPI
# ----------------------------------------

app = FastAPI(title="Enterprise NL2SQL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Later change this to your React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# Load backend once
# ----------------------------------------

db = OracleDatabase(DB_CONFIG)
db.connect()

loader = MetadataLoader(db)
metadata = loader.load_metadata()

index = MetadataIndex(metadata)
index.build()

parser = QueryParser(index)

builder = SQLBuilder(metadata)


# ----------------------------------------
# Request Model
# ----------------------------------------

class QueryRequest(BaseModel):
    question: str


# ----------------------------------------
# Health Check
# ----------------------------------------

@app.get("/")
def home():

    return {

        "status": "running",

        "project": "Enterprise NL2SQL"

    }


# ----------------------------------------
# Query Endpoint
# ----------------------------------------

@app.post("/query")
def query(request: QueryRequest):

    parsed = parser.parse(request.question)

    sql = builder.build(parsed)

    rows = db.execute(sql)

    return {

        "question": request.question,

        "parsed": parsed,

        "sql": sql,

        "rows": rows

    }