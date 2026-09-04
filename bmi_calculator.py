import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database Setup
def init_db():
    conn = sqlite3.connect("bmi_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("700x550")
        
        init_db()
        
        # UI Elements
        ttk.Label(root, text="User Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_user = ttk.Entry(root)
        self.entry_user.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(root, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_weight = ttk.Entry(root)
        self.entry_weight.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(root, text="Height (m):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_height = ttk.Entry(root)
        self.entry_height.grid(row=2, column=1, padx=10, pady=10)

        self.btn_calc = ttk.Button(root, text="Calculate & Save", command=self.calculate_bmi)
        self.btn_calc.grid(row=3, column=0, columnspan=2, pady=10)

        self.lbl_result = tk.Label(root, text="Result: N/A", font=("Arial", 12, "bold"))
        self.lbl_result.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_chart = ttk.Button(root, text="View Trend Chart", command=self.show_trend)
        self.btn_chart.grid(row=5, column=0, columnspan=2, pady=5)

        self.chart_frame = ttk.Frame(root)
        self.chart_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="nsew")

    def calculate_bmi(self):
        user = self.entry_user.get().strip()
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())
            if weight <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive numeric values for weight and height.")
            return

        if not user:
            messagebox.showerror("Invalid Input", "Please enter a user name.")
            return

        bmi = round(weight / (height ** 2), 2)
        
        if bmi < 18.5:
            category, color = "Underweight", "#3498db"
        elif 18.5 <= bmi <= 24.9:
            category, color = "Normal weight", "#2ecc71"
        elif 25 <= bmi <= 29.9:
            category, color = "Overweight", "#f39c12"
        else:
            category, color = "Obese", "#e74c3c"

        self.lbl_result.config(text=f"BMI: {bmi} ({category})", fg=color)

        try:
            conn = sqlite3.connect("bmi_history.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bmi_records (username, weight, height, bmi, category, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (user, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M"))
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save record: {e}")

    def show_trend(self):
        user = self.entry_user.get().strip()
        if not user:
            messagebox.showerror("Invalid Input", "Enter a user name to fetch history.")
            return

        try:
            conn = sqlite3.connect("bmi_history.db")
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, bmi FROM bmi_records WHERE username = ? ORDER BY id ASC", (user,))
            data = cursor.fetchall()
            conn.close()

            if not data:
                messagebox.showinfo("No Data", f"No records found for user: {user}")
                return

            dates = [row[0] for row in data]
            bmis = [row[1] for row in data]

            for widget in self.chart_frame.winfo_children():
                widget.destroy()

            fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
            ax.plot(dates, bmis, marker='o', color='#2980b9', linestyle='-')
            ax.set_title(f"BMI History for {user}")
            ax.set_ylabel("BMI Value")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch records: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
