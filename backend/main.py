from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
import psycopg
from psycopg import rows
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

# --- CONFIGURAZIONE SICUREZZA ---
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# Questo serve a FastAPI per capire da dove recuperare il token nelle rotte protette
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(name="DatiCuoreAPI")

# --- CORS CONFIGURATION ---
origins = ["https://itzmarcu.github.io"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_URL = os.getenv("DATABASE_URL")

def db_connect(): 
    return psycopg.connect(DB_URL)

# Modello Pydantic per ricevere i dati di registrazione (JSON) dal frontend
class UserRegister(BaseModel):
    username: str
    password: str

# --- FUNZIONI UTILI PER AUTH ---
def genera_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verifica_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token non valido o scaduto",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_utente: int = payload.get("id_utente")
        if id_utente is None:
            raise credentials_exception
        return id_utente  # Restituiamo direttamente l'id dell'utente loggato
    except JWTError:
        raise credentials_exception

# --- ROTTA DI REGISTRAZIONE ---
@app.post("/registrati", status_code=status.HTTP_201_CREATED)
def registrati(user_data: UserRegister):
    # Generiamo l'hash sicuro della password in tempo reale
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(user_data.password.encode('utf-8'), salt).decode('utf-8')

    conn = db_connect()
    cursor = conn.cursor()
    QUERY = 'INSERT INTO Utenti (username, password_hash) VALUES (%s, %s)'
    
    try:
        cursor.execute(QUERY, (user_data.username, password_hash))
        conn.commit()
        cursor.close()
        conn.close()
        return {"messaggio": "Utente registrato con successo!"}
    except psycopg.errors.UniqueViolation:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Username già esistente.")
    except Exception as e:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Errore del database: {e}")

# --- ROTTA DI LOGIN ---
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = db_connect()
    cursor = conn.cursor(row_factory=rows.dict_row)
    QUERY = 'SELECT id_utente, password_hash FROM Utenti WHERE username = %s'
    
    cursor.execute(QUERY, (form_data.username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o Password errati",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    password_corretta = bcrypt.checkpw(
        form_data.password.encode('utf-8'), 
        user["password_hash"].encode('utf-8')
    )

    if not password_corretta:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o Password errati",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Inseriamo sia lo username (sub) che l'id_utente all'interno del token JWT
    access_token = genera_token(data={"sub": form_data.username, "id_utente": user["id_utente"]})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROTTE PROTETTE (Filtrate per id_utente) ---
@app.get("/utente/me")
def get_current_user(id_utente: int = Depends(verifica_token)):
    conn = db_connect()
    cursor = conn.cursor(row_factory=rows.dict_row)
    QUERY = "SELECT username FROM utenti WHERE id_utente = %s"

    try:
        cursor.execute(QUERY, (id_utente,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            raise HTTPException(status_code=404, detail="Errore: utente non trovato!")
        
        return {"username": user["username"]}
    
    except Exception as e: 
        cursor.close()
        conn.close()

        raise HTTPException(status_code=500, detail=f"Errore: {e}")

@app.get("/ottieni-dati")
def get_data(id_utente: int = Depends(verifica_token)):
    conn = db_connect()
    cursor = conn.cursor(row_factory=rows.dict_row)
    # Mostra solo i dati appartenenti all'utente che ha fatto la richiesta
    QUERY = 'SELECT * FROM DatiCuore WHERE id_utente = %s'

    try: 
        cursor.execute(QUERY, (id_utente,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e: 
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Errore: {e}")
    
@app.post("/registra-dati")
def load_data(data: str = None, frequenza_cardiaca: int = None, pressione: int = None, saturazione: int = None, id_utente: int = Depends(verifica_token)):
    if not any([data, frequenza_cardiaca, pressione, saturazione]):
        raise HTTPException(status_code=400, detail="Error: Dati non forniti!")
    
    conn = db_connect()
    cursor = conn.cursor()
    # Inseriamo l'id_utente come chiave esterna per blindare il record
    QUERY = 'INSERT INTO DatiCuore ("data", frequenza_cardiaca, pressione, saturazione, id_utente) VALUES (%s, %s, %s, %s, %s)'

    try: 
        cursor.execute(QUERY, (data, frequenza_cardiaca, pressione, saturazione, id_utente))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e: 
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Errore: {e}")

    return {"messaggio": "status_code=201, Inserimento riuscito con successo!"}