from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


# ----------------------------------------------------------------------
# PERFIL DO USUÁRIO (SOMENTE CANDIDATO OU EMPRESA)
# ----------------------------------------------------------------------

class Profile(models.Model):
    TIPO_USUARIO = (
        ('candidato', 'Candidato'),
        ('empresa', 'Empresa'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)
    
    # Nome para Candidatos / Razão Social para Empresas
    nome_completo = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nome ou Razão Social")
    
    # CNPJ apenas para Empresas
    cnpj = models.CharField(max_length=18, null=True, blank=True, verbose_name="CNPJ")
    
    criado_em = models.DateTimeField(auto_now_add=True)

    disponivel_para_alocacao = models.BooleanField(default=False, verbose_name="Banco de Talentos TrabalheJá")

    def __str__(self):
        return f"{self.nome_completo} ({self.get_tipo_display()})"

# ----------------------------------------------------------------------
# PERFIL COMPLETO DO CANDIDATO (CURRÍCULO)
# ----------------------------------------------------------------------

class PerfilCandidato(models.Model):
    # Relacionamento Interno
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --- 1. IDENTIDADE E APRESENTAÇÃO ---
    foto = models.ImageField(
        upload_to='fotos_perfil/', 
        blank=True, 
        null=True,
        verbose_name="Foto de Perfil"
    )
    titulo_profissional = models.CharField(
        max_length=150,
        help_text="Ex: Desenvolvedor Full Stack PHP / React",
        verbose_name="Título Profissional"
    )
    resumo_profissional = models.TextField(
        verbose_name="Resumo Profissional",
        help_text="Fale um pouco sobre sua trajetória e principais competências."
    )

    # --- 2. CONTATO ---
    email_contato = models.EmailField(
        max_length=255, 
        null=True, 
        blank=True,
        verbose_name="E-mail de Contato",
        help_text="Email que os recrutadores usarão para falar com você."
    )
    whatsapp = models.CharField(
        max_length=20,
        verbose_name="WhatsApp/Telefone"
    )
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    github = models.URLField(blank=True, verbose_name="GitHub")
    portfolio = models.URLField(blank=True, verbose_name="Portfólio/Site")

    # --- 3. LOCALIZAÇÃO ---
    ESTADOS_CHOICES = (
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    )
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS_CHOICES,
        help_text="Sigla (Ex: SP, RJ)",
        verbose_name="Estado (UF)"
    )

    # --- 4. PREFERÊNCIAS E EXPECTATIVAS ---
    modelo_trabalho = models.CharField(
        max_length=20,
        choices=(
            ('remoto', 'Remoto'),
            ('hibrido', 'Híbrido'),
            ('presencial', 'Presencial'),
        ),
        verbose_name="Modelo de Trabalho Preferido"
    )
    disponibilidade = models.CharField(
        max_length=20,
        choices=(
            ('imediata', 'Imediata'),
            ('15_dias', '15 dias'),
            ('30_dias', '30 dias'),
        ),
        verbose_name="Disponibilidade para Início"
    )
    pretensao_salarial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Pretensão Salarial"
    )

    def save(self, *args, **kwargs):
        if self.estado:
            self.estado = self.estado.upper()
        super(PerfilCandidato, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.titulo_profissional}"
    
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
    GRAU_CHOICES = (
        ('ensino_medio', 'Ensino Médio'),
        ('tecnico', 'Curso Técnico'),
        ('tecnologo', 'Graduação Tecnológica (Tecnólogo)'),
        ('bacharelado', 'Bacharelado'),
        ('licenciatura', 'Licenciatura'),
        ('pos_graduacao', 'Pós-Graduação (Lato Sensu)'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
        ('mba', 'MBA'),
    )

    STATUS_CHOICES = (
        ('concluido', 'Concluído'),
        ('cursando', 'Cursando'),
        ('interrompido', 'Interrompido'),
    )

    candidato = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formacoes')
    grau = models.CharField(max_length=50, choices=GRAU_CHOICES)
    curso = models.CharField(max_length=150)
    instituicao = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    # Dica: Adicione datas para ficar mais profissional
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.grau} em {self.curso}"


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

    ativa = models.BooleanField(default=True)

    def __str__(self):
        # Tenta pegar o nome da empresa no perfil, se não existir usa o email
        nome_empresa = getattr(self.empresa.profile, 'nome_completo', self.empresa.email)
        return f"{self.titulo} - {nome_empresa}"

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
