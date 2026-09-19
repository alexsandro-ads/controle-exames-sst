from src.database.connection import init_db
from src.services.aso_service import (
    cadastrar_colaborador,
    lancar_aso,
    listar_colaboradores,
    obter_historico_asos,
)

def executar_teste():
    print("--- 1. Inicializando o Banco de Dados ---")
    init_db()

    print("\n--- 2. Cadastrando um Colaborador ---")
    try:
        colab_id = cadastrar_colaborador(
            nome="Carlos Eduardo",
            cpf="12345678900",
            cargo="Operador de Máquinas",
            setor="Produção",
            data_admissao="2026-01-10"
        )
        print(f"✅ Colaborador cadastrado com sucesso! ID: {colab_id}")
    except Exception as e:
        print(f"ℹ️ Colaborador já cadastrado ou erro: {e}")
        # Recupera o ID do primeiro colaborador para continuar o teste
        colaboradores = listar_colaboradores()
        colab_id = colaboradores[0]["id"] if colaboradores else 1

    print("\n--- 3. Lançando um ASO Periódico ---")
    aso_id = lancar_aso(
        colaborador_id=colab_id,
        tipo_exame="Periódico",
        data_realizacao="2026-09-18",
        resultado="Apto",
        medico_crm="12345/PE",
        periodicidade_meses=12
    )
    print(f"✅ ASO registrado com sucesso! ID: {aso_id}")

    print("\n--- 4. Consultando o Histórico de ASOs ---")
    historico = obter_historico_asos(colab_id)
    for registro in historico:
        print(
            f"- Tipo: {registro['tipo_exame']} | Realização: {registro['data_realizacao']} "
            f"| Vencimento: {registro['data_vencimento']} | Resultado: {registro['resultado']}"
        )

if __name__ == "__main__":
    executar_teste()
