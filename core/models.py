from django.db import models
from django.contrib.auth.models import User


# ----------------------------------------------------------------------
# PERFIL DO USUÁRIO (SOMENTE CANDIDATO OU EMPRESA)
# ----------------------------------------------------------------------

class Profile(models.Model):
    TIPO_USUARIO = (
        ('candidato', 'Candidato'),
        ('empresa', 'Empresa'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} ({self.tipo})"


# ----------------------------------------------------------------------
# PERFIL COMPLETO DO CANDIDATO (CURRÍCULO)
# ----------------------------------------------------------------------

class PerfilCandidato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    titulo_profissional = models.CharField(
        max_length=150,
        help_text="Ex: João Silva | Desenvolvedor Full Stack"
    )

    foto = models.ImageField(
        upload_to='fotos_perfil/',
        blank=True,
        null=True
    )

    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)

    whatsapp = models.CharField(max_length=20)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    resumo_profissional = models.TextField()

    pretensao_salarial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    disponibilidade = models.CharField(
        max_length=20,
        choices=(
            ('imediata', 'Imediata'),
            ('15_dias', '15 dias'),
            ('30_dias', '30 dias'),
        )
    )

    modelo_trabalho = models.CharField(
        max_length=20,
        choices=(
            ('remoto', 'Remoto'),
            ('hibrido', 'Híbrido'),
            ('presencial', 'Presencial'),
        )
    )

    def __str__(self):
        return self.titulo_profissional


# ----------------------------------------------------------------------
# EXPERIÊNCIA PROFISSIONAL
# ----------------------------------------------------------------------

class ExperienciaProfissional(models.Model):
    candidato = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='experiencias'
    )

    cargo = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)

    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    atual = models.BooleanField(default=False)

    descricao = models.TextField()

    def __str__(self):
        return f"{self.cargo} - {self.empresa}"


# ----------------------------------------------------------------------
# FORMAÇÃO ACADÊMICA
# ----------------------------------------------------------------------

class FormacaoAcademica(models.Model):
    candidato = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='formacoes'
    )

    grau = models.CharField(max_length=50)
    curso = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=(
            ('concluido', 'Concluído'),
            ('cursando', 'Cursando'),
            ('trancado', 'Trancado'),
        )
    )

    def __str__(self):
        return f"{self.curso} - {self.instituicao}"


# ----------------------------------------------------------------------
# COMPETÊNCIAS
# ----------------------------------------------------------------------

class Competencia(models.Model):
    candidato = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='competencias'
    )

    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


# ----------------------------------------------------------------------
# IDIOMAS
# ----------------------------------------------------------------------

class Idioma(models.Model):
    candidato = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='idiomas'
    )

    idioma = models.CharField(max_length=50)

    nivel = models.CharField(
        max_length=20,
        choices=(
            ('basico', 'Básico'),
            ('intermediario', 'Intermediário'),
            ('avancado', 'Avançado'),
            ('fluente', 'Fluente'),
        )
    )

    def __str__(self):
        return f"{self.idioma} ({self.nivel})"


# ----------------------------------------------------------------------
# VAGAS
# ----------------------------------------------------------------------

class Vaga(models.Model):

    MODELO_TRABALHO = (
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
        ('presencial', 'Presencial'),
    )

    TIPO_CONTRATO = (
        ('clt', 'CLT'),
        ('pj', 'PJ'),
        ('estagio', 'Estágio'),
        ('temporario', 'Temporário'),
    )

    titulo = models.CharField(max_length=150)
    departamento = models.CharField(max_length=100)
    codigo_vaga = models.CharField(max_length=50, unique=True)
    data_publicacao = models.DateField(auto_now_add=True)

    modelo_trabalho = models.CharField(max_length=20, choices=MODELO_TRABALHO)
    localizacao = models.CharField(max_length=100)
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO)
    carga_horaria = models.CharField(max_length=50)

    resumo = models.TextField()
    responsabilidades = models.TextField()
    requisitos_obrigatorios = models.TextField()
    requisitos_desejaveis = models.TextField(blank=True)
    soft_skills = models.TextField(blank=True)

    beneficios = models.TextField(blank=True)
    salario_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    etapas_processo = models.TextField(blank=True)
    cultura_empresa = models.URLField(blank=True)

    empresa = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vagas'
    )

    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.codigo_vaga})"


# ----------------------------------------------------------------------
# CANDIDATURA
# ----------------------------------------------------------------------

class Candidatura(models.Model):
    STATUS_CHOICES = (
        ('enviada', 'Enviada'),
        ('em_analise', 'Em análise'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    )

    vaga = models.ForeignKey(
        Vaga,
        on_delete=models.CASCADE,
        related_name='candidaturas'
    )

    candidato = models.ForeignKey(User, on_delete=models.CASCADE)

    mensagem = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='enviada'
    )

    criada_em = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('vaga', 'candidato')

    def __str__(self):
        return f"{self.candidato.email} → {self.vaga.titulo}"
