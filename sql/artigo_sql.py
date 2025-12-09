CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS artigo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    conteudo TEXT,
    status TEXT,
    categoria_id INTEGER,
    autor_id INTEGER,
    data_cadastro TEXT,
    data_atualizacao TEXT
)
"""

INSERIR = """
INSERT INTO artigo (titulo, conteudo, status, categoria_id, autor_id, data_cadastro, data_atualizacao)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE artigo SET titulo = ?, conteudo = ?, status = ?, categoria_id = ?, autor_id = ?, data_atualizacao = ?
WHERE id = ?
"""

EXCLUIR = """
DELETE FROM artigo WHERE id = ?
"""

OBTER_TODOS = """
SELECT id, titulo, conteudo, status, categoria_id, autor_id, data_cadastro, data_atualizacao
FROM artigo ORDER BY data_cadastro DESC
"""

OBTER_POR_ID = """
SELECT id, titulo, conteudo, status, categoria_id, autor_id, data_cadastro, data_atualizacao
FROM artigo WHERE id = ?
"""

OBTER_POR_TITULO = """
SELECT id, titulo, conteudo, status, categoria_id, autor_id, data_cadastro, data_atualizacao
FROM artigo WHERE titulo = ?
"""

OBTER_ULTIMOS_PUBLICADOS = """
SELECT id, titulo, conteudo, status, categoria_id, autor_id, data_cadastro, data_atualizacao
FROM artigo WHERE status = 'Publicado' ORDER BY data_cadastro DESC LIMIT ?
"""
