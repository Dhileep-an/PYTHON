import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("450x450")
        
        self.history = []

        # Length selection
        ttk.Label(root, text="Password Length:").pack(anchor="w", padx=20, pady=(15, 0))
        self.length_var = tk.IntVar(value=12)
        self.spin_length = ttk.Spinbox(root, from_=8, to=64, textvariable=self.length_var, width=10)
        self.spin_length.pack(anchor="w", padx=20, pady=5)

        # Settings
        self.var_upper = tk.BooleanVar(value=True)
        self.var_lower = tk.BooleanVar(value=True)
        self.var_digits = tk.BooleanVar(value=True)
        self.var_symbols = tk.BooleanVar(value=True)
        self.var_exclude_ambiguous = tk.BooleanVar(value=False)

        ttk.Checkbutton(root, text="Include Uppercase Letters (A-Z)", variable=self.var_upper).pack(anchor="w", padx=20)
        ttk.Checkbutton(root, text="Include Lowercase Letters (a-z)", variable=self.var_lower).pack(anchor="w", padx=20)
        ttk.Checkbutton(root, text="Include Digits (0-9)", variable=self.var_digits).pack(anchor="w", padx=20)
        ttk.Checkbutton(root, text="Include Symbols (!@#$...)", variable=self.var_symbols).pack(anchor="w", padx=20)
        ttk.Checkbutton(root, text="Exclude Ambiguous (0, O, l, 1, I)", variable=self.var_exclude_ambiguous).pack(anchor="w", padx=20, pady=(0, 10))

        # Generate Button
        ttk.Button(root, text="Generate Password", command=self.generate_password).pack(pady=10)

        # Result Display
        self.entry_pwd = ttk.Entry(root, font=("Consolas", 12), width=30)
        self.entry_pwd.pack(pady=5)

        # Strength Meter
        self.lbl_strength = tk.Label(root, text="Strength: N/A", font=("Arial", 10, "bold"))
        self.lbl_strength.pack(pady=5)

        # Copy Button
        ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=5)

        # History Display
        ttk.Label(root, text="Session History (Last 5):").pack(anchor="w", padx=20, pady=(10, 0))
        self.lst_history = tk.Listbox(root, height=5, font=("Consolas", 9))
        self.lst_history.pack(fill="x", padx=20, pady=5)

    def generate_password(self):
        length = self.length_var.get()
        if length < 8:
            messagebox.showerror("Error", "Minimum length must be at least 8 characters.")
            return

        pools = []
        if self.var_upper.get():
            pools.append(string.ascii_uppercase)
        if self.var_lower.get():
            pools.append(string.ascii_lowercase)
        if self.var_digits.get():
            pools.append(string.digits)
        if self.var_symbols.get():
            pools.append(string.punctuation)

        if len(pools) < 2:
            messagebox.showerror("Error", "Select at least 2 character types.")
            return

        if self.var_exclude_ambiguous.get():
            ambiguous = "0Ol1I"
            pools = [''.join([c for c in pool if c not in ambiguous]) for pool in pools]

        # Ensure at least one character from each selected pool
        password = [secrets.choice(pool) for pool in pools]
        
        # Fill remaining length
        all_chars = ''.join(pools)
        for _ in range(length - len(password)):
            password.append(secrets.choice(all_chars))

        # Shuffle cryptographically
        for i in range(len(password) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password[i], password[j] = password[j], password[i]

        final_pwd = ''.join(password)
        self.entry_pwd.delete(0, tk.END)
        self.entry_pwd.insert(0, final_pwd)

        self.update_strength(length, len(pools))
        self.update_history(final_pwd)

    def update_strength(self, length, pool_count):
        if length >= 14 and pool_count >= 3:
            self.lbl_strength.config(text="Strength: Strong", fg="green")
        elif length >= 10 and pool_count >= 2:
            self.lbl_strength.config(text="Strength: Medium", fg="orange")
        else:
            self.lbl_strength.config(text="Strength: Weak", fg="red")

    def copy_to_clipboard(self):
        pwd = self.entry_pwd.get()
        if pwd:
            pyperclip.copy(pwd)
            messagebox.showinfo("Success", "Password copied to clipboard!")

    def update_history(self, pwd):
        self.history.insert(0, pwd)
        if len(self.history) > 5:
            self.history.pop()
        
        self.lst_history.delete(0, tk.END)
        for p in self.history:
            self.lst_history.insert(tk.END, p)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
