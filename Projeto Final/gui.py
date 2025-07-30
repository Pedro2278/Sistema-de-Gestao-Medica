import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from config.db import SessionLocal
from controllers import paciente_controller, consulta_controller
from controllers import medico_controller
from config.db import SessionLocal  


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

db = SessionLocal()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão Médica")
        self.geometry("700x600")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Adicione aqui todas as frames, incluindo as novas ConsultaListFrame e ConsultaCancelFrame
        frames_to_create = [
            MenuFrame,
            PacienteMenuFrame,
            PacienteCreateFrame,
            PacienteListFrame,
            PacienteUpdateFrame,
            PacienteDeleteFrame,
            MedicoFrame,
            ConsultaMenuFrame,
            ConsultaListFrame,     
        ]

        for F in frames_to_create:
            try:
                frame = F(self.container, self, db)
            except TypeError:
                # Para frames que não aceitam db no construtor
                frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MenuFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        title = ctk.CTkLabel(self, text="Sistema de Gestão Médica", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=40)

        btn_paciente = ctk.CTkButton(self, text="Pacientes", command=lambda: app.show_frame(PacienteMenuFrame))
        btn_paciente.pack(pady=10, ipadx=30, ipady=10)

        btn_medico = ctk.CTkButton(self, text="Médicos", command=lambda: app.show_frame(MedicoFrame))
        btn_medico.pack(pady=10, ipadx=30, ipady=10)

        btn_consulta = ctk.CTkButton(self, text="Consultas", command=lambda: app.show_frame(ConsultaMenuFrame))
        btn_consulta.pack(pady=10, ipadx=30, ipady=10)


class ScrollableFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Criar canvas e scrollbar vertical
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=self._bg_color)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

# ---------- Paciente ----------

class PacienteMenuFrame(ctk.CTkFrame):
    def __init__(self, parent, app, db):
        super().__init__(parent)
        self.app = app
        self.db = db

        title = ctk.CTkLabel(self, text="Menu Pacientes", font=ctk.CTkFont(size=22, weight="bold"))
        title.pack(pady=20)

        btn_criar = ctk.CTkButton(self, text="Criar Paciente", command=lambda: app.show_frame(PacienteCreateFrame))
        btn_criar.pack(pady=10, ipadx=20, ipady=8)

        btn_listar = ctk.CTkButton(self, text="Listar Pacientes", command=lambda: app.show_frame(PacienteListFrame))
        btn_listar.pack(pady=10, ipadx=20, ipady=8)

        btn_atualizar = ctk.CTkButton(self, text="Atualizar Paciente", command=lambda: app.show_frame(PacienteUpdateFrame))
        btn_atualizar.pack(pady=10, ipadx=20, ipady=8)

        btn_deletar = ctk.CTkButton(self, text="Deletar Paciente", command=lambda: app.show_frame(PacienteDeleteFrame))
        btn_deletar.pack(pady=10, ipadx=20, ipady=8)

        btn_voltar = ctk.CTkButton(self, text="Voltar", command=lambda: app.show_frame(MenuFrame))
        btn_voltar.pack(pady=30, ipadx=20, ipady=8)

class PacienteCreateFrame(ctk.CTkFrame):
    def __init__(self, parent, app, db):
        super().__init__(parent)
        self.app = app
        self.db = db

        ctk.CTkLabel(self, text="Criar Paciente", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=lambda: app.show_frame(PacienteMenuFrame)).pack(anchor="nw", padx=10, pady=10)

        self.nome_entry = ctk.CTkEntry(self, placeholder_text="Nome")
        self.nome_entry.pack(pady=5, padx=20, fill="x")
        self.cpf_entry = ctk.CTkEntry(self, placeholder_text="CPF")
        self.cpf_entry.pack(pady=5, padx=20, fill="x")
        self.telefone_entry = ctk.CTkEntry(self, placeholder_text="Telefone")
        self.telefone_entry.pack(pady=5, padx=20, fill="x")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=5, padx=20, fill="x")

        btn_cadastrar = ctk.CTkButton(self, text="Cadastrar Paciente", command=self.cadastrar_paciente)
        btn_cadastrar.pack(pady=15, padx=20)

    def cadastrar_paciente(self):
        nome = self.nome_entry.get().strip()
        cpf = self.cpf_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        email = self.email_entry.get().strip()
        if not nome or not cpf:
            messagebox.showerror("Erro", "Nome e CPF são obrigatórios.")
            return
        try:
            paciente = paciente_controller.create_paciente(self.db, nome, cpf, telefone, email)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar paciente: {e}")
            return
        messagebox.showinfo("Sucesso", f"Paciente {paciente.nome} cadastrado com ID {paciente.id}")
        self.nome_entry.delete(0, "end")
        self.cpf_entry.delete(0, "end")
        self.telefone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

