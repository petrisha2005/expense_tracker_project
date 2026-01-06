# Personal Finance Manager App - Upgraded Version
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- File to store data ---
DATA_FILE = "finance_data.csv"

# --- Initialize CSV if it doesn't exist ---
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Type", "Category", "Amount", "Note"])

# --- Helper Functions ---
def add_entry():
    date = date_entry.get()
    entry_type = type_var.get()
    category = category_entry.get()
    amount = amount_entry.get()
    note = note_entry.get()

    if not (date and entry_type and category and amount):
        messagebox.showwarning("Input Error", "Please fill all required fields!")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Input Error", "Amount must be a number!")
        return

    with open(DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, entry_type, category, amount, note])

    messagebox.showinfo("Success", "Entry Added!")
    clear_inputs()
    update_summary()

def clear_inputs():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

def read_data():
    data = []
    with open(DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['Amount'] = float(row['Amount'])
            data.append(row)
    return data

def update_summary():
    data = read_data()
    total_income = sum(d['Amount'] for d in data if d['Type']=="Income")
    total_expense = sum(d['Amount'] for d in data if d['Type']=="Expense")
    balance = total_income - total_expense

    income_label.config(text=f"Total Income: ₹{total_income}")
    expense_label.config(text=f"Total Expense: ₹{total_expense}")
    balance_label.config(text=f"Balance: ₹{balance}")

    plot_expense_chart(data)

def plot_expense_chart(data):
    categories = {}
    for d in data:
        if d['Type'] == "Expense":
            categories[d['Category']] = categories.get(d['Category'], 0) + d['Amount']

    fig.clear()
    ax = fig.add_subplot(111)

    if categories:
        ax.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%", startangle=140)
        ax.set_title("Expenses by Category", fontsize=14)
    else:
        ax.text(0.5, 0.5, "No expense data yet!", ha='center', va='center', fontsize=14)
        ax.axis('off')

    canvas.draw()

# --- GUI Setup ---
root = tk.Tk()
root.title("Personal Finance Manager")
root.geometry("950x650")
root.resizable(True, True)

# --- Input Frame ---
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(fill=tk.X)

tk.Label(input_frame, text="Date (YYYY-MM-DD):", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
date_entry = tk.Entry(input_frame, font=("Arial", 11))
date_entry.grid(row=0, column=1, sticky="w")

type_var = tk.StringVar()
type_var.set("Expense")
tk.Radiobutton(input_frame, text="Expense", variable=type_var, value="Expense", font=("Arial", 11)).grid(row=0, column=2)
tk.Radiobutton(input_frame, text="Income", variable=type_var, value="Income", font=("Arial", 11)).grid(row=0, column=3)

tk.Label(input_frame, text="Category:", font=("Arial", 11)).grid(row=1, column=0, sticky="w")
category_entry = tk.Entry(input_frame, font=("Arial", 11))
category_entry.grid(row=1, column=1, sticky="w")

tk.Label(input_frame, text="Amount:", font=("Arial", 11)).grid(row=1, column=2, sticky="w")
amount_entry = tk.Entry(input_frame, font=("Arial", 11))
amount_entry.grid(row=1, column=3, sticky="w")

tk.Label(input_frame, text="Note:", font=("Arial", 11)).grid(row=2, column=0, sticky="w")
note_entry = tk.Entry(input_frame, width=50, font=("Arial", 11))
note_entry.grid(row=2, column=1, columnspan=3, sticky="w")

tk.Button(input_frame, text="Add Entry", command=add_entry, bg="green", fg="white", font=("Arial", 12)).grid(row=3, column=0, columnspan=4, pady=10)

# --- Summary Frame ---
summary_frame = tk.Frame(root, padx=10, pady=10)
summary_frame.pack(fill=tk.X)

income_label = tk.Label(summary_frame, text="Total Income: ₹0", font=("Arial", 12))
income_label.pack(anchor="w")
expense_label = tk.Label(summary_frame, text="Total Expense: ₹0", font=("Arial", 12))
expense_label.pack(anchor="w")
balance_label = tk.Label(summary_frame, text="Balance: ₹0", font=("Arial", 12, "bold"))
balance_label.pack(anchor="w")

# --- Chart Frame ---
chart_frame = tk.Frame(root, padx=10, pady=10)
chart_frame.pack(fill=tk.BOTH, expand=True)

fig = plt.Figure(figsize=(6,5))
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- Initialize Summary ---
update_summary()

root.mainloop()
