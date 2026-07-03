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

load_dotenv()

# --- CONFIGURAZIONE SICUREZZA ---
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # Il login scade dopo 2 ore

# Credenziali caricate dal .env o da Render
MY_USERNAME = os.getenv("APP_USERNAME", "admin")
MY_PASSWORD_HASH = os.getenv("APP_PASSWORD_HASH")

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
        username: str = payload.get("sub")
        if username != MY_USERNAME:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# --- ROTTA DI LOGIN (Richiesta da login.html) ---
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not MY_PASSWORD_HASH:
        raise HTTPException(status_code=500, detail="Errore di configurazione del server (Hash mancante)")
        
    # Verifica della password usando bcrypt nativo
    password_corretta = bcrypt.checkpw(
        form_data.password.encode('utf-8'), 
        MY_PASSWORD_HASH.encode('utf-8')
    )

    if form_data.username != MY_USERNAME or not password_corretta:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o Password errati",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = genera_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROTTE PROTEGGIUTE (Aggiunto Depends(verifica_token)) ---

@app.get("/ottieni-dati")
def get_data(username: str = Depends(verifica_token)):
    conn = db_connect()
    cursor = conn.cursor(row_factory=rows.dict_row)
    QUERY = 'SELECT * FROM DatiCuore'

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
def load_data(data: str = None, frequenza_cardiaca: int = None, pressione: int = None, saturazione: int = None, username: str = Depends(verifica_token)):
    if not any([data, frequenza_cardiaca, pressione, saturazione]):
        raise HTTPException(status_code=400, detail="Error: Dati non forniti!")
    
    conn = db_connect()
    cursor = conn.cursor()
    QUERY = 'INSERT INTO DatiCuore ("data", frequenza_cardiaca, pressione, saturazione) VALUES (%s, %s, %s, %s)'

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