# Projeto Individual - Case Tracker

Uma aplicação web simples de gerenciamento de casos investigativos construída com FastAPI, HTMX, HTML, CSS, JavaScript e SQL.

O objetivo do projeto é demonstrar o uso de tecnologias web modernas para implementar uma aplicação web CRUD básica com modelos de banco de dados relacionais e interações dinâmicas usando HTMX.

Esse projeto foi desenvolvido como parte do curso de WebMac.

---

# O que o projeto faz

Case Tracker é uma aplicação web idealizada para auxiliar a organização de casos investigativos e suas evidências associadas.

Usuários podem:

* Criar e gerenciar casos investigativos
* Adicionar evidências relacionadas a cada caso
* Editar informações de casos e descrições de evidências
* Deletar entradas de casos ou evidências
* Buscar casos por título

O sistema modela a relação entre casos e evidências, simulando um fluxo de trabalho investigativo simplificado.

---

# Por que esse projeto é útil

Processos investigativos frequentemente envolvem gerenciar grandes quantidades de informação estruturada como casos, suspeitos, evidências e relatórios.

Esse projeto demonstra como uma simples aplicação web pode ajudar a estruturar e gerenciar essa informação eficientemente usando:

* Uma **base de dados relacional**
* Um **framework backend moderno**
* **Interações frontend dinâmicas sem frameworks de JavaScript pesados**

Também serve como exemplo prático de construção de aplicações web interativas usando FastAPI e HTMX.

---

# Tecnologias usadas

| Tecnologia | Propósito |
|-----------|--------|
| FastAPI | Framework web backend |
| HTMX | Interações frontend dinâmicas e operações CRUD |
| HTML | Estrutura das páginas web |
| CSS | Estilização e layout responsivo |
| JavaScript | Comportamento do lado do cliente adicional |
| SQL | Base de dados relacional |

---

# Estrutura da Base de Dados

A aplicação usa dois modelos principais:

## Caso

Representa um caso investigativo.

Campos:

* id
* título
* descrição
* status *(aberto, sob investigação, fechado)*

## Evidência

Representa uma evidência associada com um caso

Campos:

* id
* descrição
* tipo
* id_caso

## Relação 

Caso (1) ------- (N) Evidência

Cada caso pode conter múltiplas evidências

---

# Features da aplicação

A aplicação implementa as seguintes features usando **operações CRUD HTMX**:

### Create

* Adiciona novos casos investigativos
* Adiciona novas entradas de evidências

### Read

* Lista casos existentes
* Visualiza evidência associada a um caso

### Update

* Atualiza status do caso
* Edita descrição da evidência

### Delete

* Remove casos
* Remove entradas de evidências

### Feature extra:

* Busca casos por título

---

# Telas da Aplicação

A aplicação contém pelo menos duas telas principais:

## Gerenciamento de Casos

Permite aos usuários criar, editar, buscar e deletar casos de investigação.

## Gerenciamento de Evidência

Permite aos usuários gerenciar evidências associadas a casos específicos.

Todas as intefaces são **responsivas para dispositivos desktop e mobile**.

---

# Como executar o projeto

### 1. Clone o repositório
  git clone https://github.com/your-username/case-tracker.git

### 2. Entre na pasta do projeto
   cd case-tracker

### 3. Instale as dependências
   pip install -r requirements.txt

### 4. Execute a aplicação
   uvicorn app.main:app --reload

### 5. Abra no browser
   http://127.0.0.1:8000

---

# Conseguindo ajuda

Se você encontrar problemas ao executar o projeto, você pode:
* verificar a documentação do FastAPI
* verificar as dependências do Python
* confirmar que a base de dados foi criada corretamente

---

# Autor

Desenvolvido por um estudante como parte do projeto do curso WebMac.

---
