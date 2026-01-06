# Fully Loaded Personal Finance Manager App
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import defaultdict

# --- File to store data ---
DATA_FILE = "finance_data.csv"

# --- Initialize CSV if not exist ---
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Type", "Category", "Amount", "Note"])

# --- Budget settings (for alerts) ---
BUDGETS = {
    "Food": 5000,
    "Shopping": 3000,
    "Travel": 4000,
    "Bills": 7000
}

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

    # Save to CSV
    with open(DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, entry_type, category, amount, note])

    clear_inputs()
    update_summary()
    messagebox.showinfo("Success", f"{entry_type} entry added!")

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

    # Budget alerts
    alert_text = ""
    expense_by_cat = defaultdict(float)
    for d in data:
        if d['Type'] == "Expense":
            expense_by_cat[d['Category']] += d['Amount']
    for cat, spent in expense_by_cat.items():
        if cat in BUDGETS and spent > BUDGETS[cat]:
            alert_text += f"⚠️ {cat} exceeded budget!\n"
    alert_label.config(text=alert_text)

    # Update charts
    plot_expense_chart(data)
    plot_trend_chart(data)

def plot_expense_chart(data):
    categories = defaultdict(float)
    for d in data:
        if d['Type'] == "Expense":
            categories[d['Category']] += d['Amount']

    pie_fig.clear()
    ax = pie_fig.add_subplot(111)
    if categories:
        ax.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%", startangle=140)
        ax.set_title("Expenses by Category", fontsize=14)
    else:
        ax.text(0.5, 0.5, "No expense data yet!", ha='center', va='center', fontsize=14)
        ax.axis('off')
    pie_canvas.draw()

def plot_trend_chart(data):
    monthly_income = defaultdict(float)
    monthly_expense = defaultdict(float)
    for d in data:
        month = datetime.strptime(d['Date'], "%Y-%m-%d").strftime("%Y-%m")
        if d['Type'] == "Income":
            monthly_income[month] += d['Amount']
        else:
            monthly_expense[month] += d['Amount']

    months = sorted(list(set(list(monthly_income.keys()) + list(monthly_expense.keys()))))
    income_vals = [monthly_income[m] for m in months]
    expense_vals = [monthly_expense[m] for m in months]

    trend_fig.clear()
    ax = trend_fig.add_subplot(111)
    if months:
        ax.plot(months, income_vals, marker='o', label="Income", color="green")
        ax.plot(months, expense_vals, marker='o', label="Expense", color="red")
        ax.set_title("Monthly Income vs Expense", fontsize=14)
        ax.set_ylabel("Amount (₹)")
        ax.set_xlabel("Month")
        ax.legend()
        ax.grid(True)
    else:
        ax.text(0.5, 0.5, "No data yet!", ha='center', va='center', fontsize=14)
        ax.axis('off')
    trend_canvas.draw()

def export_report():
    data = read_data()
    if not data:
        messagebox.showwarning("No Data", "No data to export!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Category", "Amount", "Note"])
            for d in data:
                writer.writerow([d['Date'], d['Type'], d['Category'], d['Amount'], d['Note']])
        messagebox.showinfo("Exported", f"Report exported to {file_path}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Personal Finance Manager - Full Version")
root.geometry("1000x700")
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
tk.Button(input_frame, text="Export Report", command=export_report, bg="blue", fg="white", font=("Arial", 12)).grid(row=4, column=0, columnspan=4, pady=5)

# --- Summary Frame ---
summary_frame = tk.Frame(root, padx=10, pady=10)
summary_frame.pack(fill=tk.X)

income_label = tk.Label(summary_frame, text="Total Income: ₹0", font=("Arial", 12))
income_label.pack(anchor="w")
expense_label = tk.Label(summary_frame, text="Total Expense: ₹0", font=("Arial", 12))
expense_label.pack(anchor="w")
balance_label = tk.Label(summary_frame, text="Balance: ₹0", font=("Arial", 12, "bold"))
balance_label.pack(anchor="w")
alert_label = tk.Label(summary_frame, text="", font=("Arial", 12), fg="red")
alert_label.pack(anchor="w")

# --- Chart Frames ---
chart_frame = tk.Frame(root, padx=10, pady=10)
chart_frame.pack(fill=tk.BOTH, expand=True)

# Expense Pie Chart
pie_fig = plt.Figure(figsize=(5,4))
pie_canvas = FigureCanvasTkAgg(pie_fig, master=chart_frame)
pie_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Monthly Trend Chart
trend_fig = plt.Figure(figsize=(5,4))
trend_canvas = FigureCanvasTkAgg(trend_fig, master=chart_frame)
trend_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# --- Initialize ---
update_summary()

root.mainloop()
