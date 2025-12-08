import sqlite3
from model.artigo_model import Artigo
from sql.artigo_sql import (
    CRIAR_TABELA,
    INSERIR,
    ALTERAR,
    EXCLUIR,
    OBTER_TODOS,
    OBTER_POR_ID,
    OBTER_POR_TITULO,
)
from util.config import DATABASE_PATH


def criar_tabela():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.cursor()
        cur.execute(CRIAR_TABELA)
        conn.commit()
    finally:
        conn.close()


def inserir(artigo: Artigo) -> int:
    artigo.set_timestamps_for_insert()
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.cursor()
        cur.execute(INSERIR, (
            artigo.titulo,
            artigo.conteudo,
            artigo.status,
            artigo.categoria_id,
            artigo.autor_id,
            artigo.data_cadastro,
            artigo.data_atualizacao,
        ))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def alterar(artigo: Artigo) -> None:
    artigo.touch_update()
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.cursor()
        cur.execute(ALTERAR, (
            artigo.titulo,
            artigo.conteudo,
            artigo.status,
            artigo.categoria_id,
            artigo.autor_id,
            artigo.data_atualizacao,
            artigo.id,
        ))
        conn.commit()
    finally:
        conn.close()


def excluir(artigo_id: int) -> None:
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.cursor()
        cur.execute(EXCLUIR, (artigo_id,))
        conn.commit()
    finally:
        conn.close()


def obter_por_id(artigo_id: int) -> Artigo | None:
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.cursor()
        cur.execute(OBTER_POR_ID, (artigo_id,))
        row = cur.fetchone()
        if not row:
            return None
        return _row_to_artigo(row)
    finally:
        conn.close()


def obter_todos() -> list[Artigo]:
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.cursor()
        cur.execute(OBTER_TODOS)
        rows = cur.fetchall()
        return [_row_to_artigo(r) for r in rows]
    finally:
        conn.close()


def obter_por_titulo(titulo: str) -> Artigo | None:
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.cursor()
        cur.execute(OBTER_POR_TITULO, (titulo,))
        row = cur.fetchone()
        if not row:
            return None
        return _row_to_artigo(row)
    finally:
        conn.close()


def _row_to_artigo(row) -> Artigo:
    return Artigo(
        id=row[0],
        titulo=row[1],
        conteudo=row[2],
        status=row[3],
        categoria_id=row[4],
        autor_id=row[5],
        data_cadastro=row[6],
        data_atualizacao=row[7],
    )
