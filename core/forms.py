from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Vaga, PerfilCandidato, ExperienciaProfissional, FormacaoAcademica

class CadastroForm(forms.ModelForm):
    nome_completo = forms.CharField(
        label="Nome Completo / Razão Social",
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu nome ou o nome da empresa', 
            'class': 'form-control'
        })
    )

    tipo = forms.ChoiceField(
        choices=Profile.TIPO_USUARIO,
        label="Eu sou:",
        widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'toggleCNPJ(this)'})
    )

    cnpj = forms.CharField(
        label="CNPJ",
        required=False,  # Validaremos manualmente no clean()
        widget=forms.TextInput(attrs={
            'placeholder': '00.000.000/0000-00', 
            'class': 'form-control'
        })
    )

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Crie uma senha forte', 'class': 'form-control'})
    )

    confirm_password = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'seu@email.com', 'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(username=email).exists():
            raise ValidationError('Já existe um usuário com este e-mail.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo")
        cnpj = cleaned_data.get("cnpj")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # 1. Validação de Senha
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")

        # 2. Validação Condicional de CNPJ
        if tipo == 'empresa' and not cnpj:
            self.add_error('cnpj', "Empresas devem obrigatoriamente informar o CNPJ.")
            
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email').lower()
        
        user.username = email
        user.email = email
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()
            # Criar ou atualizar o perfil vinculado
            profile, created = Profile.objects.get_or_create(user=user)
            profile.tipo = self.cleaned_data.get('tipo')
            profile.nome_completo = self.cleaned_data.get('nome_completo')
            
            # Salva o CNPJ apenas se for empresa
            if profile.tipo == 'empresa':
                profile.cnpj = self.cleaned_data.get('cnpj')
            else:
                profile.cnpj = None
                
            profile.save()
            
        return user

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        exclude = ['empresa', 'criada_em', 'data_publicacao']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: Desenvolvedor Senior', 'class': 'form-control'}),
            'codigo_vaga': forms.TextInput(attrs={'placeholder': 'Ex: TI-2024-001', 'class': 'form-control'}),
            'salario_min': forms.NumberInput(attrs={'placeholder': 'R$ Mínimo', 'class': 'form-control'}),
            'salario_max': forms.NumberInput(attrs={'placeholder': 'R$ Máximo', 'class': 'form-control'}),
            'resumo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'responsabilidades': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'requisitos_obrigatorios': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'cultura_empresa': forms.URLInput(attrs={'placeholder': 'Link do vídeo ou site', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        min_sal = cleaned_data.get("salario_min")
        max_sal = cleaned_data.get("salario_max")

        if min_sal and max_sal and max_sal < min_sal:
            self.add_error('salario_max', "O salário máximo não pode ser menor que o mínimo.")
        return cleaned_data

class PerfilCandidatoForm(forms.ModelForm):
    class Meta:
        model = PerfilCandidato
        exclude = ['user']
        
        widgets = {
            'email_contato': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@contato.com'}),
            'titulo_profissional': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}), # Alterado para select
            'resumo_profissional': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '(00) 00000-0000', 'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'URL do LinkedIn', 'class': 'form-control'}),
            'github': forms.URLInput(attrs={'placeholder': 'URL do GitHub', 'class': 'form-control'}),
            'portfolio': forms.URLInput(attrs={'placeholder': 'URL do Portfólio', 'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'pretensao_salarial': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponibilidade': forms.Select(attrs={'class': 'form-select'}),
            'modelo_trabalho': forms.Select(attrs={'class': 'form-select'}),
        }

class ExperienciaProfissionalForm(forms.ModelForm):
    class Meta:
        model = ExperienciaProfissional
        fields = ['cargo', 'empresa', 'data_inicio', 'data_fim', 'atual', 'descricao']

        widgets = {
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'atual': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva suas conquistas...', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")
        atual = cleaned_data.get("atual")

        if data_inicio and not atual:
            if not data_fim:
                self.add_error('data_fim', "Informe a data de término ou marque como atual.")
            elif data_fim < data_inicio:
                self.add_error('data_fim', "A data de término não pode ser anterior ao início.")
        return cleaned_data

class FormacaoAcademicaForm(forms.ModelForm):
    class Meta:
        model = FormacaoAcademica
        fields = ['grau', 'curso', 'instituicao', 'status', 'data_inicio', 'data_fim'] # Adicionados
        
        widgets = {
            'grau': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Análise e Desenvolvimento de Sistemas'}),
            'instituicao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: USP, FIAP, Alura'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }