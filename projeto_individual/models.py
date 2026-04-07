# Arquivo Models.py

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Caso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    status: str
    classificacao: str
    prioridade: str
    criado_em: datetime = Field(default_factory=datetime.utcnow)

    evidencias: List["Evidencia"] = Relationship(back_populates="caso")


class Evidencia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    categoria: str
    status_atual: str
    coletado_onde: Optional[str] = None
    coletado_quando: datetime

    caso_id: int = Field(foreign_key="caso.id")
    caso: Optional[Caso] = Relationship(back_populates="evidencias")