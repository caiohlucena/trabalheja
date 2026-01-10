from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Vaga, PerfilCandidato, ExperienciaProfissional, FormacaoAcademica

class CadastroForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=Profile.TIPO_USUARIO,
        label="Eu sou:",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Crie uma senha forte'})
    )

    confirm_password = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'})
    )

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'seu@email.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(username=email).exists():
            raise ValidationError('Já existe um usuário com este e-mail.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email').lower()
        
        user.username = email
        user.email = email
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.tipo = self.cleaned_data.get('tipo')
            profile.save()
        return user

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        exclude = ['empresa', 'criada_em', 'data_publicacao']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: Desenvolvedor Senior'}),
            'codigo_vaga': forms.TextInput(attrs={'placeholder': 'Ex: TI-2024-001'}),
            'salario_min': forms.NumberInput(attrs={'placeholder': 'R$ Mínimo'}),
            'salario_max': forms.NumberInput(attrs={'placeholder': 'R$ Máximo'}),
            'resumo': forms.Textarea(attrs={'rows': 3}),
            'responsabilidades': forms.Textarea(attrs={'rows': 4}),
            'requisitos_obrigatorios': forms.Textarea(attrs={'rows': 4}),
            'cultura_empresa': forms.URLInput(attrs={'placeholder': 'Link do vídeo ou site da cultura'}),
        }

class PerfilCandidatoForm(forms.ModelForm):
    class Meta:
        model = PerfilCandidato
        exclude = ['user'] # Geralmente o usuário é vinculado automaticamente na view
        
        widgets = {
            'resumo_profissional': forms.Textarea(attrs={'rows': 4}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/seu-perfil'}),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/seu-perfil'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}), # Adicionado para estilo
        }

class ExperienciaProfissionalForm(forms.ModelForm):
    class Meta:
        model = ExperienciaProfissional
        fields = ['cargo', 'empresa', 'data_inicio', 'data_fim', 'atual', 'descricao']

        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'atual': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva suas conquistas...'}),
        }

class FormacaoAcademicaForm(forms.ModelForm):
    class Meta:
        model = FormacaoAcademica
        fields = ['grau', 'curso', 'instituicao', 'status']