from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates
from dtos.artigo_dto import CriarArtigoDTO, AlterarArtigoDTO
from repo import artigo_repo, categoria_repo
from model.artigo_model import Artigo
from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil

router = APIRouter(prefix="/admin/artigos", tags=["Admin - Artigos"]) 
templates = criar_templates()


@router.get("/listar", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ADMIN.value])
def listar(request: Request):
    artigos = artigo_repo.obter_todos()
    return templates.TemplateResponse(
        "admin/artigos/listar.html",
        {"request": request, "artigos": artigos},
    )


@router.get("/cadastrar", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ADMIN.value])
def cadastrar_form(request: Request):
    categorias = categoria_repo.obter_todos()
    return templates.TemplateResponse(
        "admin/artigos/cadastrar.html",
        {"request": request, "categorias": categorias, "form": {}},
    )


@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
def cadastrar(request: Request, titulo: str = Form(...), conteudo: str = Form(""), categoria_id: int = Form(None)):
    dto = CriarArtigoDTO(titulo=titulo, conteudo=conteudo, categoria_id=categoria_id)
    artigo = Artigo(titulo=dto.titulo, conteudo=dto.conteudo, categoria_id=dto.categoria_id)
    artigo_repo.inserir(artigo)
    informar_sucesso(request, "Artigo cadastrado com sucesso")
    return RedirectResponse(url="/admin/artigos/listar", status_code=302)


@router.get("/editar/{id}", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ADMIN.value])
def editar_form(request: Request, id: int):
    artigo = artigo_repo.obter_por_id(id)
    if not artigo:
        informar_erro(request, "Artigo não encontrado")
        return RedirectResponse(url="/admin/artigos/listar", status_code=302)
    categorias = categoria_repo.obter_todos()
    return templates.TemplateResponse(
        "admin/artigos/editar.html",
        {"request": request, "artigo": artigo, "categorias": categorias},
    )


@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
def editar(request: Request, id: int, titulo: str = Form(...), conteudo: str = Form(""), categoria_id: int = Form(None)):
    artigo = artigo_repo.obter_por_id(id)
    if not artigo:
        informar_erro(request, "Artigo não encontrado")
        return RedirectResponse(url="/admin/artigos/listar", status_code=302)
    dto = AlterarArtigoDTO(titulo=titulo, conteudo=conteudo, categoria_id=categoria_id)
    artigo.titulo = dto.titulo
    artigo.conteudo = dto.conteudo
    artigo.categoria_id = dto.categoria_id
    artigo_repo.alterar(artigo)
    informar_sucesso(request, "Artigo atualizado com sucesso")
    return RedirectResponse(url="/admin/artigos/listar", status_code=302)


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
def excluir(request: Request, id: int):
    artigo_repo.excluir(id)
    informar_sucesso(request, "Artigo excluído com sucesso")
    return RedirectResponse(url="/admin/artigos/listar", status_code=302)
