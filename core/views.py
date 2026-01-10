from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .decorators import apenas_empresa
from .forms import (
    CadastroForm,
    VagaForm,
    PerfilCandidatoForm,
    ExperienciaProfissionalForm,
    FormacaoAcademicaForm
)
from .models import (
    Vaga,
    Candidatura,
    PerfilCandidato,
    ExperienciaProfissional,
    FormacaoAcademica
)

# ======================================================================
# LANDING / AUTENTICAÇÃO
# ======================================================================

def landing(request):
    return render(request, 'public/landing.html')


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CadastroForm()

    return render(request, 'auth/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# ======================================================================
# VAGAS – LISTAGEM / DETALHE
# ======================================================================

def vagas(request):
    vagas = Vaga.objects.all().order_by('-criada_em')

    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = request.user.profile.tipo

    return render(request, 'vagas/list.html', {
        'vagas': vagas,
        'tipo_usuario': tipo_usuario
    })


@login_required
def detalhe_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    return render(request, 'vagas/detail.html', {'vaga': vaga})


# ======================================================================
# VAGAS – EMPRESA
# ======================================================================

@apenas_empresa
@login_required
def empresa(request):
    vagas = Vaga.objects.filter(empresa=request.user)
    return render(request, 'empresa/profile.html', {'vagas': vagas})


@apenas_empresa
@login_required
def criar_vaga(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user
            vaga.save()
            messages.success(request, 'Vaga criada com sucesso.')
            return redirect('company_dashboard')
    else:
        form = VagaForm()

    return render(request, 'vagas/create.html', {'form': form})


@apenas_empresa
@login_required
def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)

    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaga atualizada com sucesso.')
            return redirect('company_dashboard')
    else:
        form = VagaForm(instance=vaga)

    return render(request, 'vagas/edit.html', {
        'form': form,
        'vaga': vaga
    })


@apenas_empresa
@login_required
def candidaturas_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)
    candidaturas = vaga.candidaturas.select_related('candidato')

    return render(request, 'vagas/applicants.html', {
        'vaga': vaga,
        'candidaturas': candidaturas
    })


@apenas_empresa
@login_required
def atualizar_status_candidatura(request, candidatura_id):
    candidatura = get_object_or_404(
        Candidatura,
        id=candidatura_id,
        vaga__empresa=request.user
    )

    if request.method == 'POST':
        novo_status = request.POST.get('status')

        if novo_status in dict(Candidatura.STATUS_CHOICES):
            candidatura.status = novo_status
            candidatura.save()
            messages.success(request, 'Status atualizado com sucesso.')

    return redirect('vaga_applicants', vaga_id=candidatura.vaga.id)


# ======================================================================
# CANDIDATURA – CANDIDATO
# ======================================================================

@login_required
def candidatar_vaga(request, vaga_id):
    if request.user.profile.tipo != 'candidato':
        messages.error(request, 'Apenas candidatos podem se candidatar.')
        return redirect('vaga_list')

    vaga = get_object_or_404(Vaga, id=vaga_id)

    if Candidatura.objects.filter(vaga=vaga, candidato=request.user).exists():
        messages.warning(request, 'Você já se candidatou a esta vaga.')
        return redirect('vaga_list')

    if request.method == 'POST':
        Candidatura.objects.create(
            vaga=vaga,
            candidato=request.user,
            mensagem=request.POST.get('mensagem', '')
        )
        messages.success(request, 'Candidatura enviada com sucesso.')
        return redirect('vaga_list')

    return render(request, 'vagas/apply.html', {'vaga': vaga})

@login_required
def minhas_candidaturas(request):
    candidaturas = Candidatura.objects.filter(
        candidato=request.user
    ).select_related('vaga')

    return render(request, 'candidato/applications.html', {
        'candidaturas': candidaturas
    })


# ======================================================================
# PERFIL DO CANDIDATO
# ======================================================================

@login_required
def perfil_candidato(request):
    if request.user.profile.tipo != 'candidato':
        return redirect('dashboard')

    perfil, _ = PerfilCandidato.objects.get_or_create(user=request.user)

    return render(request, 'candidato/profile.html', {
        'perfil': perfil,
        'experiencias': request.user.experiencias.all(),
        'formacoes': request.user.formacoes.all()
    })


@login_required
def editar_perfil_candidato(request):
    if request.user.profile.tipo != 'candidato':
        return redirect('dashboard')

    perfil, _ = PerfilCandidato.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PerfilCandidatoForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso.')
            return redirect('candidate_profile')
    else:
        form = PerfilCandidatoForm(instance=perfil)

    return render(request, 'candidato/edit_profile.html', {'form': form})


# ======================================================================
# EXPERIÊNCIA PROFISSIONAL
# ======================================================================

@login_required
def adicionar_experiencia(request):
    if request.user.profile.tipo != 'candidato':
        return redirect('dashboard')

    if request.method == 'POST':
        form = ExperienciaProfissionalForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.candidato = request.user
            experiencia.save()
            messages.success(request, 'Experiência adicionada com sucesso.')
            return redirect('candidate_profile')
    else:
        form = ExperienciaProfissionalForm()

    return render(request, 'candidato/experience_form.html', {
        'form': form,
        'titulo': 'Adicionar Experiência'
    })


@login_required
def editar_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(
        ExperienciaProfissional,
        id=experiencia_id,
        candidato=request.user
    )

    if request.method == 'POST':
        form = ExperienciaProfissionalForm(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiência atualizada.')
            return redirect('candidate_profile')
    else:
        form = ExperienciaProfissionalForm(instance=experiencia)

    return render(request, 'candidato/experience_form.html', {
        'form': form,
        'titulo': 'Editar Experiência'
    })


@login_required
def excluir_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(
        ExperienciaProfissional,
        id=experiencia_id,
        candidato=request.user
    )

    experiencia.delete()
    messages.success(request, 'Experiência removida.')
    return redirect('candidate_profile')


# ======================================================================
# FORMAÇÃO ACADÊMICA
# ======================================================================

@login_required
def adicionar_formacao(request):
    if request.user.profile.tipo != 'candidato':
        return redirect('dashboard')

    if request.method == 'POST':
        form = FormacaoAcademicaForm(request.POST)
        if form.is_valid():
            formacao = form.save(commit=False)
            formacao.candidato = request.user
            formacao.save()
            messages.success(request, 'Formação acadêmica adicionada.')
            return redirect('candidate_profile')
    else:
        form = FormacaoAcademicaForm()

    return render(request, 'candidato/education_form.html', {
        'form': form,
        'titulo': 'Adicionar Formação Acadêmica'
    })


@login_required
def editar_formacao(request, formacao_id):
    formacao = get_object_or_404(
        FormacaoAcademica,
        id=formacao_id,
        candidato=request.user
    )

    if request.method == 'POST':
        form = FormacaoAcademicaForm(request.POST, instance=formacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formação acadêmica atualizada.')
            return redirect('candidate_profile')
    else:
        form = FormacaoAcademicaForm(instance=formacao)

    return render(request, 'candidato/education_form.html', {
        'form': form,
        'titulo': 'Editar Formação Acadêmica'
    })


@login_required
def excluir_formacao(request, formacao_id):
    formacao = get_object_or_404(
        FormacaoAcademica,
        id=formacao_id,
        candidato=request.user
    )

    formacao.delete()
    messages.success(request, 'Formação acadêmica removida.')
    return redirect('candidate_profile')
