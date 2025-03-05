import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import win32com.client

def resolve_shortcut(path):
    """ Resolve um atalho .lnk para seu caminho real. """
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(path)
    return shortcut.TargetPath

class DualConsoleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual Console Launcher")
        self.root.geometry("800x600")
        
        self.loginserver_path = None
        self.gameserver_path = None
        self.loginserver_process = None
        self.gameserver_process = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Título e seleção do LoginServer
        self.label_login = tk.Label(self.root, text="LoginServer", font=("Arial", 12, "bold"))
        self.label_login.pack()
        self.btn_select_login = tk.Button(self.root, text="Selecionar .bat", command=self.select_login_bat)
        self.btn_select_login.pack()
        
        # Console do LoginServer
        self.text_login = tk.Text(self.root, height=10, width=100, state=tk.DISABLED)
        self.text_login.pack()
        
        # Título e seleção do GameServer
        self.label_game = tk.Label(self.root, text="GameServer", font=("Arial", 12, "bold"))
        self.label_game.pack()
        self.btn_select_game = tk.Button(self.root, text="Selecionar .bat", command=self.select_game_bat)
        self.btn_select_game.pack()
        
        # Console do GameServer
        self.text_game = tk.Text(self.root, height=10, width=100, state=tk.DISABLED)
        self.text_game.pack()
        
        # Botão StartEngine
        self.btn_start = tk.Button(self.root, text="StartEngine", command=self.start_engine, font=("Arial", 12, "bold"))
        self.btn_start.pack(pady=10)
    
    def select_login_bat(self):
        path = filedialog.askopenfilename(filetypes=[("Arquivos BAT", "*.bat"), ("Atalhos", "*.lnk")])
        if path:
            self.loginserver_path = resolve_shortcut(path) if path.endswith(".lnk") else path
            messagebox.showinfo("Selecionado", f"LoginServer: {self.loginserver_path}")
    
    def select_game_bat(self):
        path = filedialog.askopenfilename(filetypes=[("Arquivos BAT", "*.bat"), ("Atalhos", "*.lnk")])
        if path:
            self.gameserver_path = resolve_shortcut(path) if path.endswith(".lnk") else path
            messagebox.showinfo("Selecionado", f"GameServer: {self.gameserver_path}")
    
    def start_engine(self):
        if not self.loginserver_path and not self.gameserver_path:
            messagebox.showwarning("Erro", "Nenhum arquivo .bat foi carregado!")
            return
        
        if not self.loginserver_path or not self.gameserver_path:
            if not messagebox.askokcancel("Aviso", "Nem todos os arquivos foram carregados. Continuar mesmo assim?"):
                return
        
        # Inicia os servidores
        if self.loginserver_path:
            self.loginserver_process = subprocess.Popen(self.loginserver_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.monitor_process(self.loginserver_process, self.text_login)
        
        if self.gameserver_path:
            self.gameserver_process = subprocess.Popen(self.gameserver_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.monitor_process(self.gameserver_process, self.text_game)
    
    def monitor_process(self, process, text_widget):
        """ Lê a saída do processo e exibe no widget de texto. """
        def read_output():
            for line in iter(process.stdout.readline, ''):
                text_widget.config(state=tk.NORMAL)
                text_widget.insert(tk.END, line)
                text_widget.config(state=tk.DISABLED)
                text_widget.see(tk.END)
        
        self.root.after(100, read_output)

if __name__ == "__main__":
    if sys.platform != "win32":
        messagebox.showerror("Erro", "Esta aplicação só funciona no Windows!")
        sys.exit(1)
    
    root = tk.Tk()
    app = DualConsoleApp(root)
    root.mainloop()
