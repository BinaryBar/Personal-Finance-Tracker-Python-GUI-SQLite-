import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime

# Initialize database
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL
    )
''')
conn.commit()

# Insert expense
def add_expense():
    date = date_entry.get()
    category = category_var.get()
    description = desc_entry.get()
    amount = amount_entry.get()

    if not date or not category or not amount:
        messagebox.showwarning("Warning", "Please fill in all required fields.")
        return

    try:
        float(amount)
    except:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    c.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
              (date, category, description, amount))
    conn.commit()
    messagebox.showinfo("Success", "Expense added!")
    update_tree()

# Display entries
def update_tree():
    for i in tree.get_children():
        tree.delete(i)
    c.execute("SELECT date, category, description, amount FROM expenses ORDER BY id DESC")
    for row in c.fetchall():
        tree.insert("", "end", values=row)

# GUI setup
root = tk.Tk()
root.title("💸 Personal Finance Tracker")
root.geometry("700x500")

# Inputs
tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root)
date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
date_entry.pack()

tk.Label(root, text="Category:").pack()
category_var = tk.StringVar()
category_menu = ttk.Combobox(root, textvariable=category_var, values=["Food", "Bills", "Transport", "Health", "Others"])
category_menu.pack()

tk.Label(root, text="Description (optional):").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Amount (BDT):").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Add Expense", command=add_expense, bg="green", fg="white").pack(pady=10)

# Treeview (Table)
tree = ttk.Treeview(root, columns=("Date", "Category", "Description", "Amount"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True)

update_tree()
root.mainloop()
