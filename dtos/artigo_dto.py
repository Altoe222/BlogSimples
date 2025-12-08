from pydantic import BaseModel, constr, Field
from typing import Optional


class CriarArtigoDTO(BaseModel):
    titulo: constr(min_length=3, max_length=200)
    conteudo: Optional[str] = Field(default="")
    status: Optional[str] = Field(default="Rascunho")
    categoria_id: Optional[int] = None
    autor_id: Optional[int] = None


class AlterarArtigoDTO(BaseModel):
    titulo: constr(min_length=3, max_length=200)
    conteudo: Optional[str] = Field(default="")
    status: Optional[str] = Field(default="Rascunho")
    categoria_id: Optional[int] = None
    autor_id: Optional[int] = None
