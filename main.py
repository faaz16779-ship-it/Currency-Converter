import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"
API_KEY_FILE = "api_key.txt"
API_KEY = ""

if os.path.exists(API_KEY_FILE):
    with open(API_KEY_FILE, "r") as f:
        API_KEY = f.read().strip()

BASE_URL = "https://v6.exchangerate-api.com/v6/"

CURRENCIES = [
    "USD", "EUR", "RUB", "GBP", "JPY", "CNY", "KZT", "UAH",
    "CAD", "AUD", "CHF", "SEK", "NOK", "INR", "BRL"
]


class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("650x520")
        self.root.resizable(False, False)

        self.history = []
        self.load_history()

        self.create_widgets()

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text="API Key:").pack(side=tk.LEFT)
        self.api_entry = ttk.Entry(top_frame, width=40, show="*")
        self.api_entry.pack(side=tk.LEFT, padx=5)
        self.api_entry.insert(0, API_KEY)
        ttk.Button(top_frame, text="Set Key", command=self.set_api_key).pack(side=tk.LEFT)

        conv_frame = ttk.LabelFrame(self.root, text="Conversion", padding=10)
        conv_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(conv_frame, text="Amount:").grid(row=0, column=0, sticky="w", pady=5)
        self.amount_entry = ttk.Entry(conv_frame, width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(conv_frame, text="From:").grid(row=1, column=0, sticky="w", pady=5)
        self.from_combo = ttk.Combobox(conv_frame, values=CURRENCIES, state="readonly", width=18)
        self.from_combo.grid(row=1, column=1, padx=5, pady=5)
        self.from_combo.set("USD")

        ttk.Label(conv_frame, text="To:").grid(row=2, column=0, sticky="w", pady=5)
        self.to_combo = ttk.Combobox(conv_frame, values=CURRENCIES, state="readonly", width=18)
        self.to_combo.grid(row=2, column=1, padx=5, pady=5)
        self.to_combo.set("EUR")

        self.result_label = ttk.Label(conv_frame, text="", font=("Arial", 12, "bold"))
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(conv_frame, text="Convert", command=self.convert).grid(row=4, column=0, columnspan=2, pady=5)

        hist_frame = ttk.LabelFrame(self.root, text="History", padding=10)
        hist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("Date", "Amount", "From", "To", "Result")
        self.tree = ttk.Treeview(hist_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(hist_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.refresh_tree()

    def set_api_key(self):
        global API_KEY
        key = self.api_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "API key cannot be empty.")
            return
        API_KEY = key
        with open(API_KEY_FILE, "w") as f:
            f.write(key)
        messagebox.showinfo("Success", "API key saved.")

    def get_rates(self, base_currency):
        if not API_KEY:
            messagebox.showerror("Error", "Please set your API key first.")
            return None
        url = f"{BASE_URL}{API_KEY}/latest/{base_currency}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("result") == "success":
                return data["conversion_rates"]
            else:


15: 22
messagebox.showerror("Error", f"API error: {data.get('error-type', 'unknown')}")
return None
except requests.exceptions.RequestException as e:
messagebox.showerror("Error", f"Request failed: {e}")
return None


def convert(self):
    amount_str = self.amount_entry.get().strip()
    if not amount_str:
        messagebox.showerror("Error", "Enter an amount.")
        return
    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return
    if amount <= 0:
        messagebox.showerror("Error", "Amount must be a positive number.")
        return

    from_curr = self.from_combo.get()
    to_curr = self.to_combo.get()
    if from_curr == to_curr:
        result = amount
        self.result_label.config(text=f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}")
        self.add_to_history(amount, from_curr, to_curr, result)
        return

    rates = self.get_rates(from_curr)
    if rates is None:
        return
    if to_curr not in rates:
        messagebox.showerror("Error", f"Currency {to_curr} not found.")
        return

    result = amount * rates[to_curr]
    self.result_label.config(text=f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}")
    self.add_to_history(amount, from_curr, to_curr, result)


def add_to_history(self, amount, from_curr, to_curr, result):
    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
        "from": from_curr,
        "to": to_curr,
        "result": result
    }
    self.history.append(record)
    self.save_history()
    self.refresh_tree()


def save_history(self):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(self.history, f, indent=2, ensure_ascii=False)


def load_history(self):
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                self.history = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.history = []


def refresh_tree(self):
    for row in self.tree.get_children():
        self.tree.delete(row)
    for record in reversed(self.history):
        self.tree.insert("", 0, values=(
            record["date"],
            f"{record['amount']:.2f}",
            record["from"],
            record["to"],
            f"{record['result']:.2f}"
        ))


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
