# 🚀 Trabalhe Já - Marketplace de Oportunidades

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

O **Trabalhe Já** é uma plataforma moderna de recrutamento e seleção que conecta talentos a oportunidades de forma assertiva. O projeto conta com perfis distintos para Candidatos e Empresas, gestão de currículos com fotos e um marketplace de vagas responsivo.

## ✨ Funcionalidades

### 👤 Para Candidatos
- **Perfil Profissional:** Cadastro de currículo completo (Resumo, Experiências, Formação e Competências).
- **Foto de Perfil:** Upload de foto com tratamento dinâmico.
- **Marketplace:** Visualização de vagas em formato de cards "Premium".
- **Candidatura:** Envio de interesse para vagas específicas.

### 🏢 Para Empresas
- **Gestão de Vagas:** Cadastro detalhado de oportunidades (Modelo, Contrato, Salário, Requisitos).
- **Dashboard de Candidaturas:** (Em desenvolvimento) Visualização de quem se aplicou às vagas.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.12 + Django Framework.
- **Frontend:** HTML5, CSS3 (Design Premium/Impact), Bootstrap 5.
- **Banco de Dados:** SQLite (Desenvolvimento).
- **Imagens:** Pillow (Processamento de fotos).

---

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar o ambiente local:

1. Clonar o Repositório
git clone [https://github.com/caiohlucena/trabalheja.git](https://github.com/caiohlucena/trabalheja.git)
cd trabalheja

2. Criar Ambiente Virtual (VENV)
python -m venv venv

3. Ativar a VENV
Windows:
.\venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

4. Instalar Dependências
pip install -r requirements.txt

5. Configurar o Banco de Dados
python manage.py makemigrations
python manage.py migrate

6. Criar um Superusuário (Admin)
python manage.py createsuperuser

7. Rodar o Servidor

python manage.py runserver
Acesse em: http://127.0.0.1:8000