class PacienteListFrame(ctk.CTkFrame):
    def __init__(self, parent, app, db):
        super().__init__(parent)
        self.app = app
        self.db = db

        ctk.CTkLabel(self, text="Lista de Pacientes", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=lambda: app.show_frame(PacienteMenuFrame)).pack(anchor="nw", padx=10, pady=10)

        self.buscar_entry = ctk.CTkEntry(self, placeholder_text="Pesquisar paciente por nome")
        self.buscar_entry.pack(pady=5, padx=20, fill="x")

        btn_buscar = ctk.CTkButton(self, text="Buscar", command=self.buscar_pacientes)
        btn_buscar.pack(pady=5, padx=20)

        # Novo botão para atualizar manualmente
        btn_atualizar = ctk.CTkButton(self, text="Atualizar Lista", command=self.atualizar_lista)
        btn_atualizar.pack(pady=5, padx=20)

        self.lista_text = ctk.CTkTextbox(self, width=650, height=350)
        self.lista_text.pack(pady=15, padx=20)
        self.lista_text.configure(state="disabled")

        # Atualiza lista sempre que abrir a tela
        self.bind("<Visibility>", lambda e: self.atualizar_lista())

        self.atualizar_lista()

    def atualizar_lista(self):
        pacientes = paciente_controller.get_all_pacientes(self.db)
        self.mostrar_pacientes(pacientes)

    def buscar_pacientes(self):
        nome = self.buscar_entry.get().strip()
        pacientes = paciente_controller.buscar_pacientes_por_nome(self.db, nome)
        self.mostrar_pacientes(pacientes)

    def mostrar_pacientes(self, pacientes):
        self.lista_text.configure(state="normal")
        self.lista_text.delete("1.0", "end")  # corrigido aqui (era "0.0")
        if not pacientes:
            self.lista_text.insert("end", "Nenhum paciente encontrado.\n")
        else:
            for p in pacientes:
                linha = f"ID: {p.id} | Nome: {p.nome} | CPF: {p.cpf} | Telefone: {p.telefone} | Email: {p.email}\n"
                self.lista_text.insert("end", linha)
        self.lista_text.configure(state="disabled")

