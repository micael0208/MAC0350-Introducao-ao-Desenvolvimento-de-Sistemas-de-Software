CREATE TABLE caso (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('aberto', 'investigando', 'fechado')) NOT NULL,
    classificacao TEXT NOT NULL CHECK(classificacao IN ('homicidio', 'roubo', 'cyber', 'narcoticos')),
    prioridade TEXT NOT NULL CHECK(prioridade IN ('baixa', 'moderada', 'elevada')),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evidencia (
    id INTEGER PRIMARY KEY,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL CHECK(categoria IN ('biologica', 'digital', 'documental', 'fisica', 'latente')),
    caso_id INTEGER NOT NULL,
    status_atual TEXT NOT NULL CHECK(status_atual IN ('coletado', 'em_analise', 'armazenado')),
    coletado_onde TEXT,
    coletado_quando TIMESTAMP NOT NULL,

    FOREIGN KEY (caso_id) REFERENCES caso(id) ON DELETE CASCADE
);
