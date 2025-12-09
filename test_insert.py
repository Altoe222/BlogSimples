import sqlite3
from datetime import datetime

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
now = datetime.utcnow().isoformat(sep=' ')
c.execute("INSERT INTO artigo (titulo, conteudo, status, categoria_id, autor_id, data_cadastro, data_atualizacao, visualizacoes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
          ('Teste Artigo', 'Conteúdo teste para verificação', 'Publicado', 1, 1, now, now, 0))
conn.commit()
print('Artigo inserido com sucesso')
conn.close()
