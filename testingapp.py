import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import PhotoImage

class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Viewer")

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.select_button = ttk.Button(self.main_frame, text="Select Database", command=self.select_database)
        self.select_button.grid(row=0, column=0, pady=10)

        self.load_all_button = ttk.Button(self.main_frame, text="Load All Tables", command=self.load_all_tables)
        self.load_all_button.grid(row=1, column=0, pady=10)

        self.tree = ttk.Treeview(self.main_frame, columns=('ID', 'Name', 'Value'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Value', text='Value')
        self.tree_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        self.tree.grid(row=2, column=0)
        self.tree_scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))

        self.loaded_label = ttk.Label(self.main_frame, text="", foreground="green")
        self.loaded_label.grid(row=3, column=0, pady=10)
        self.load_image()

    def load_image(self):
        try:
            image_path = '359420804_1021436118870746_6792354226991959439_n_preview_rev_1.png'
            self.img = PhotoImage(file=image_path)

            self.image_label = ttk.Label(self.main_frame, image=self.img)
            self.image_label.grid(row=4, column=0, pady=10)

        except Exception as e:
            print(f"Error loading image: {e}")

    def select_database(self):
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db;*.sqlite;*.db3")])

        if file_path:
            self.file_path = file_path
            self.loaded_label.config(text="DATABASE LOADED")

    def load_all_tables(self):
        if hasattr(self, 'file_path') and self.file_path:
            conn = sqlite3.connect(self.file_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for item in self.tree.get_children():
                self.tree.delete(item)
            for table_info in tables:
                table_name = table_info[0]
                self.tree.insert('', 'end', values=[f'Table: {table_name}'])
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                for row in rows:
                    self.tree.insert('', 'end', values=row)
            conn.close()
        else:
            messagebox.showwarning("Warning", "Please select a database first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseViewer(root)
    root.mainloop()
