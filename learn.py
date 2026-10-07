import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

file = "prices.csv"

if not os.path.exists(file):
    pd.DataFrame(columns=["Product", "Price", "Date"]).to_csv(file, index=False)


def show(text):
    result.delete("1.0", tk.END)
    result.insert(tk.END, text)


def add_price():
    try:
        name = product.get()
        price = float(price_box.get())
        date = date_box.get()

        if not name or price <= 0:
            raise ValueError("Enter valid details.")

        data = pd.read_csv(file)
        data.loc[len(data)] = [name, price, date]
        data.to_csv(file, index=False)
        messagebox.showinfo("Done", "Price saved!")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


def show_data():
    show(pd.read_csv(file).to_string(index=False))


def check_price():
    data = pd.read_csv(file)
    name = search_box.get()
    prices = data[data.Product.str.lower() == name.lower()].Price

    if prices.empty:
        show("Product not found.")
        return

    avg = np.mean(prices)
    change = prices.iloc[-1] - prices.iloc[0]

    text = f"Product: {name}\nAverage Price: ₹{avg:.2f}\nPrice Change: ₹{change:.2f}"

    if abs(change) >= 10:
        text += "\n\nBig price change noticed!"

    show(text)


def compare():
    data = pd.read_csv(file)
    avg = data.groupby("Product").Price.mean()
    show("Average Prices\n\n" + avg.to_string())


def price_graph():
    data = pd.read_csv(file)

    for name in data.Product.unique():
        x = data[data.Product == name]
        plt.plot(x.Date, x.Price, marker="o", label=name)

    plt.title("Price Changes")
    plt.xlabel("Date")
    plt.ylabel("Price (₹)")
    plt.legend()
    plt.show()


def average_graph():
    data = pd.read_csv(file)
    data.groupby("Product").Price.mean().plot(kind="bar")
    plt.title("Average Product Prices")
    plt.ylabel("Price (₹)")
    plt.show()


# GUI
window = tk.Tk()
window.title("Product Price Tracker")
window.geometry("550x600")

tk.Label(window, text="PRODUCT PRICE TRACKER",
         font=("Arial", 18, "bold")).pack(pady=15)

for text, widget in [
    ("Product Name", "product"),
    ("Price", "price_box"),
    ("Date (YYYY-MM-DD)", "date_box"),
]:
    tk.Label(window, text=text).pack()
    globals()[widget] = tk.Entry(window)
    globals()[widget].pack()

tk.Button(window, text="Add Price", command=add_price).pack(pady=8)

tk.Label(window, text="Search Product").pack()
search_box = tk.Entry(window)
search_box.pack()

buttons = [
    ("Check Price", check_price),
    ("Compare Products", compare),
    ("Show All Data", show_data),
    ("Price Graph", price_graph),
    ("Average Graph", average_graph)
]

for text, command in buttons:
    tk.Button(window, text=text, command=command).pack(pady=5)

result = tk.Text(window, height=12, width=60)
result.pack(pady=15)

window.mainloop()