from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Profile, PerfilCandidato, ExperienciaProfissional, 
    FormacaoAcademica, Competencia, Idioma, Vaga, Candidatura
)

# 1. Inlines apontando para User (conforme seu models.py atual)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class PerfilCandidatoInline(admin.StackedInline):
    model = PerfilCandidato
    can_delete = False

class ExperienciaInline(admin.TabularInline):
    model = ExperienciaProfissional
    extra = 0

class FormacaoInline(admin.TabularInline):
    model = FormacaoAcademica
    extra = 0

class CompetenciaInline(admin.TabularInline):
    model = Competencia
    extra = 0

class IdiomaInline(admin.TabularInline):
    model = Idioma
    extra = 0

# 2. Re-registrar o UserAdmin para incluir TUDO em uma página só
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [
        ProfileInline, 
        PerfilCandidatoInline, 
        ExperienciaInline, 
        FormacaoInline, 
        CompetenciaInline, 
        IdiomaInline
    ]
    list_display = ('username', 'email', 'get_tipo', 'is_staff')

    def get_tipo(self, obj):
        try:
            return obj.profile.tipo
        except:
            return "-"
    get_tipo.short_description = 'Tipo de Usuário'

# 3. Manter os registros de Vaga e Candidatura como estavam
@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'codigo_vaga', 'modelo_trabalho')
    list_filter = ('modelo_trabalho', 'tipo_contrato')
    search_fields = ('titulo', 'codigo_vaga')

@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ('vaga', 'candidato', 'status', 'score', 'criada_em')
    list_filter = ('status',)
    ordering = ('-score',)

# Opcional: registrar individualmente se quiser acesso rápido pela home do admin
admin.site.register(Profile)
admin.site.register(PerfilCandidato)