class PacienteUpdateFrame(ctk.CTkFrame):
    def __init__(self, parent, app, db):
        super().__init__(parent)
        self.app = app
        self.db = db

        # Título
        ctk.CTkLabel(self, text="Atualizar Paciente", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=15)

        # Botão voltar
        ctk.CTkButton(self, text="Voltar", command=lambda: app.show_frame(PacienteMenuFrame)).pack(anchor="nw", padx=15, pady=10)

        # Frame para busca
        busca_frame = ctk.CTkFrame(self)
        busca_frame.pack(pady=10, padx=15, fill="x")

        ctk.CTkLabel(busca_frame, text="Buscar Paciente por Nome:").pack(anchor="w", pady=(0,5))
        self.nome_busca_entry = ctk.CTkEntry(busca_frame, placeholder_text="Digite o nome")
        self.nome_busca_entry.pack(fill="x")

        btn_buscar = ctk.CTkButton(busca_frame, text="Buscar", command=self.buscar_pacientes)
        btn_buscar.pack(pady=10)

        # Textbox para mostrar resultados da busca
        self.resultado_text = ctk.CTkTextbox(self, width=650, height=150)
        self.resultado_text.pack(pady=10, padx=15)
        self.resultado_text.configure(state="disabled")

        # Frame para edição dos dados
        editar_frame = ctk.CTkFrame(self)
        editar_frame.pack(pady=10, padx=15, fill="x")

        ctk.CTkLabel(editar_frame, text="Digite o ID do paciente para carregar os dados:").pack(anchor="w")
        self.id_entry = ctk.CTkEntry(editar_frame, placeholder_text="ID do paciente")
        self.id_entry.pack(fill="x", pady=(0,10))

        btn_carregar = ctk.CTkButton(editar_frame, text="Carregar Dados", command=self.carregar_dados)
        btn_carregar.pack(pady=(0,15))

        # Campos para edição
        self.nome_entry = ctk.CTkEntry(editar_frame, placeholder_text="Nome")
        self.nome_entry.pack(fill="x", pady=5)
        self.cpf_entry = ctk.CTkEntry(editar_frame, placeholder_text="CPF")
        self.cpf_entry.pack(fill="x", pady=5)
        self.telefone_entry = ctk.CTkEntry(editar_frame, placeholder_text="Telefone")
        self.telefone_entry.pack(fill="x", pady=5)
        self.email_entry = ctk.CTkEntry(editar_frame, placeholder_text="Email")
        self.email_entry.pack(fill="x", pady=5)

        btn_atualizar = ctk.CTkButton(editar_frame, text="Atualizar Paciente", command=self.atualizar_paciente)
        btn_atualizar.pack(pady=15)

    def buscar_pacientes(self):
        nome = self.nome_busca_entry.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Digite um nome para buscar.")
            return
        pacientes = paciente_controller.buscar_pacientes_por_nome(self.db, nome)
        self.resultado_text.configure(state="normal")
        self.resultado_text.delete("0.0", "end")
        if not pacientes:
            self.resultado_text.insert("end", "Nenhum paciente encontrado.\n")
        else:
            for p in pacientes:
                linha = f"ID: {p.id} | Nome: {p.nome} | CPF: {p.cpf} | Telefone: {p.telefone or ''} | Email: {p.email or ''}\n"
                self.resultado_text.insert("end", linha)
        self.resultado_text.configure(state="disabled")

    def carregar_dados(self):
        try:
            id_paciente = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return
        paciente = paciente_controller.get_paciente_by_id(self.db, id_paciente)
        if not paciente:
            messagebox.showerror("Erro", "Paciente não encontrado.")
            return

        self.nome_entry.delete(0, "end")
        self.nome_entry.insert(0, paciente.nome)
        self.cpf_entry.delete(0, "end")
        self.cpf_entry.insert(0, paciente.cpf)
        self.telefone_entry.delete(0, "end")
        self.telefone_entry.insert(0, paciente.telefone or "")
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, paciente.email or "")

    def atualizar_paciente(self):
        try:
            id_paciente = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return

        nome = self.nome_entry.get().strip()
        cpf = self.cpf_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not nome or not cpf:
            messagebox.showerror("Erro", "Nome e CPF são obrigatórios.")
            return

        paciente = paciente_controller.update_paciente(
            self.db,
            id_paciente,
            nome=nome,
            cpf=cpf,
            telefone=telefone if telefone else None,
            email=email if email else None
        )
        if paciente:
            messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")
            # Opcional: limpar campos ou atualizar lista
            self.limpar_campos()
            self.resultado_text.configure(state="normal")
            self.resultado_text.delete("0.0", "end")
        else:
            messagebox.showerror("Erro", "Falha ao atualizar paciente.")

    def limpar_campos(self):
        self.id_entry.delete(0, "end")
        self.nome_entry.delete(0, "end")
        self.cpf_entry.delete(0, "end")
        self.telefone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

