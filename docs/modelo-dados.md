# 🗄️ Modelo de Dados - Controle de Exames SST

## 1. Entidades e Campos

### Tabela: `colaboradores`
| Campo | Tipo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `id` | PK (Int/UUID) | Chave primária | 1 |
| `nome` | Varchar(100) | Nome completo | João da Silva |
| `cpf` | Varchar(11) | CPF (apenas números) | 12345678900 |
| `cargo` | Varchar(50) | Cargo atual | Operador de Produção |
| `setor` | Varchar(50) | Setor / Departamento | Panificação |
| `data_admissao` | Date | Data de contratação | 2024-01-15 |
| `status` | Enum | Ativo / Inativo | Ativo |

### Tabela: `exames`
| Campo | Tipo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `id` | PK (Int/UUID) | Chave primária | 10 |
| `nome_exame` | Varchar(100) | Nome do exame | Audiometria Tonal |
| `periodicidade_meses` | Int | Validade padrão em meses | 12 |

### Tabela: `asos` (Registros de Saúde)
| Campo | Tipo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `id` | PK (Int/UUID) | Chave primária | 100 |
| `colaborador_id` | FK (`colaboradores.id`) | ID do colaborador | 1 |
| `tipo_exame` | Enum | Admissional / Periódico / etc. | Periódico |
| `data_realizacao` | Date | Data em que fez o exame | 2026-03-10 |
| `data_vencimento` | Date | Data limite de validade | 2027-03-10 |
| `resultado` | Enum | Apto / Inapto | Apto |
| `medico_crm` | Varchar(20) | CRM e UF do médico | 12345/PE |