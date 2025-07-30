# 🏥 Sistema de Gestão Médica

Este projeto é um sistema completo de gerenciamento de pacientes, médicos e consultas médicas, desenvolvido como trabalho final da disciplina **Banco de Dados II** (Curso de Análise e Desenvolvimento de Sistemas - 2025.1).
---

## 📌 Funcionalidades

✅ Cadastro, atualização, busca e remoção de **pacientes**  
✅ Cadastro e gerenciamento de **médicos** com especialidades  
✅ Agendamento e listagem de **consultas médicas futuras**  
✅ Filtro de consultas por **nome** e por **data mínima**  
✅ Interface gráfica com **CustomTkinter** estilizada e responsiva  
✅ Integração completa com banco de dados **MySQL**

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **MySQL**
- **SQLAlchemy** (ORM)
- **CustomTkinter** (interface gráfica)
- **Tkinter.messagebox** (alertas)
- **Procedures, Triggers, Views e Joins no MySQL**

---

## 💾 Estrutura do Projeto

Projeto Final/

│
├── config/

│ └── db.py # Conexão com o banco de dados

│
├── controllers/

│ ├── paciente_controller.py

│ ├── medico_controller.py

│ └── consulta_controller.py

│ └──especialidade_controller.py
│

├── models/

│ ├── paciente.py

│ ├── medico.py

│ ├── consulta.py

│ ├── clinica.py

│ └── especialidade.py

│ └──__init__.py

│
├── gui.py # Arquivo principal com as telas (CustomTkinter)

├── README.md # Documentação do projeto

└── requirements.txt # Dependências do projeto

## 🧠 Recursos Avançados em Banco de Dados Utilizados

| Recurso MySQL     | Onde foi utilizado                                 |
|-------------------|-----------------------------------------------------|
| ✅ **Procedures**   | `agendar_consulta` usada no agendamento via `CALL` |
| ✅ **Triggers**     | impedir exclusão se houver dependência         |
| ✅ **Views**        | `vw_consultas_futuras` para exibir consultas       |
| ✅ **Joins**        | View junta dados de consultas, médicos e pacientes |
| ✅ **Transactions** | Com `commit()` e `rollback()` em ações críticas    |
| ✅ **Funções SQL**  | `NOW()`, filtros de datas e LIKE com `LOWER()`     |

💡 Como Executar o Projeto

1. Clone este repositório:
git clone https://github.com/seu-usuario/nome-repositorio.git

2 - Instale as dependências:
- pip install -r requirements.txt
- 
3 - Configure seu banco de dados MySQL (ver config/db.py).
  
4 - Execute o sistema:
- python gui.py

  
👨‍💻 Desenvolvedor

Pedro Henrique Vogado Maia

Curso: Análise e Desenvolvimento de Sistemas – 2025.1

Disciplina: Banco de Dados II

Instituição: Instituto Federal de Ciências e Tecnologia do Pauí - Campos Corrente




🧾 LICENÇA
MIT License

Copyright (c) 2025 Pedro Henrique Vogado Maia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Este projeto está licenciado sob os termos da Licença MIT. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.

