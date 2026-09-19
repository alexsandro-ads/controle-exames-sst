-- Tabela de Colaboradores
CREATE TABLE IF NOT EXISTS colaboradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    cargo TEXT NOT NULL,
    setor TEXT NOT NULL,
    data_admissao DATE NOT NULL,
    status TEXT DEFAULT 'Ativo' CHECK (status IN ('Ativo', 'Inativo'))
);

-- Tabela de Exames Complementares / ASOs
CREATE TABLE IF NOT EXISTS asos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colaborador_id INTEGER NOT NULL,
    tipo_exame TEXT NOT NULL CHECK (
        tipo_exame IN ('Admissional', 'Periódico', 'Demissional', 'Retorno ao Trabalho', 'Mudança de Risco')
    ),
    data_realizacao DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    resultado TEXT NOT NULL CHECK (resultado IN ('Apto', 'Inapto')),
    medico_crm TEXT NOT NULL,
    FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id) ON DELETE CASCADE
);