from typing import Optional
from model.categoria_model import Categoria
from sql.categoria_sql import *
from util.db_util import obter_conexao


def _row_to_categoria(row) -> Categoria:
    """
    Converte uma linha do banco de dados em objeto Categoria.
    """
    return Categoria(
        id=row["id"] if isinstance(row, dict) else row[0],
        nome=row["nome"] if isinstance(row, dict) else row[1],
        descricao=row["descricao"] if isinstance(row, dict) else row[2],
        data_cadastro=row["data_cadastro"] if isinstance(row, dict) else row[3],
        data_atualizacao=row["data_atualizacao"] if isinstance(row, dict) else row[4],
    )


def criar_tabela():
    """Cria a tabela de categorias se ela não existir."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)


def inserir(categoria: Categoria) -> Optional[Categoria]:
    """Insere uma nova categoria no banco de dados."""
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (categoria.nome, categoria.descricao))

            if cursor.lastrowid:
                categoria.id = cursor.lastrowid
                return categoria
            return None
    except Exception as e:
        print(f"Erro ao inserir categoria: {e}")
        return None


def alterar(categoria: Categoria) -> bool:
    """Atualiza uma categoria existente."""
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(
                ALTERAR,
                (categoria.nome, categoria.descricao, categoria.id)
            )
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao alterar categoria: {e}")
        return False


def excluir(id: int) -> bool:
    """Exclui uma categoria do banco de dados."""
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(EXCLUIR, (id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir categoria: {e}")
        return False


def obter_por_id(id: int) -> Optional[Categoria]:
    """Busca uma categoria por ID."""
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_ID, (id,))
            row = cursor.fetchone()

            if row:
                # sqlite3.Row can behave like dict; handle both
                if hasattr(row, "keys"):
                    return _row_to_categoria({k: row[k] for k in row.keys()})
                return _row_to_categoria(row)
            return None
    except Exception as e:
        print(f"Erro ao obter categoria por ID: {e}")
        return None


def obter_todos() -> list[Categoria]:
    """Retorna todas as categorias do banco de dados."""
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_TODOS)
            rows = cursor.fetchall()

            resultado = []
            for row in rows:
                if hasattr(row, "keys"):
                    resultado.append(_row_to_categoria({k: row[k] for k in row.keys()}))
                else:
                    resultado.append(_row_to_categoria(row))
            return resultado
    except Exception as e:
        print(f"Erro ao obter todas as categorias: {e}")
        return []


def obter_por_nome(nome: str) -> Optional[Categoria]:
    """Busca uma categoria pelo nome exato."""
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_POR_NOME, (nome,))
            row = cursor.fetchone()

            if row:
                if hasattr(row, "keys"):
                    return _row_to_categoria({k: row[k] for k in row.keys()})
                return _row_to_categoria(row)
            return None
    except Exception as e:
        print(f"Erro ao obter categoria por nome: {e}")
        return None
