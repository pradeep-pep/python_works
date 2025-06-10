#This program does masks Cobol IDs in source files based on a given LDAP file.
import os
import sys
import time 
import datetime
import platform
import tkinter as tk
from tkinter import ttk, messagebox

#File Handling
LDAP_DIR = r'C:\Users\pepsara\Documents\PYTHON WORKS\LDAP'
LDAP_FILE = os.path.join(LDAP_DIR, 'Userid_Mapping.txt')
COB_SRC_DIR = r'C:\Users\pepsara\Documents\PYTHON WORKS\CobSource'
COB_MASKED_DIR = r'C:\Users\pepsara\Documents\PYTHON WORKS\CobMasked'
MAX_FILES = 10

def get_cbl_files():
    files = []  
    if os.path.exists(COB_SRC_DIR):
        for fname in os.listdir(COB_SRC_DIR):
            if fname.lower().endswith('.txt') or fname.lower().endswith('.cbl'):
                files.append(fname)
    print("COBOL source files found:", files)
    return sorted(files)
    

#Task Handling

#Main Menu
def CobIDMask():
    ToDoWelcome() 
    CobolMaskerApp()

def ToDoWelcome(): #1
    print()
    print("***CobolGuard - COBOL Sensitive Info Masking Utility !***")
    print()
    print("This utility will help masking sensitive information [NBK ID's]" \
    " in COBOL source files, using a provided UserID mapping file.")
    print()

def CobolMaskerApp(): #2
    files = get_cbl_files()
    on_ok(files)

def on_ok(files):
    root = tk.Tk()
    root.withdraw()
    # Prompt for user name
    username = input("Enter your name: ").strip()
    if not username:
        print("No name entered. Exiting.")
        return
    # Create timestamped folder
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    user_folder = os.path.join(COB_MASKED_DIR, f"{username}_{timestamp}")
    os.makedirs(user_folder, exist_ok=True)
    print(f"Output folder created: {user_folder}")

    for fname in files:
        src_path = os.path.join(COB_SRC_DIR, fname)
        print(f"Processing {fname} from {src_path}")
        out_path = os.path.join(user_folder, fname)
        print(f"Processing {fname} from {src_path} to {out_path}")
        try:
            mask_ids_in_cobol(LDAP_FILE, src_path, out_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing {fname}: {e}")
            return
    messagebox.showinfo("Done", f"Masked {len(files)} program(s) to {COB_MASKED_DIR}")

def mask_ids_in_cobol(ldap_file, cobol_file, output_file):
    # Read all IDs into a set for fast lookup
    print(f"Reading IDs from {ldap_file}")
    if not os.path.exists(ldap_file):
        raise FileNotFoundError(f"LDAP file not found: {ldap_file}")
    print(f"Reading COBOL source file {cobol_file}")
    if not os.path.exists(cobol_file):
        raise FileNotFoundError(f"COBOL source file not found: {cobol_file}")   
    print(f"Writing masked output to {output_file}")
    if not os.path.exists(COB_MASKED_DIR):
        os.makedirs(COB_MASKED_DIR)
        print(f"Creating output directory {COB_MASKED_DIR} if it does not exist")

    with open(ldap_file, 'r') as f:
        # ids = set(line.strip()[:7] for line in f if line.strip())
        ids = set()
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Remove # from 1st and 4th position (original string)
            chars = list(line)
            if len(chars) >= 7:
                # Remove 4th char first (index 3), then 1st char (index 0)
                if chars[3] == '#':
                    chars.pop(3)
                if chars[0] == '#':
                    chars.pop(0)
                id_candidate = ''.join(chars[:7])
                ids.add(id_candidate)
        print(f"IDs loaded: {len(ids)} unique IDs found")
        print("Sample IDs:", list(ids)[:10])   

    with open(cobol_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Stop processing if PROCEDURE DIVISION is found
            if 'PROCEDURE DIVISION' in line:
                outfile.write(line)
                break
            line_to_check = line.lstrip()
            # Mask if line starts with '*' OR contains 'AUTHOR' (case-insensitive)
            if line_to_check.startswith('*') or 'author' in line.lower():
                print(f"Masking IDs in line: {line.strip()}")
                for id_ in ids:
                    if id_ in line:
                        line = line.replace(id_, '@@@@@@@')
                outfile.write(line)
            else:
                outfile.write(line)
        # Write the rest of the file unchanged
        for line in infile:
            outfile.write(line)

CobIDMask()

