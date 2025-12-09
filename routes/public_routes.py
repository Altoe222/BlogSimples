from fastapi import APIRouter, Request, status

from util.template_util import criar_templates
from util.auth_decorator import obter_usuario_logado
from util.rate_limiter import DynamicRateLimiter, obter_identificador_cliente
from util.flash_messages import informar_erro
from util.logger_config import logger
from repo import artigo_repo, categoria_repo

router = APIRouter()
templates_public = criar_templates()

# Rate limiter para páginas públicas (proteção contra DDoS)
public_limiter = DynamicRateLimiter(
    chave_max="rate_limit_public_max",
    chave_minutos="rate_limit_public_minutos",
    padrao_max=100,
    padrao_minutos=1,
    nome="public_pages",
)


@router.get("/")
async def home(request: Request):
    """
    Rota inicial - Landing Page pública com os últimos artigos
    """
    # Rate limiting por IP
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

    # Obtém os 6 últimos artigos publicados
    ultimos_artigos = artigo_repo.obter_ultimos_publicados(6)
    categorias = categoria_repo.obter_todos()
    usuario_logado = obter_usuario_logado(request)

    return templates_public.TemplateResponse(
        "index.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "ultimos_artigos": ultimos_artigos,
            "categorias": categorias,
        }
    )


@router.get("/index")
async def index(request: Request):
    """
    Página pública inicial (Landing Page)
    Sempre exibe a página pública, independentemente de autenticação
    """
    # Rate limiting por IP
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

    # Obtém os 6 últimos artigos publicados
    ultimos_artigos = artigo_repo.obter_ultimos_publicados(6)
    categorias = categoria_repo.obter_todos()
    usuario_logado = obter_usuario_logado(request)

    return templates_public.TemplateResponse(
        "index.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "ultimos_artigos": ultimos_artigos,
            "categorias": categorias,
        }
    )


@router.get("/sobre")
async def sobre(request: Request):
    """
    Página "Sobre" com informações do projeto acadêmico
    """
    # Rate limiting por IP
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

    return templates_public.TemplateResponse(
        "sobre.html",
        {"request": request}
    )


@router.get("/artigos")
async def listar_artigos(request: Request, page: int = 1, categoria: int | None = None):
    """Lista pública de artigos publicados (paginada)."""
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

    limite = 10
    offset = (max(page, 1) - 1) * limite
    artigos = artigo_repo.obter_publicados(offset=offset, limite=limite, categoria_id=categoria)
    categorias = categoria_repo.obter_todos()
    usuario_logado = obter_usuario_logado(request)

    return templates_public.TemplateResponse(
        "artigos/listar.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "artigos": artigos,
            "categorias": categorias,
            "pagina": page,
        }
    )


@router.get("/artigos/ler/{artigo_id}")
async def ler_artigo(request: Request, artigo_id: int):
    """Visualiza um artigo publicado por id."""
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

    # incrementa contador de visualizacoes e refaz o fetch para exibir o novo valor
    try:
        artigo_repo.incrementar_visualizacoes(artigo_id)
    except Exception:
        # não bloquear a visualização se incremento falhar
        pass

    artigo = artigo_repo.obter_por_id(artigo_id)
    if not artigo or artigo.status != 'Publicado':
        return templates_public.TemplateResponse(
            "errors/404.html",
            {"request": request},
            status_code=status.HTTP_404_NOT_FOUND
        )

    usuario_logado = obter_usuario_logado(request)
    categorias = categoria_repo.obter_todos()

    return templates_public.TemplateResponse(
        "artigos/ler.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "artigo": artigo,
            "categorias": categorias,
        }
    )
