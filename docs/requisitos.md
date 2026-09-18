# 📄 Requisitos do Sistema - Controle de Exames SST

## 1. Visão Geral
Sistema voltado para controle e monitoramento de Saúde Ocupacional, visando automatizar o acompanhamento dos ASOs (Atestado de Saúde Ocupacional) e exames complementares de acordo com o PCMSO (NR-07).

## 2. Requisitos Funcionais (RF)
- **RF-01:** Cadastrar colaboradores (Nome, CPF, Data de Nascimento, Cargo, Setor, Data de Admissão).
- **RF-02:** Cadastrar exames e indicar a periodicidade recomendada (anual, semestral, bianual, etc.).
- **RF-03:** Registrar o lançamento de ASO emitido (Tipo de exame, Data de realização, Data de vencimento, Médico examinador, CRM, Resultado/Aptidão).
- **RF-04:** Gerar alertas visuais ou relatórios de exames a vencer nos intervalos de 60, 30 e 15 dias.
- **RF-05:** Permitir a filtragem de colaboradores por status de aptidão (Apto, Inapto, Pendente/Vencido).

## 3. Regras de Negócio (RN)
- **RN-01 (Tipos de Exame):** Os exames devem ser classificados obrigatoriamente como: *Admissional*, *Periódico*, *Demissional*, *Retorno ao Trabalho* ou *Mudança de Risco Ocupacional*.
- **RN-02 (Cálculo de Vencimento):** A data de vencimento do ASO deve ser calculada automaticamente com base na periodicidade atrelada ao cargo/risco ocupacional.
- **RN-03 (Histórico):** Nenhum registro de ASO antigo pode ser deletado; o histórico de saúde ocupacional do colaborador deve ser preservado.