import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

CSV_FILE = "fridge.csv"

class FridgeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menedżer lodówki")
        self.geometry("700x500")

        # Pola do dodawania produktów
        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Produkt:").grid(row=0, column=0, padx=5)
        self.entry_name = ttk.Entry(form)
        self.entry_name.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Ilość:").grid(row=0, column=2, padx=5)
        self.entry_qty = ttk.Entry(form, width=5)
        self.entry_qty.grid(row=0, column=3, padx=5)

        ttk.Label(form, text="Data ważności (RRRR-MM-DD):").grid(row=0, column=4, padx=5)
        self.entry_exp = ttk.Entry(form)
        self.entry_exp.grid(row=0, column=5, padx=5)

        add_btn = ttk.Button(form, text="Dodaj", command=self.add_product)
        add_btn.grid(row=0, column=6, padx=5)

        # Tabela produktów
        self.table = ttk.Treeview(
            self, columns=("Produkt", "Ilość", "Data ważności", "Status"), show="headings"
        )
        for col in ("Produkt", "Ilość", "Data ważności", "Status"):
            self.table.heading(col, text=col)
        self.table.pack(fill="both", expand=True, pady=10)

        # Wczytaj istniejące produkty
        self.products = []
        self.load_data()
        self.refresh_table()

    def add_product(self):
        name = self.entry_name.get().strip()
        qty = self.entry_qty.get().strip()
        exp_date = self.entry_exp.get().strip()

        if not name or not qty or not exp_date:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
            return

        try:
            exp = datetime.strptime(exp_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Błąd", "Niepoprawny format daty (RRRR-MM-DD)")
            return

        self.products.append({"name": name, "qty": qty, "exp": exp})
        self.save_data()
        self.refresh_table()

        self.entry_name.delete(0, tk.END)
        self.entry_qty.delete(0, tk.END)
        self.entry_exp.delete(0, tk.END)

    def get_status(self, exp):
        today = datetime.today().date()
        if exp < today:
            return "❌ Przeterminowany"
        elif exp <= today + timedelta(days=2):
            return "⚠️ Kończy się"
        return "✅ OK"

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for p in self.products:
            status = self.get_status(p["exp"])
            self.table.insert("", "end", values=(p["name"], p["qty"], p["exp"], status))

    def save_data(self):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Produkt", "Ilość", "Data"])
            for p in self.products:
                writer.writerow([p["name"], p["qty"], p["exp"]])

    def load_data(self):
        if not os.path.exists(CSV_FILE):
            return
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                exp = datetime.strptime(row["Data"], "%Y-%m-%d").date()
                self.products.append({"name": row["Produkt"], "qty": row["Ilość"], "exp": exp})


if __name__ == "__main__":
    app = FridgeApp()
    app.mainloop()
