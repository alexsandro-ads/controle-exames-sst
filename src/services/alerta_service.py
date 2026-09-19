from datetime import datetime, date
from src.database.connection import get_connection


def obter_status_exames_colaboradores() -> list:
    """
    Retorna a lista de todos os colaboradores ativos com a informação do último ASO realizado
    e a quantidade de dias restantes até o vencimento.
    """
    query = """
        SELECT 
            c.id AS colaborador_id,
            c.nome,
            c.cpf,
            c.cargo,
            c.setor,
            a.id AS aso_id,
            a.tipo_exame,
            a.data_realizacao,
            a.data_vencimento,
            a.resultado,
            a.medico_crm
        FROM colaboradores c
        LEFT JOIN asos a ON a.id = (
            SELECT id FROM asos 
            WHERE colaborador_id = c.id 
            ORDER BY data_realizacao DESC, id DESC 
            LIMIT 1
        )
        WHERE c.status = 'Ativo'
        ORDER BY a.data_vencimento ASC NULLS LAST
    """

    hoje = date.today()
    resultado = []

    with get_connection() as conn:
        cursor = conn.cursor()
        rows = [dict(row) for row in cursor.execute(query).fetchall()]

    for row in rows:
        if row["data_vencimento"]:
            data_venc = datetime.strptime(row["data_vencimento"], "%Y-%m-%d").date()
            dias_restantes = (data_venc - hoje).days

            if dias_restantes < 0:
                categoria = "Vencido"
                cor_alerta = "vermelho"
            elif dias_restantes <= 30:
                categoria = "A vencer em 30 dias"
                cor_alerta = "laranja_escuro"
            elif dias_restantes <= 60:
                categoria = "A vencer em 60 dias"
                cor_alerta = "laranja"
            elif dias_restantes <= 90:
                categoria = "A vencer em 90 dias"
                cor_alerta = "amarelo"
            else:
                categoria = "Em dia"
                cor_alerta = "verde"
        else:
            dias_restantes = None
            categoria = "Sem ASO cadastrado"
            cor_alerta = "cinza"

        row["dias_restantes"] = dias_restantes
        row["status_alerta"] = categoria
        row["cor_alerta"] = cor_alerta
        resultado.append(row)

    return resultado


def filtrar_alertas_por_janela(dias: int = 30) -> list:
    """
    Filtra colaboradores que possuem ASO vencido ou a vencer nos próximos N dias (ex: 30, 60, 90).
    """
    todos = obter_status_exames_colaboradores()
    return [
        c for c in todos 
        if c["dias_restantes"] is not None and c["dias_restantes"] <= dias
    ]


def obter_resumo_dashboard() -> dict:
    """
    Retorna métricas consolidadas para uso no painel/dashboard.
    """
    todos = obter_status_exames_colaboradores()

    resumo = {
        "total_colaboradores": len(todos),
        "vencidos": 0,
        "vencem_30_dias": 0,
        "vencem_60_dias": 0,
        "vencem_90_dias": 0,
        "em_dia": 0,
        "sem_aso": 0,
    }

    for item in todos:
        cat = item["status_alerta"]
        if cat == "Vencido":
            resumo["vencidos"] += 1
        elif cat == "A vencer em 30 dias":
            resumo["vencem_30_dias"] += 1
        elif cat == "A vencer em 60 dias":
            resumo["vencem_60_dias"] += 1
        elif cat == "A vencer em 90 dias":
            resumo["vencem_90_dias"] += 1
        elif cat == "Em dia":
            resumo["em_dia"] += 1
        else:
            resumo["sem_aso"] += 1

    return resumo