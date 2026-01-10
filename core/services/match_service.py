# core/services/match_service.py

def calcular_match(vaga, candidato):
    score = 0

    # Modelo de trabalho
    if candidato.modelo_trabalho == vaga.modelo_trabalho:
        score += 20

    # Pretensão salarial
    if candidato.pretensao_salarial and vaga.salario_max:
        if candidato.pretensao_salarial <= vaga.salario_max:
            score += 20

    # Experiência
    total_exp = candidato.user.experiencias.count()
    if total_exp >= 4:
        score += 20
    elif total_exp >= 2:
        score += 12
    elif total_exp >= 1:
        score += 5

    # Formação
    if candidato.user.formacoes.filter(status='concluido').exists():
        score += 15
    elif candidato.user.formacoes.exists():
        score += 8

    return min(score, 100)
