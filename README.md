<div align="center">

# ⚡Finly — Gestão Financeira

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5/CSS3](https://img.shields.io/badge/UI/UX-Dark%20Theme-1572B6?style=for-the-badge)

Uma aplicação Full Stack completa para controle de finanças pessoais, desenvolvida com foco em performance, experiência do usuário (UX) e arquitetura de software escalável.

</div>

---

## 📌 Visão Geral do Projeto

O **Finly** foi desenvolvido para simplificar o gerenciamento de receitas e despesas diárias. O projeto conta com uma API REST robusta e assíncrona construída em **FastAPI**, integração com banco de dados **SQLite**, e uma interface Web reativa *(SPA)* criada com **HTML5, CSS3 puro (com suporte a Dark Mode)** e **JavaScript Vanilla**.

> **Destaques do projeto:**
> - Autenticação segura de usuários.
> - Separação clara de responsabilidades (Front-end e Back-end descentralizados).
> - Interface limpa com cálculo automatizado de saldos e transações em tempo real.


---

## 🚀 Funcionalidades

- [x] **Autenticação & Controle de Acesso:** Sistema de Login e Cadastro de usuários.
- [x] **Gestão de Transações:** Cadastro de receitas e despesas com descrição, valor, categoria e data.
- [x] **Cálculo Automático de Balanço:** Atualização dinâmica de Entradas, Saídas e Saldo Total.
- [x] **Histórico Detalhado:** Tabela organizada com listagem e remoção rápida de transações.
- [x] **Design Responsivo & Dark Mode:** Interface elegante e adaptável a telas de desktop e dispositivos móveis.

---

## 🛠️ Tecnologias Utilizadas

### **Back-end**
- **Python 3.10+**
- **FastAPI**: Framework web moderno, de alta performance para construção de APIs REST.
- **Uvicorn**: Servidor ASGI para execução assíncrona da aplicação.
- **SQLite / SQLAlchemy**: Banco de dados relacional leve e ORM para manipulação de dados.
- **Pydantic**: Validação de dados e tipagem estrita de schemas.

### **Front-end**
- **HTML5 Semantic**: Estrutura acessível e bem definida.
- **CSS3 Moderno**: Variáveis CSS, Flexbox, CSS Grid, efeito Glassmorphism e responsividade.
- **JavaScript (ES6+)**: Manipulação nativa do DOM, consumo de API assíncrona via `fetch`.

---

## 📂 Estrutura do Projeto

```text
finance-app/
│
├── backend/
│   ├── main.py            # Instância do FastAPI, rotas da API e regras de negócio
│   ├── database.py        # Configuração da conexão com o SQLite
│   ├── models.py          # Modelos de dados / Tabelas ORM
│   └── schemas.py         # Schemas de validação Pydantic
│
├── frontend/
│   ├── index.html         # Estrutura principal da aplicação (SPA)
│   ├── styles.css         # Estilização visual (Paleta Dark/Neon)
│   ├── app.js             # Lógica do front-end e integração REST
│   └── logo.png           # Identidade visual do Finly
│
├── .gitignore
├── README.md
└── requirements.txt       # Dependências do projeto Python
