import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import secrets
import string
from password_manager import PasswordManager
from file_analyzer import FileAnalyzer
from auth_manager import AuthManager

class PasswordFileManagerApp:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.password_manager = PasswordManager()
        self.file_analyzer = FileAnalyzer()
        
        self.root = tk.Tk()
        self.root.title("CripISafe")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")


        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 12, 'bold'))
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white', font=('Arial', 12, 'bold'))
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('Treeview', font=('Arial', 12), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))

        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill='both', expand=True, padx=20, pady=20)


        self.create_login_widgets()


    def create_login_widgets(self):
        self.title_label = ttk.Label(self.login_frame, text="Bem vindo!", font=('Arial', 18, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_label = ttk.Label(self.login_frame, text="Usuario:")
        self.username_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.password_label = ttk.Label(self.login_frame, text="Senha:")
        self.password_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.password_entry = ttk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.show_password_var = tk.IntVar()
        self.show_password_check = ttk.Checkbutton(self.login_frame, text="Mostrar senha", variable=self.show_password_var, command=self.toggle_password)
        self.show_password_check.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.register_button = ttk.Button(self.login_frame, text="Registre-se", command=self.register, style='Accent.TButton')
        self.register_button.grid(row=4, column=0, padx=5, pady=20, ipadx=10, ipady=5, sticky='e')

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login, style='Accent.TButton')
        self.login_button.grid(row=4, column=1, padx=5, pady=20, ipadx=10, ipady=5, sticky='w')

        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(1, weight=1)
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(1, weight=1)
        self.login_frame.grid_rowconfigure(2, weight=1)
        self.login_frame.grid_rowconfigure(3, weight=1)
        self.login_frame.grid_rowconfigure(4, weight=1)

        

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Input Error", "Por favor preencha todos os campos")
            return
        if self.auth_manager.register(username, password):
            messagebox.showinfo("Success", "Registro realizado com sucesso")
        else:
            messagebox.showwarning("Error", "O nome de usuário já existe")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Input Error", "Por favor preencha todos os campos")
            return
        if self.auth_manager.login(username, password):
            self.login_frame.pack_forget()
            self.create_main_widgets()
        else:
            messagebox.showwarning("Error", "nome de usuário ou senha inválidos")

    def create_main_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.create_password_frame()
        self.create_file_frame()
        self.create_view_frame()

    def create_password_frame(self):
        self.password_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.password_frame, text="Ger. Senhas")

        # Adiciona um estilo de borda ao frame
        self.password_frame.configure(borderwidth=2, relief='groove')

        # Título da seção
        self.section_title = ttk.Label(self.password_frame, text="Gerenciador de Senhas", font=('Arial', 18, 'bold'))
        self.section_title.grid(row=0, column=0, columnspan=2, pady=10)

        # Labels e Entradas para Email e Senha
        self.email_label = ttk.Label(self.password_frame, text="Email:", font=('Arial', 12))
        self.email_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.email_entry = ttk.Entry(self.password_frame, font=('Arial', 12))
        self.email_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.password_value_label = ttk.Label(self.password_frame, text="Senha:", font=('Arial', 12))
        self.password_value_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.password_value_entry = ttk.Entry(self.password_frame, show='*', font=('Arial', 12))
        self.password_value_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.password_value_entry.bind('<KeyRelease>', self.check_password_strength)

        # Checkbox para mostrar senha
        self.show_password_var_pm = tk.IntVar()
        self.show_password_check_pm = ttk.Checkbutton(self.password_frame, text="Mostrar senha", variable=self.show_password_var_pm, command=self.toggle_password_pm)
        self.show_password_check_pm.grid(row=3, column=1, sticky='w', padx=10, pady=5)

        # Barra de progresso para força da senha
        self.style.configure('red.Horizontal.TProgressbar', troughcolor='white', background='red')
        self.style.configure('yellow.Horizontal.TProgressbar', troughcolor='white', background='yellow')
        self.style.configure('green.Horizontal.TProgressbar', troughcolor='white', background='green')

        self.password_strength_label = ttk.Label(self.password_frame, text="Força da Senha:", font=('Arial', 12))
        self.password_strength_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.password_strength = ttk.Progressbar(self.password_frame, length=200, mode='determinate', style='red.Horizontal.TProgressbar')
        self.password_strength.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        # Botões para gerar e salvar senha
        self.generate_password_button = ttk.Button(self.password_frame, text="Gerar Senha Segura", command=self.generate_password, style='Accent.TButton')
        self.generate_password_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=5, sticky='ew')
        self.generate_password_button.config(width=20)  # Ajusta a largura do botão

        self.save_password_button = ttk.Button(self.password_frame, text="Salvar Senha", command=self.save_password, style='Accent.TButton')
        self.save_password_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=5, sticky='ew')
        self.save_password_button.config(width=20)  # Ajusta a largura do botão

        # Adiciona o layout da grid
        self.password_frame.grid_columnconfigure(0, weight=1)
        self.password_frame.grid_columnconfigure(1, weight=1)
        self.password_frame.grid_rowconfigure(0, weight=0)
        self.password_frame.grid_rowconfigure(1, weight=0)
        self.password_frame.grid_rowconfigure(2, weight=0)
        self.password_frame.grid_rowconfigure(3, weight=0)
        self.password_frame.grid_rowconfigure(4, weight=0)
        self.password_frame.grid_rowconfigure(5, weight=0)
        self.password_frame.grid_rowconfigure(6, weight=0)



    def toggle_password_pm(self):
        if self.show_password_var_pm.get():
            self.password_value_entry.config(show='')
        else:
            self.password_value_entry.config(show='*')

    def check_password_strength(self, event):
        password = self.password_value_entry.get()
        strength = self.get_password_strength(password)
        
        if strength < 4:
            self.password_strength.config(value=33, style='red.Horizontal.TProgressbar')
        elif strength < 6:
            self.password_strength.config(value=100, style='green.Horizontal.TProgressbar')
        else:
            self.password_strength.config(value=100, style='green.Horizontal.TProgressbar')

        # Atualiza a cor da barra de progresso
        self.password_strength_label.config(text=f"Força da Senha: {'Fraca' if strength < 4 else 'Forte' if strength < 6 else 'Forte'}")

    def get_password_strength(self, password):
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        strength = sum([length >= 8, has_upper, has_lower, has_digit, has_special])
        return strength

    def create_file_frame(self):
        self.file_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.file_frame, text="Ana. Arquivos")

        # Adiciona um estilo de borda ao frame
        self.file_frame.configure(borderwidth=2, relief='groove')

        # Frame para os botões
        button_frame = ttk.Frame(self.file_frame)
        button_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        self.select_file_button = ttk.Button(button_frame, text="Selecionar Arquivo", command=self.select_file, style='Accent.TButton')
        self.select_file_button.pack(side='left', padx=5)

        self.analyze_file_button = ttk.Button(button_frame, text="Analisar Arquivo", command=self.analyze_file, style='Accent.TButton')
        self.analyze_file_button.pack(side='left', padx=5)

        # Área de texto para exibir o conteúdo do arquivo
        self.file_content_text = tk.Text(self.file_frame, wrap='word', height=30, borderwidth=1, relief='solid', font=('Arial', 12))
        self.file_content_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Adiciona uma barra de rolagem vertical
        self.v_scrollbar = ttk.Scrollbar(self.file_frame, orient='vertical', command=self.file_content_text.yview)
        self.v_scrollbar.grid(row=1, column=2, sticky='ns')
        self.file_content_text.configure(yscrollcommand=self.v_scrollbar.set)

        # Adiciona uma barra de rolagem horizontal
        self.h_scrollbar = ttk.Scrollbar(self.file_frame, orient='horizontal', command=self.file_content_text.xview)
        self.h_scrollbar.grid(row=2, column=0, sticky='ew')
        self.file_content_text.configure(xscrollcommand=self.h_scrollbar.set)

        # Label de status para feedback
        self.status_label = ttk.Label(self.file_frame, text="Nenhum arquivo selecionado", font=('Arial', 12, 'italic'))
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')

        # Ajusta o layout
        self.file_frame.grid_columnconfigure(0, weight=1)
        self.file_frame.grid_columnconfigure(1, weight=1)
        self.file_frame.grid_rowconfigure(1, weight=1)


    def create_view_frame(self):
        self.view_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_frame, text="Visu. Senhas")

        # Estilo para Treeview
        self.style.configure('Treeview', background='#f9f9f9', fieldbackground='#f9f9f9', foreground='#333', font=('Arial', 12))
        self.style.configure('Treeview.Heading', font=('Arial', 12, 'bold'), background='#e0e0e0', foreground='#333')
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white', font=('Arial', 12, 'bold'))

        # Treeview para exibir senhas
        self.password_tree = ttk.Treeview(self.view_frame, columns=("Email", "Password"), show='headings', style='Treeview')
        self.password_tree.heading("Email", text="Email")
        self.password_tree.heading("Password", text="Senha")
        self.password_tree.column("Email", width=300, anchor='w')
        self.password_tree.column("Password", width=300, anchor='w')
        self.password_tree.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Adiciona uma barra de rolagem vertical
        self.v_scrollbar = ttk.Scrollbar(self.view_frame, orient='vertical', command=self.password_tree.yview)
        self.v_scrollbar.grid(row=0, column=2, sticky='ns')
        self.password_tree.configure(yscrollcommand=self.v_scrollbar.set)

        # Adiciona uma barra de rolagem horizontal
        self.h_scrollbar = ttk.Scrollbar(self.view_frame, orient='horizontal', command=self.password_tree.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')
        self.password_tree.configure(xscrollcommand=self.h_scrollbar.set)

        # Botões
        button_frame = ttk.Frame(self.view_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky='ew')

        self.refresh_password_list_button = ttk.Button(button_frame, text="Recarregar lista de senhas", command=self.refresh_password_list, style='Accent.TButton')
        self.refresh_password_list_button.pack(side='left', padx=5)

        self.delete_password_button = ttk.Button(button_frame, text="Excluir senha", command=self.remove_password, style='Accent.TButton')
        self.delete_password_button.pack(side='left', padx=5)

        self.edit_password_button = ttk.Button(button_frame, text="Editar Senha", command=self.edit_password, style='Accent.TButton')
        self.edit_password_button.pack(side='left', padx=5)

        self.view_frame.grid_rowconfigure(0, weight=1)
        self.view_frame.grid_columnconfigure(0, weight=1)
        self.view_frame.grid_columnconfigure(1, weight=0)
        self.view_frame.grid_rowconfigure(1, weight=0)
        self.view_frame.grid_rowconfigure(2, weight=0)


    def save_password(self):
        email = self.email_entry.get()
        password = self.password_value_entry.get()

        if not email or not password:
            messagebox.showwarning("Input Error", "Por favor preencha todos os campos")
            return

        if not self.is_valid_email(email):
            messagebox.showwarning("Input Error", "Formato invalido. Adicione um dominio (e.g., @gmail.com, @outlook.com, etc.)")
            return

        if self.password_manager.email_exists(email):
            messagebox.showwarning("Input Error", "Esse email ja existe. Adicione um diferente.")
            return

        self.password_manager.add_password(email, password)
        messagebox.showinfo("Success", f" Senha por {email} salvo com sucesso")
        self.refresh_password_list()

    def remove_password(self):
        selected_item = self.password_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Selecione o item para remover")
            return
        email = self.password_tree.item(selected_item)["values"][0]
        self.password_manager.remove_password(email)
        messagebox.showinfo("Success", "Senha removida com sucesso")
        self.refresh_password_list()

    def edit_password(self):
        selected_item = self.password_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Selecione o item para editar")
            return

        current_email = self.password_tree.item(selected_item)["values"][0]
        current_password = self.password_tree.item(selected_item)["values"][1]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar senha")
        edit_window.geometry("300x200")

        new_email_label = ttk.Label(edit_window, text="Novo Email:")
        new_email_label.pack(padx=10, pady=5, anchor='w')
        new_email_entry = ttk.Entry(edit_window)
        new_email_entry.insert(0, current_email)
        new_email_entry.pack(padx=10, pady=5, fill='x')

        new_password_label = ttk.Label(edit_window, text="Nova senha:")
        new_password_label.pack(padx=10, pady=5, anchor='w')
        new_password_entry = ttk.Entry(edit_window, show='*')
        new_password_entry.insert(0, current_password)
        new_password_entry.pack(padx=10, pady=5, fill='x')

        show_password_var = tk.IntVar()
        show_password_check = ttk.Checkbutton(edit_window, text="Mostrar senha", variable=show_password_var, command=lambda: self.toggle_password_visibility(new_password_entry, show_password_var))
        show_password_check.pack(padx=10, pady=5)

        save_button = ttk.Button(edit_window, text="Salvar", command=lambda: self.save_edited_password(selected_item, new_email_entry.get(), new_password_entry.get(), edit_window))
        save_button.pack(padx=10, pady=10)

    def toggle_password_visibility(self, entry, var):
        if var.get():
            entry.config(show='')
        else:
            entry.config(show='*')

    def save_edited_password(self, selected_item, new_email, new_password, window):
        old_email = self.password_tree.item(selected_item)["values"][0]

        if not new_email or not new_password:
            messagebox.showwarning("Input Error", "Por favor preencha todos os campos")
            return

        if not self.is_valid_email(new_email):
            messagebox.showwarning("Input Error", "Formato invalido. Adicione um dominio (e.g., @gmail.com, @outlook.com, etc.)")
            return

        if self.password_manager.email_exists(new_email) and new_email != old_email:
            messagebox.showwarning("Input Error", "Esse email ja existe. Adicione um diferente.")
            return

        self.password_manager.remove_password(old_email)
        self.password_manager.add_password(new_email, new_password)

        messagebox.showinfo("Success", "Senha modificada com sucesso")
        self.refresh_password_list()
        window.destroy()

    def generate_password(self):
        password = self.create_secure_password()
        self.password_value_entry.delete(0, tk.END)
        self.password_value_entry.insert(0, password)
        self.check_password_strength(None)  # Update the password strength bar

    def create_secure_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(length))

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Selecione o arquivo")
        if file_path:
            self.selected_file_path = file_path
            self.status_label.config(text=f"Arquivo selecionado: {file_path}")


    def analyze_file(self):
        if not hasattr(self, 'selected_file_path'):
            messagebox.showwarning("No File", "Nenhum arquivo selecionado. Selecione um arquivo primeiro.")
            return
        content = self.file_analyzer.analyze_file(self.selected_file_path)
        self.file_content_text.delete(1.0, tk.END)
        self.file_content_text.insert(tk.END, content)

    def refresh_password_list(self):
        for item in self.password_tree.get_children():
            self.password_tree.delete(item)
        passwords = self.password_manager.get_all_passwords()
        for email, password in passwords:
            self.password_tree.insert("", "end", values=(email, password))
            

    def is_valid_email(self, email):
        valid_domains = ["@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com"]
        return any(email.endswith(domain) for domain in valid_domains)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PasswordFileManagerApp()
    app.run()
