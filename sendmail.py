import os
import smtplib
from email.message import EmailMessage
from tkinter.filedialog import askopenfilenames

import customtkinter
from customtkinter import CTkLabel, CTkButton

class Email:
    def __init__(self, conteudo):
        # Pré configuração do e-mail
        self.remetente = ""
        self.senha = "" # <--- Sua senha de app (não senha da conta)
        self.destinatario = "" # <--- E-mail Kindle
        self.assunto = "Arquivos EPUB"
        self.conteudo = conteudo

        # Cria o e-mail a ser enviado
        self.msg = EmailMessage()
        self.msg["From"] = self.remetente
        self.msg["To"] = self.destinatario
        self.msg["Subject"] = self.assunto
        self.msg.set_content(self.conteudo)

    def anexar_arquivos(self, arquivos):
        for arquivo in arquivos:
            with open(arquivo, "rb") as f:
                dados = f.read()
                nome = os.path.basename(arquivo)
                self.msg.add_attachment(dados, maintype="application", subtype="octet-stream", filename=nome)

    def enviar_email(self):
        # Caso seu email seja Gmail ou outro qualquer, coloque o respectivo servidor smtp no host abaixo.
        with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465) as smtp:
            smtp.login(self.remetente, self.senha)
            smtp.send_message(self.msg)
            print("E-mail enviado com sucesso!")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.geometry("500x300")
        self.title("Enviar EPUB por Email")

        self.arquivos_selecionados = []
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure(1, weight=2)

        CTkLabel(self, text="Selecione os EPUBs para envio").grid(column=1, row=0, padx=10, pady=10)
        CTkButton(self, text="SELECIONAR", command=self.selecionar_arquivos).grid(column=1, row=1, padx=10, pady=10)
        CTkLabel(self, text="Arquivos selecionados:", font=("Arial", 10, "bold")).grid(column=1, row=2, padx=25, pady=(10, 0))

        self.label_arquivos = CTkLabel(self, text="", justify="left", anchor="w")
        self.label_arquivos.grid(column=1, row=3, padx=25, pady=5, sticky="w")

        CTkButton(self, text="ENVIAR", command=self.enviar).grid(column=1, row=4, padx=10, pady=10)

    def selecionar_arquivos(self):
        self.arquivos_selecionados = askopenfilenames(filetypes=[("Arquivos EPUB", "*.epub")])
        if self.arquivos_selecionados:
            nomes = "\n".join([os.path.basename(f) for f in self.arquivos_selecionados])
            self.label_arquivos.configure(text=nomes)

    def enviar(self):
        if not self.arquivos_selecionados:
            self.label_arquivos.configure(text="Nenhum arquivo selecionado.")
            return
        email = Email("Segue em anexo os arquivos EPUB.")
        email.anexar_arquivos(self.arquivos_selecionados)
        email.enviar_email()

app = App()
app.mainloop()