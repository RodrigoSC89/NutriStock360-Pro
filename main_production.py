# NutriStock360 - API Produção Railway
# Versão otimizada para deploy em produção

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
import jwt
import os

# Configurações
SECRET_KEY = os.getenv("SECRET_KEY", "nutristock360_secret_key_change_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Database URL - Railway automaticamente fornece DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fallback para desenvolvimento local
    DATABASE_URL = "sqlite:///./nutristock360.db"

# Ajustar para PostgreSQL se necessário
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# FastAPI App
app = FastAPI(
    title="NutriStock360 API",
    description="Sistema completo para nutricionistas",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - permitir acesso do frontend
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://*.railway.app",
    "https://*.up.railway.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= MODELS =============

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    nome = Column(String)
    crn = Column(String)
    telefone = Column(String)
    role = Column(String, default="nutricionista")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    pacientes = relationship("Paciente", back_populates="nutricionista")
    consultas = relationship("Consulta", back_populates="nutricionista")
    planos = relationship("PlanoAlimentar", back_populates="nutricionista")

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String)
    cpf = Column(String)
    telefone = Column(String)
    data_nascimento = Column(DateTime)
    peso_atual = Column(Float)
    altura = Column(Integer)
    objetivo = Column(String)
    observacoes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    nutricionista_id = Column(Integer, ForeignKey("users.id"))
    
    nutricionista = relationship("User", back_populates="pacientes")
    consultas = relationship("Consulta", back_populates="paciente")
    planos = relationship("PlanoAlimentar", back_populates="paciente")

class Alimento(Base):
    __tablename__ = "alimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    categoria = Column(String)
    porcao = Column(Integer, default=100)
    calorias = Column(Float)
    carboidratos = Column(Float)
    proteinas = Column(Float)
    gorduras = Column(Float)
    fibras = Column(Float)
    sodio = Column(Float, default=0)
    acucar = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class PlanoAlimentar(Base):
    __tablename__ = "planos_alimentares"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    objetivo = Column(String)
    calorias_diarias = Column(Integer)
    duracao_dias = Column(Integer)
    observacoes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    nutricionista_id = Column(Integer, ForeignKey("users.id"))
    
    paciente = relationship("Paciente", back_populates="planos")
    nutricionista = relationship("User", back_populates="planos")

class Consulta(Base):
    __tablename__ = "consultas"
    
    id = Column(Integer, primary_key=True, index=True)
    data_consulta = Column(DateTime)
    tipo = Column(String)
    status = Column(String, default="agendada")
    observacoes = Column(Text)
    valor = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    nutricionista_id = Column(Integer, ForeignKey("users.id"))
    
    paciente = relationship("Paciente", back_populates="consultas")
    nutricionista = relationship("User", back_populates="consultas")

# ============= SCHEMAS =============

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nome: str
    crn: str
    telefone: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: dict

class PacienteCreate(BaseModel):
    nome: str
    email: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    peso_atual: Optional[float] = None
    altura: Optional[int] = None
    objetivo: Optional[str] = None
    observacoes: Optional[str] = None

class AlimentoCreate(BaseModel):
    nome: str
    categoria: str
    porcao: int = 100
    calorias: float
    carboidratos: float
    proteinas: float
    gorduras: float
    fibras: float
    sodio: Optional[float] = 0
    acucar: Optional[float] = 0

class PlanoCreate(BaseModel):
    nome: str
    paciente_id: int
    objetivo: str
    calorias_diarias: int
    duracao_dias: int
    observacoes: Optional[str] = None

class ConsultaCreate(BaseModel):
    paciente_id: int
    data_consulta: datetime
    tipo: str
    observacoes: Optional[str] = None
    valor: Optional[float] = None

# ============= DEPENDENCIES =============

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# ============= STARTUP =============

@app.on_event("startup")
async def startup_event():
    # Criar tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    
    # Inicializar dados básicos
    db = SessionLocal()
    try:
        # Verificar se já existem alimentos
        if db.query(Alimento).count() == 0:
            await inicializar_alimentos(db)
    finally:
        db.close()

async def inicializar_alimentos(db: Session):
    """Inicializar base de alimentos brasileiros"""
    alimentos_basicos = [
        {"nome": "Arroz branco cozido", "categoria": "cereais", "calorias": 128, "carboidratos": 26.2, "proteinas": 2.5, "gorduras": 0.2, "fibras": 1.6},
        {"nome": "Feijão carioca cozido", "categoria": "leguminosas", "calorias": 76, "carboidratos": 13.6, "proteinas": 4.8, "gorduras": 0.5, "fibras": 8.5},
        {"nome": "Frango peito grelhado", "categoria": "carnes", "calorias": 159, "carboidratos": 0.0, "proteinas": 32.0, "gorduras": 3.2, "fibras": 0.0},
        {"nome": "Ovo de galinha", "categoria": "carnes", "calorias": 155, "carboidratos": 1.6, "proteinas": 13.0, "gorduras": 11.0, "fibras": 0.0},
        {"nome": "Banana nanica", "categoria": "frutas", "calorias": 92, "carboidratos": 23.8, "proteinas": 1.4, "gorduras": 0.1, "fibras": 2.0},
        {"nome": "Maçã", "categoria": "frutas", "calorias": 56, "carboidratos": 14.8, "proteinas": 0.3, "gorduras": 0.1, "fibras": 1.3},
        {"nome": "Leite desnatado", "categoria": "laticinios", "calorias": 34, "carboidratos": 4.5, "proteinas": 3.4, "gorduras": 0.1, "fibras": 0.0},
        {"nome": "Pão francês", "categoria": "cereais", "calorias": 270, "carboidratos": 56.2, "proteinas": 8.0, "gorduras": 2.2, "fibras": 2.3},
        {"nome": "Batata inglesa cozida", "categoria": "vegetais", "calorias": 52, "carboidratos": 11.9, "proteinas": 1.4, "gorduras": 0.1, "fibras": 1.3},
        {"nome": "Tomate", "categoria": "vegetais", "calorias": 15, "carboidratos": 3.1, "proteinas": 1.1, "gorduras": 0.2, "fibras": 1.2},
        {"nome": "Alface americana", "categoria": "vegetais", "calorias": 11, "carboidratos": 1.8, "proteinas": 1.4, "gorduras": 0.2, "fibras": 1.1},
        {"nome": "Cenoura crua", "categoria": "vegetais", "calorias": 34, "carboidratos": 7.7, "proteinas": 1.3, "gorduras": 0.2, "fibras": 3.2},
        {"nome": "Brócolis cozido", "categoria": "vegetais", "calorias": 25, "carboidratos": 4.0, "proteinas": 3.6, "gorduras": 0.4, "fibras": 3.4},
        {"nome": "Aveia em flocos", "categoria": "cereais", "calorias": 394, "carboidratos": 66.6, "proteinas": 13.9, "gorduras": 8.5, "fibras": 9.1},
        {"nome": "Iogurte natural", "categoria": "laticinios", "calorias": 51, "carboidratos": 7.0, "proteinas": 4.3, "gorduras": 0.2, "fibras": 0.0}
    ]
    
    for alimento_data in alimentos_basicos:
        alimento = Alimento(**alimento_data)
        db.add(alimento)
    
    db.commit()

# ============= ENDPOINTS =============

@app.get("/")
async def root():
    return {"message": "NutriStock360 API", "status": "online", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        nome=user.nome,
        crn=user.crn,
        telefone=user.telefone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "id": db_user.id,
            "email": db_user.email,
            "nome": db_user.nome,
            "crn": db_user.crn,
            "role": db_user.role
        }
    }

