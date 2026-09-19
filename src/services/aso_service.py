from datetime import datetime, timedelta
from src.database.connection import get_connection


# ==========================================
# GESTÃO DE COLABORADORES
# ==========================================

def cadastrar_colaborador(nome: str, cpf: str, cargo: str, setor: str, data_admissao: str) -> int:
    """
    Cadastra um novo colaborador no sistema.
    :param data_admissao: Formato 'YYYY-MM-DD'
    :return: ID do colaborador cadastrado
    """
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    
    query = """
        INSERT INTO colaboradores (nome, cpf, cargo, setor, data_admissao)
        VALUES (?, ?, ?, ?, ?)
    """
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (nome.strip(), cpf_limpo, cargo.strip(), setor.strip(), data_admissao))
        conn.commit()
        return cursor.lastrowid


def listar_colaboradores(apenas_ativos: bool = True) -> list:
    """Retorna a lista de colaboradores cadastrados."""
    query = "SELECT * FROM colaboradores"
    if apenas_ativos:
        query += " WHERE status = 'Ativo'"
    query += " ORDER BY nome ASC"

    with get_connection() as conn:
        cursor = conn.cursor()
        return [dict(row) for row in cursor.execute(query).fetchall()]


def buscar_colaborador_por_id(colaborador_id: int) -> dict | None:
    """Busca os dados de um colaborador específico pelo ID."""
    query = "SELECT * FROM colaboradores WHERE id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        row = cursor.execute(query, (colaborador_id,)).fetchone()
        return dict(row) if row else None


# ==========================================
# GESTÃO DE ASOS
# ==========================================

def calcular_data_vencimento(data_realizacao: str, periodicidade_meses: int = 12) -> str:
    """Calcula a data limite de vencimento com base nos meses de validade."""
    data_dt = datetime.strptime(data_realizacao, "%Y-%m-%d")
    data_vencimento = data_dt + timedelta(days=periodicidade_meses * 30.4375)
    return data_vencimento.strftime("%Y-%m-%d")


def lancar_aso(
    colaborador_id: int,
    tipo_exame: str,
    data_realizacao: str,
    resultado: str,
    medico_crm: str,
    periodicidade_meses: int = 12,
    data_vencimento: str | None = None
) -> int:
    """
    Registra um novo ASO para o colaborador.
    Tipos permitidos: 'Admissional', 'Periódico', 'Demissional', 'Retorno ao Trabalho', 'Mudança de Risco'
    """
    tipos_validos = [
        'Admissional', 'Periódico', 'Demissional', 
        'Retorno ao Trabalho', 'Mudança de Risco'
    ]
    if tipo_exame not in tipos_validos:
        raise ValueError(f"Tipo de exame inválido. Use um dos seguintes: {tipos_validos}")

    if resultado not in ['Apto', 'Inapto']:
        raise ValueError("Resultado deve ser 'Apto' ou 'Inapto'.")

    if not data_vencimento:
        data_vencimento = calcular_data_vencimento(data_realizacao, periodicidade_meses)

    query = """
        INSERT INTO asos (
            colaborador_id, tipo_exame, data_realizacao, 
            data_vencimento, resultado, medico_crm
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (
            colaborador_id,
            tipo_exame,
            data_realizacao,
            data_vencimento,
            resultado,
            medico_crm.strip()
        ))
        conn.commit()
        return cursor.lastrowid


def obter_historico_asos(colaborador_id: int) -> list:
    """Retorna todos os ASOs registrados para um colaborador ordenados pelo mais recente."""
    query = """
        SELECT * FROM asos 
        WHERE colaborador_id = ? 
        ORDER BY data_realizacao DESC
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        return [dict(row) for row in cursor.execute(query, (colaborador_id,)).fetchall()]