from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Artigo:
    id: Optional[int] = None
    titulo: str = ""
    conteudo: str = ""
    status: str = "Rascunho"
    categoria_id: Optional[int] = None
    autor_id: Optional[int] = None
    data_cadastro: Optional[str] = None
    data_atualizacao: Optional[str] = None

    def set_timestamps_for_insert(self):
        now = datetime.utcnow().isoformat(sep=" ")
        self.data_cadastro = now
        self.data_atualizacao = now

    def touch_update(self):
        self.data_atualizacao = datetime.utcnow().isoformat(sep=" ")
