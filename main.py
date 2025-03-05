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
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.loginserver_path = None
        self.gameserver_path = None
        self.loginserver_process = None
        self.gameserver_process = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Título e seleção do LoginServer
        self.label_login = tk.Label(self.root, text="LoginServer", font=("Arial", 12, "bold"))
        self.label_login.grid(row=0, column=0, sticky="ew")
        self.btn_select_login = tk.Button(self.root, text="Selecionar .bat", command=self.select_login_bat)
        self.btn_select_login.grid(row=1, column=0, sticky="ew")
        
        # Título e seleção do GameServer
        self.label_game = tk.Label(self.root, text="GameServer", font=("Arial", 12, "bold"))
        self.label_game.grid(row=3, column=0, sticky="ew")
        self.btn_select_game = tk.Button(self.root, text="Selecionar .bat", command=self.select_game_bat)
        self.btn_select_game.grid(row=4, column=0, sticky="ew")
        
        # PanedWindow for resizable consoles
        self.paned_window = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned_window.grid(row=2, column=0, rowspan=3, sticky="nsew")
        
        # Console do LoginServer
        self.text_login = tk.Text(self.paned_window, height=10, width=100, state=tk.DISABLED)
        self.paned_window.add(self.text_login)
        
        # Console do GameServer
        self.text_game = tk.Text(self.paned_window, height=10, width=100, state=tk.DISABLED)
        self.paned_window.add(self.text_game)
        
        # Botão StartEngine
        self.btn_start = tk.Button(self.root, text="Start", command=self.start_engine, font=("Arial", 10, "bold"))
        self.btn_start.grid(row=6, column=0, pady=5, sticky="ew")
        
        # Botão StopEngine
        self.btn_stop = tk.Button(self.root, text="Stop", command=self.stop_engine, font=("Arial", 10, "bold"))
        self.btn_stop.grid(row=7, column=0, pady=5, sticky="ew")
        
        # Botão Save Config
        self.btn_save_config = tk.Button(self.root, text="Save Config", command=self.save_config, font=("Arial", 10, "bold"))
        self.btn_save_config.grid(row=8, column=0, pady=5, sticky="ew")
        
        # Botão Load Config
        self.btn_load_config = tk.Button(self.root, text="Load Config", command=self.load_config, font=("Arial", 10, "bold"))
        self.btn_load_config.grid(row=9, column=0, pady=5, sticky="ew")
        
        # Botão Reset Interface
        self.btn_reset = tk.Button(self.root, text="Reset", command=self.reset_interface, font=("Arial", 10, "bold"))
        self.btn_reset.grid(row=10, column=0, pady=5, sticky="ew")
    
    def reset_interface(self):
        self.loginserver_path = None
        self.gameserver_path = None
        self.text_login.config(state=tk.NORMAL)
        self.text_login.delete(1.0, tk.END)
        self.text_login.config(state=tk.DISABLED)
        self.text_game.config(state=tk.NORMAL)
        self.text_game.delete(1.0, tk.END)
        self.text_game.config(state=tk.DISABLED)
        messagebox.showinfo("Reset", "Interface resetada com sucesso!")
    
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
    
    def stop_engine(self):
        if self.loginserver_process:
            self.loginserver_process.terminate()
            self.loginserver_process = None
            self.text_login.config(state=tk.NORMAL)
            self.text_login.insert(tk.END, "LoginServer stopped.\n")
            self.text_login.config(state=tk.DISABLED)
        
        if self.gameserver_process:
            self.gameserver_process.terminate()
            self.gameserver_process = None
            self.text_game.config(state=tk.NORMAL)
            self.text_game.insert(tk.END, "GameServer stopped.\n")
            self.text_game.config(state=tk.DISABLED)
    
    def monitor_process(self, process, text_widget):
        """ Lê a saída do processo e exibe no widget de texto. """
        def read_output():
            for line in iter(process.stdout.readline, ''):
                text_widget.config(state=tk.NORMAL)
                text_widget.insert(tk.END, line)
                text_widget.config(state=tk.DISABLED)
                text_widget.see(tk.END)
        
        self.root.after(100, read_output)
    
    def save_config(self):
        config = {
            "loginserver_path": self.loginserver_path,
            "gameserver_path": self.gameserver_path
        }
        with open("config.txt", "w") as config_file:
            config_file.write(str(config))
        messagebox.showinfo("Configuração", "Configurações salvas com sucesso!")
    
    def load_config(self):
        try:
            with open("config.txt", "r") as config_file:
                config = eval(config_file.read())
                self.loginserver_path = config.get("loginserver_path")
                self.gameserver_path = config.get("gameserver_path")
                messagebox.showinfo("Configuração", "Configurações carregadas com sucesso!")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de configuração não encontrado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configurações: {e}")

if __name__ == "__main__":
    if sys.platform != "win32":
        messagebox.showerror("Erro", "Esta aplicação só funciona no Windows!")
        sys.exit(1)
    
    root = tk.Tk()
    app = DualConsoleApp(root)
    root.mainloop()
