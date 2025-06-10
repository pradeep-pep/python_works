import os
import tkinter as tk
from tkinter import ttk, messagebox

LDAP_DIR = r'C:\Users\pepsara\Documents\PYTHON WORKS\LDAP'
LDAP_FILE = os.path.join(LDAP_DIR, 'LDAP.txt')
COB_SRC_DIR = r'C:\Users\pepsara\Documents\PYTHON WORKS\CobSource'
COB_MASKED_DIR = r'C:\Users\pepsara\Documents\PYTHON WORKS\CobMasked'
MAX_FILES = 50

def mask_ids_in_cobol(ldap_file, cobol_file, output_file):
    # Read all IDs into a set for fast lookup
    with open(ldap_file, 'r') as f:
        ids = set(line.strip() for line in f if line.strip())

    with open(cobol_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Stop processing if PROCEDURE DIVISION is found
            if 'PROCEDURE DIVISION' in line:
                outfile.write(line)
                break
            # Only process lines starting with '*'
            if line.lstrip().startswith('*'):
                # Replace all IDs with '@'
                for id_ in ids:
                    if id_ in line:
                        line = line.replace(id_, '@')
                outfile.write(line)
            else:
                outfile.write(line)
        # Write the rest of the file unchanged
        for line in infile:
            outfile.write(line)

class CobolMaskerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CobolGuard - COBOL Masking Utility")
        self.file_vars = {}  # filename: tk.BooleanVar
        self.displayed_files = []
        self.all_files = self.get_cbl_files()
        self.selected_files = set()
        self.search_terms = set()

        # Search box
        self.search_var = tk.StringVar()
        search_frame = tk.Frame(root)
        search_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(search_frame, text="Search:").pack(side='left')
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind('<Return>', self.on_search)

        # File list
        self.file_frame = tk.Frame(root)
        self.file_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.file_canvas = tk.Canvas(self.file_frame)
        self.scrollbar = ttk.Scrollbar(self.file_frame, orient="vertical", command=self.file_canvas.yview)
        self.scrollable_frame = tk.Frame(self.file_canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.file_canvas.configure(
                scrollregion=self.file_canvas.bbox("all")
            )
        )
        self.file_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.file_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.file_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # OK button
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill='x', padx=10, pady=5)
        self.ok_btn = tk.Button(btn_frame, text="OK", command=self.on_ok)
        self.ok_btn.pack(side='right')

        self.populate_file_list(self.all_files[:MAX_FILES])

    def get_cbl_files(self):
        files = []
        if os.path.exists(COB_SRC_DIR):
            for fname in os.listdir(COB_SRC_DIR):
                if fname.lower().endswith('.cbl'):
                    files.append(fname)
        return sorted(files)

    def populate_file_list(self, file_list):
        # Clear previous
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.file_vars.clear()
        self.displayed_files = []
        for fname in file_list:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.scrollable_frame, text=fname, variable=var)
            cb.pack(anchor='w')
            self.file_vars[fname] = var
            self.displayed_files.append(fname)

    def on_search(self, event=None):
        term = self.search_var.get().strip()
        if not term:
            # If search box is empty, show all files (up to MAX_FILES)
            self.populate_file_list(self.all_files[:MAX_FILES])
            return
        # Add new search term
        self.search_terms.add(term.lower())
        # Filter files for all search terms, no duplicates
        filtered = []
        for fname in self.all_files:
            for t in self.search_terms:
                if t in fname.lower() and fname not in filtered:
                    filtered.append(fname)
        self.populate_file_list(filtered[:MAX_FILES])
        self.search_var.set('')  # Clear search box

    def on_ok(self):
        selected = [fname for fname, var in self.file_vars.items() if var.get()]
        if not selected:
            messagebox.showerror("Error", "No program selected. Please select at least one program.")
            return
        for fname in selected:
            src_path = os.path.join(COB_SRC_DIR, fname)
            out_path = os.path.join(COB_MASKED_DIR, fname)
            try:
                mask_ids_in_cobol(LDAP_FILE, src_path, out_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {fname}: {e}")
                return
        messagebox.showinfo("Done", f"Masked {len(selected)} program(s) to {COB_MASKED_DIR}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CobolMaskerApp(root)
    root.mainloop()