class PacienteDeleteFrame(ctk.CTkFrame):
    def __init__(self, parent, app, db):
        super().__init__(parent)
        self.app = app
        self.db = db

        ctk.CTkLabel(self, text="Deletar Paciente", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=lambda: app.show_frame(PacienteMenuFrame)).pack(anchor="nw", padx=10, pady=10)

        self.nome_busca_entry = ctk.CTkEntry(self, placeholder_text="Digite o nome para buscar")
        self.nome_busca_entry.pack(pady=5, padx=20, fill="x")

        btn_buscar = ctk.CTkButton(self, text="Buscar", command=self.buscar_pacientes)
        btn_buscar.pack(pady=10)

        self.resultado_text = ctk.CTkTextbox(self, width=650, height=150)
        self.resultado_text.pack(pady=10, padx=20)
        self.resultado_text.configure(state="disabled")

        self.id_entry = ctk.CTkEntry(self, placeholder_text="Digite o ID do paciente para deletar")
        self.id_entry.pack(pady=5, padx=20, fill="x")

        btn_mostrar_consultas = ctk.CTkButton(self, text="Mostrar Consultas Relacionadas", command=self.mostrar_consultas_relacionadas)
        btn_mostrar_consultas.pack(pady=5)

        btn_deletar = ctk.CTkButton(self, text="Deletar", command=self.deletar_paciente)
        btn_deletar.pack(pady=15, padx=20)

        self.consultas_text = ctk.CTkTextbox(self, width=650, height=100)
        self.consultas_text.pack(pady=10, padx=20)
        self.consultas_text.configure(state="disabled")

    def buscar_pacientes(self):
        nome = self.nome_busca_entry.get().strip()
        pacientes = paciente_controller.buscar_pacientes_por_nome(self.db, nome)
        self.resultado_text.configure(state="normal")
        self.resultado_text.delete("0.0", "end")
        if not pacientes:
            self.resultado_text.insert("end", "Nenhum paciente encontrado.\n")
        else:
            for p in pacientes:
                linha = f"ID: {p.id} | Nome: {p.nome} | CPF: {p.cpf} | Telefone: {p.telefone} | Email: {p.email}\n"
                self.resultado_text.insert("end", linha)
        self.resultado_text.configure(state="disabled")

    def mostrar_consultas_relacionadas(self):
        try:
            id_paciente = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return
        consultas = consulta_controller.get_consultas_by_paciente_id(self.db, id_paciente)
        self.consultas_text.configure(state="normal")
        self.consultas_text.delete("0.0", "end")
        if not consultas:
            self.consultas_text.insert("end", "Nenhuma consulta relacionada a este paciente.\n")
        else:
            for c in consultas:
                linha = (
                    f"ID: {c.id} | Médico ID: {c.medico_id} | Clínica ID: {c.clinica_id} | "
                    f"Data: {c.data_consulta} | Status: {c.status}\n"
                )
                self.consultas_text.insert("end", linha)
        self.consultas_text.configure(state="disabled")

    def deletar_paciente(self):
        try:
            id_paciente = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return
        consultas = consulta_controller.get_consultas_by_paciente_id(self.db, id_paciente)
        if consultas:
            msg = "Existem consultas relacionadas a este paciente. Deseja realmente deletar?\nIsso pode afetar dados relacionados."
            if not messagebox.askyesno("Confirmação", msg):
                return
        sucesso = paciente_controller.delete_paciente(self.db, id_paciente)
        if sucesso:
            messagebox.showinfo("Sucesso", "Paciente deletado com sucesso!")
            self.resultado_text.configure(state="normal")
            self.resultado_text.delete("0.0", "end")
            self.id_entry.delete(0, "end")
            self.nome_busca_entry.delete(0, "end")
            self.consultas_text.configure(state="normal")
            self.consultas_text.delete("0.0", "end")
            self.consultas_text.configure(state="disabled")
            self.resultado_text.configure(state="disabled")
        else:
            messagebox.showerror("Erro", "Falha ao deletar paciente.")


# ---------- Médico ----------

class MedicoFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        ctk.CTkLabel(self, text="Médicos Disponíveis", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        # Caixa de texto para mostrar médicos
        self.textbox = ctk.CTkTextbox(self, width=700, height=400)
        self.textbox.pack(pady=10, padx=20)
        self.textbox.configure(state="disabled")  # Inicialmente só leitura

        # Botão voltar
        btn_voltar = ctk.CTkButton(self, text="Voltar", command=lambda: app.show_frame(MenuFrame))
        btn_voltar.pack(pady=10)

        self.atualizar_lista_medicos()

    def atualizar_lista_medicos(self):
        medicos = medico_controller.listar_medicos_com_especialidades(db)
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")

        if not medicos:
            self.textbox.insert("end", "Nenhum médico encontrado.\n")
        else:
            for medico in medicos:
                especialidade_nome = medico.especialidade.nome if medico.especialidade else "Sem especialidade"
                linha = (
                    f"Nome: {medico.nome}\n"
                    f"CRM: {medico.crm}\n"
                    f"Especialidade: {especialidade_nome}\n"
                    "------------------------------\n"
                )
                self.textbox.insert("end", linha)

        self.textbox.configure(state="disabled")

# ---------- Consulta ----------

class ConsultaMenuFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        ctk.CTkLabel(self, text="Menu Consultas", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)
        ctk.CTkLabel(self, text="Sistema de Gestão Médica").pack(pady=10)

        btn_listar = ctk.CTkButton(self, text="Consultas Futuras", command=lambda: app.show_frame(ConsultaListFrame))
        btn_listar.pack(pady=10, ipadx=30, ipady=10)

        btn_voltar = ctk.CTkButton(self, text="Voltar", command=lambda: app.show_frame(MenuFrame))
        btn_voltar.pack(pady=30, ipadx=30, ipady=10)


class ConsultaListFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        ctk.CTkLabel(self, text="Consultas Futuras", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=lambda: app.show_frame(ConsultaMenuFrame)).pack(anchor="nw", padx=10, pady=10)

        self.nome_paciente_entry = ctk.CTkEntry(self, placeholder_text="Pesquisar pelo nome do paciente")
        self.nome_paciente_entry.pack(pady=5, padx=20, fill="x")

        self.data_min_entry = ctk.CTkEntry(self, placeholder_text="Filtrar por data mínima (YYYY-MM-DD)")
        self.data_min_entry.pack(pady=5, padx=20, fill="x")

        btn_pesquisar = ctk.CTkButton(self, text="Pesquisar", command=self.atualizar_consultas)
        btn_pesquisar.pack(pady=5)

        self.consultas_text = ctk.CTkTextbox(self, width=650, height=400)
        self.consultas_text.pack(pady=10, padx=20)
        self.consultas_text.configure(state="disabled")

        self.atualizar_consultas()

    def atualizar_consultas(self):
        nome = self.nome_paciente_entry.get().strip().lower()
        data_min = self.data_min_entry.get().strip()

        consultas = consulta_controller.get_consultas_futuras(db)

        self.consultas_text.configure(state="normal")
        self.consultas_text.delete("0.0", "end")

        consultas_filtradas = []

        for c in consultas:
            paciente_nome = c.paciente.lower()
            data_consulta_str = str(c.data_consulta)

            if nome and nome not in paciente_nome:
                continue

            if data_min:
                try:
                    from datetime import datetime
                    data_min_dt = datetime.strptime(data_min, "%Y-%m-%d")
                    data_consulta_dt = datetime.strptime(data_consulta_str.split()[0], "%Y-%m-%d")
                    if data_consulta_dt < data_min_dt:
                        continue
                except Exception:
                    messagebox.showerror("Erro", "Formato de data inválido. Use YYYY-MM-DD.")
                    self.consultas_text.configure(state="disabled")
                    return

            consultas_filtradas.append(c)

        if not consultas_filtradas:
            self.consultas_text.insert("end", "Nenhuma consulta futura encontrada.\n")
        else:
            for c in consultas_filtradas:
                data_str = str(c.data_consulta)
                linha = (
                    f"ID Consulta: {c.consulta_id} | Paciente: {c.paciente} | Médico: {c.medico} | "
                    f"Data: {data_str}\n"
                )
                self.consultas_text.insert("end", linha)

        self.consultas_text.configure(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()
