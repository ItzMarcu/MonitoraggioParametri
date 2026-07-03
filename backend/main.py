from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from psycopg import rows
from dotenv import load_dotenv
import os

origins = ["https://itzmarcu.github.io"]
app = FastAPI(name="DatiCuoreAPI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def db_connect(): 
    return psycopg.connect(DB_URL)

@app.get("/ottieni-dati")
def get_data():
    conn = db_connect()
    cursor = conn.cursor(row_factory=rows.dict_row)
    QUERY = "SELECT * FROM DatiCuore"

    try: 
        cursor.execute(QUERY)
        data = cursor.fetchall()
        
        cursor.close()
        conn.close()

        return data
    
    except Exception as e: 
        cursor.close()
        conn.close()

        raise HTTPException(status_code=500, detail=f"Errore: {e}")
    
@app.post("/registra-dati")
def load_data(data: str = None, frequenza_cardiaca: int = None, pressione: int = None, saturazione: int = None):
    if not any([data, frequenza_cardiaca, pressione, saturazione]):
        raise HTTPException(status_code=400, detail="Error: Dati non forniti!")
    
    conn = db_connect()
    cursor = conn.cursor()

    QUERY = """
        INSERT INTO DatiCuore (data, frequenza_cardiaca, pressione, saturazione)
        VALUES (%s, %s, %s, %s)
    """

    try: 
        cursor.execute(QUERY, (data, frequenza_cardiaca, pressione, saturazione))
        conn.commit()
        
        cursor.close()
        conn.close()
    
    except Exception as e: 
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Errore: {e}")

    return {"messaggio": "status_code=201, Inserimento riuscito con successo!"}