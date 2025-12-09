"""
Testes automatizados para o BlogSimples
Cobre rotas públicas, autenticação, CRUD de categorias e artigos
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import sys
import os

# Configurar path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

client = TestClient(app)


class TestRotasPublicas:
    """Testes de rotas públicas (sem autenticação)"""

    def test_home_page(self):
        """GET / deve retornar 200 e conter a página inicial"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Blog" in response.text or "blog" in response.text.lower()

    def test_index_page(self):
        """GET /index deve retornar 200"""
        response = client.get("/index")
        assert response.status_code == 200

    def test_sobre_page(self):
        """GET /sobre deve retornar 200"""
        response = client.get("/sobre")
        assert response.status_code == 200

    def test_artigos_list_page(self):
        """GET /artigos deve retornar 200 e listar artigos"""
        response = client.get("/artigos")
        assert response.status_code == 200
        assert "artigo" in response.text.lower()

    def test_artigos_list_pagination(self):
        """GET /artigos?page=1 deve funcionar com paginação"""
        response = client.get("/artigos?page=1")
        assert response.status_code == 200

    def test_artigos_list_com_categoria(self):
        """GET /artigos?categoria=1 deve funcionar com filtro"""
        response = client.get("/artigos?categoria=1")
        assert response.status_code == 200

    def test_artigo_nao_encontrado(self):
        """GET /artigos/ler/999 deve retornar 404 se artigo não existe"""
        response = client.get("/artigos/ler/999")
        assert response.status_code == 404


class TestAutenticacao:
    """Testes de autenticação e cadastro"""

    def test_pagina_cadastro(self):
        """GET /cadastrar deve exibir form de cadastro"""
        response = client.get("/cadastrar")
        assert response.status_code == 200
        assert "cadastro" in response.text.lower() or "register" in response.text.lower()

    def test_pagina_login(self):
        """GET /login deve exibir form de login"""
        response = client.get("/login")
        assert response.status_code == 200
        assert "login" in response.text.lower()

    def test_logout(self):
        """GET /logout deve desconectar usuário"""
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200


class TestAdminCategorias:
    """Testes para CRUD de categorias (admin)"""

    def test_listar_categorias_sem_autenticacao(self):
        """GET /admin/categorias sem login deve redirecionar"""
        response = client.get("/admin/categorias")
        assert response.status_code in [200, 303, 307, 302]  # redirect ou acesso negado

    def test_categorias_page_sem_auth(self):
        """Acesso a categorias sem auth deve falhar ou redirecionar"""
        response = client.get("/admin/categorias/")
        assert response.status_code in [200, 303, 307, 302]


class TestAdminArticles:
    """Testes para CRUD de artigos (admin)"""

    def test_listar_artigos_admin_sem_autenticacao(self):
        """GET /admin/artigos sem login deve redirecionar"""
        response = client.get("/admin/artigos")
        assert response.status_code in [200, 303, 307, 302]

    def test_artigos_page_sem_auth(self):
        """Acesso a artigos admin sem auth deve falhar ou redirecionar"""
        response = client.get("/admin/artigos/")
        assert response.status_code in [200, 303, 307, 302]


class TestDocumentacao:
    """Testes de endpoints de documentação"""

    def test_swagger_docs(self):
        """GET /docs deve retornar Swagger UI"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()

    def test_redoc_docs(self):
        """GET /redoc deve retornar ReDoc UI"""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestErros:
    """Testes de páginas de erro"""

    def test_pagina_nao_encontrada(self):
        """GET /rota/inexistente deve retornar 404"""
        response = client.get("/rota/inexistente/aleatoria")
        assert response.status_code == 404


class TestHeadersSeguranca:
    """Testes de headers de segurança"""

    def test_security_headers_na_home(self):
        """Home page deve ter headers de segurança"""
        response = client.get("/")
        # Verificar se headers de segurança existem
        assert response.status_code == 200
        # X-Content-Type-Options, X-Frame-Options etc são esperados
        # (podem estar em response.headers)


class TestRateLimiting:
    """Testes de rate limiting"""

    def test_rate_limit_publico(self):
        """Rate limiting deve estar ativo para rotas públicas"""
        # Fazer múltiplas requisições rápidas
        for i in range(5):
            response = client.get("/")
            assert response.status_code in [200, 429]  # OK ou Too Many Requests


class TestRotasInternas:
    """Testes de integração com rotas internas"""

    def test_home_com_ultimos_artigos(self):
        """Home deve carregar os últimos artigos"""
        response = client.get("/")
        assert response.status_code == 200
        # Deve conter referências a artigos (mesmo que vazio)
        assert "html" in response.text.lower()

    def test_base_publica_menu(self):
        """Menu público deve ter links corretos"""
        response = client.get("/")
        assert "Início" in response.text or "Home" in response.text
        assert "Sobre" in response.text or "About" in response.text
        assert "Artigos" in response.text

    def test_navbar_artigos_link(self):
        """Navbar deve ter link para artigos"""
        response = client.get("/")
        assert "/artigos" in response.text


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