@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "id": db_user.id,
            "email": db_user.email,
            "nome": db_user.nome,
            "crn": db_user.crn,
            "role": db_user.role
        }
    }

@app.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nome": current_user.nome,
        "crn": current_user.crn,
        "role": current_user.role
    }

# ===== PACIENTES =====

@app.post("/pacientes")
async def criar_paciente(paciente: PacienteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_paciente = Paciente(**paciente.dict(), nutricionista_id=current_user.id)
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@app.get("/pacientes")
async def listar_pacientes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Paciente).filter(Paciente.nutricionista_id == current_user.id, Paciente.is_active == True).all()

@app.get("/pacientes/{paciente_id}")
async def obter_paciente(paciente_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(
        Paciente.id == paciente_id, 
        Paciente.nutricionista_id == current_user.id
    ).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

# ===== ALIMENTOS =====

@app.post("/alimentos")
async def criar_alimento(alimento: AlimentoCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_alimento = Alimento(**alimento.dict())
    db.add(db_alimento)
    db.commit()
    db.refresh(db_alimento)
    return db_alimento

@app.get("/alimentos")
async def listar_alimentos(categoria: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Alimento)
    if categoria:
        query = query.filter(Alimento.categoria == categoria)
    return query.all()

# ===== PLANOS =====

@app.post("/planos")
async def criar_plano(plano: PlanoCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_plano = PlanoAlimentar(**plano.dict(), nutricionista_id=current_user.id)
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano

@app.get("/planos")
async def listar_planos(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(PlanoAlimentar).filter(PlanoAlimentar.nutricionista_id == current_user.id).all()

# ===== CONSULTAS =====

@app.post("/consultas")
async def criar_consulta(consulta: ConsultaCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_consulta = Consulta(**consulta.dict(), nutricionista_id=current_user.id)
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@app.get("/consultas")
async def listar_consultas(data: Optional[str] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Consulta).filter(Consulta.nutricionista_id == current_user.id)
    if data:
        query = query.filter(Consulta.data_consulta.contains(data))
    return query.all()

# ===== DASHBOARD =====

@app.get("/dashboard")
async def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total_pacientes = db.query(Paciente).filter(
        Paciente.nutricionista_id == current_user.id,
        Paciente.is_active == True
    ).count()
    
    hoje = datetime.now().date()
    consultas_hoje = db.query(Consulta).filter(
        Consulta.nutricionista_id == current_user.id,
        Consulta.data_consulta.contains(str(hoje))
    ).count()
    
    planos_ativos = db.query(PlanoAlimentar).filter(
        PlanoAlimentar.nutricionista_id == current_user.id,
        PlanoAlimentar.is_active == True
    ).count()
    
    return {
        "total_pacientes": total_pacientes,
        "consultas_hoje": consultas_hoje,
        "planos_ativos": planos_ativos,
        "alertas": 0
    }

# Servir arquivos estáticos se houver uma pasta static
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)