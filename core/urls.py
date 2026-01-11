from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ==================================================================
    # PÚBLICO / LANDING
    # ==================================================================

    path(
        '',
        views.landing,
        name='landing'
    ),

    # ==================================================================
    # AUTENTICAÇÃO
    # ==================================================================

    path(
        'login/',
        LoginView.as_view(template_name='auth/login.html'),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),

    path(
        'cadastro/',
        views.cadastro,
        name='register'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # ==================================================================
    # VAGAS (PÚBLICO / CANDIDATO)
    # ==================================================================

    path(
        'vagas/',
        views.vagas,
        name='vaga_list'
    ),

    path(
        'vagas/<int:vaga_id>/',
        views.detalhe_vaga,
        name='vaga_detail'
    ),

    path(
        'vagas/<int:vaga_id>/candidatar/',
        views.candidatar_vaga,
        name='vaga_apply'
    ),

    # ==================================================================
    # CANDIDATO
    # ==================================================================

    path(
        'candidato/candidaturas/',
        views.minhas_candidaturas,
        name='candidate_applications'
    ),

    path(
        'candidato/perfil/',
        views.perfil_candidato,
        name='candidate_profile'
    ),

    path(
        'candidato/perfil/editar/',
        views.editar_perfil_candidato,
        name='candidate_profile_edit'
    ),

    # ---------------- EXPERIÊNCIA ----------------

    path(
        'candidato/experiencia/adicionar/',
        views.adicionar_experiencia,
        name='experience_add'
    ),

    path(
        'candidato/experiencia/<int:experiencia_id>/editar/',
        views.editar_experiencia,
        name='experience_edit'
    ),

    path(
        'candidato/experiencia/<int:experiencia_id>/excluir/',
        views.excluir_experiencia,
        name='experience_delete'
    ),

    # ---------------- FORMAÇÃO ----------------

    path(
        'candidato/formacao/adicionar/',
        views.adicionar_formacao,
        name='education_add'
    ),

    path(
        'candidato/formacao/<int:formacao_id>/editar/',
        views.editar_formacao,
        name='education_edit'
    ),

    path(
        'candidato/formacao/<int:formacao_id>/excluir/',
        views.excluir_formacao,
        name='education_delete'
    ),

    # ==================================================================
    # EMPRESA
    # ==================================================================

    path(
        'empresa/',
        views.empresa,
        name='company_dashboard'
    ),

    path(
        'empresa/vagas/criar/',
        views.criar_vaga,
        name='vaga_create'
    ),

    path(
        'empresa/vagas/<int:vaga_id>/editar/',
        views.editar_vaga,
        name='vaga_edit'
    ),

    path(
        'empresa/vagas/<int:vaga_id>/candidaturas/',
        views.candidaturas_vaga,
        name='vaga_applicants'
    ),
    
    path(
        'empresa/candidaturas/<int:candidatura_id>/status/',
        views.atualizar_status_candidatura,
        name='application_status_update'
    ),
    
    path(
        'empresa/candidato/<int:user_id>/perfil/',
        views.visualizar_perfil_candidato,
        name='company_view_candidate'
    ),

    path(
        'trabalhe-ja-talentos/', 
        views.trabalhe_ja_talentos, 
        name='trabalhe_ja_talentos' # Este nome deve bater com o erro!
    ),
    
    path('teste-perfil/', views.teste_perfil_elite, name='teste_perfil_elite'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
