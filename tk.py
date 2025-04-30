import tkinter as tk
from email.message import Message
from tkinter import messagebox
from tkinter import StringVar, Label, Entry, Listbox, Scrollbar, Button
from db import Database
db = Database('store.db')

def popul_List():
    part_list.delete(0, "end")
    for row in db.fetch():
        part_list.insert("end", row)

def add_items():
    if part_text.get() == '' or  customer_text.get()== '' or retailer_text.get() == ' ' or  price_text.get() == '':
        messagebox.showerror("Required fileds", "Please insert data into the boxes ")
        return
    else:
        db.insert(part_text.get(), customer_text.get(), retailer_text.get(), price_text.get())
        part_list.delete(0, "end")
        part_list.insert("end",
                         f"Part: {part_text.get()}, Customer: {customer_text.get()}, Retailer: {retailer_text.get()}, Price: {price_text.get()}")
        clear_text()
        popul_List()
def select_item(event):
    try:
        global selected_item
        index = part_list.curselection()[0]
        selected_item = part_list.get(index)

        part_entry.delete(0, "end")
        part_entry.insert('end', selected_item[1])
        customer_entry.delete(0, "end")
        customer_entry.insert('end', selected_item[2])
        retailer_entry.delete(0, "end")
        retailer_entry.insert('end', selected_item[3])
        price_entry.delete(0, "end")
        price_entry.insert('end', selected_item[4])
    except IndexError:
        pass

def remove_items():
    db.delete(selected_item[0])
    clear_text()
    popul_List()
def upd_items():
    db.update(selected_item[0],part_text.get(), customer_text.get(), retailer_text.get(), price_text.get())
    clear_text()
    popul_List()
def clear_text():
    part_entry.delete(0, "end")
    customer_entry.delete(0, "end")
    retailer_entry.delete(0, "end")
    price_entry.delete(0, "end")

class winApp(tk.Tk):
    def __init__(self):
        super().__init__()

app = winApp()
part_text = StringVar()
part_label = Label(app, text='Part Name', font=('bold',14), pady=20)
part_label.grid(row=0, column=0)
part_entry = Entry(app,  textvariable=part_text)
part_entry.grid(row=0, column=1)

customer_text = StringVar()
customer_label = Label(app, text='Customer', font=('bold',14))
customer_label.grid(row=0, column=2)
customer_entry = Entry(app,  textvariable=customer_text)
customer_entry.grid(row=0, column=3)

retailer_text = StringVar()
retailer_label = Label(app, text='Retailer', font=('bold',14))
retailer_label.grid(row=1, column=0)
retailer_entry = Entry(app,  textvariable=retailer_text)
retailer_entry.grid(row=1, column=1)

price_text = StringVar()
price_label = Label(app, text='Price', font=('bold',14))
price_label.grid(row=1, column=2)
price_entry = Entry(app,  textvariable=price_text)
price_entry.grid(row=1, column=3)

part_list = Listbox(app, height=8, width=50, border=0)
part_list.grid(row=3, column=0, columnspan=3, rowspan=6, padx=20, pady=20, sticky="nsew")

part_list.bind("<<ListboxSelect>>", select_item)
# Scrollbar (placed inside the same grid row)
scollbar = Scrollbar(app)
scollbar.grid(row=3, column=2, rowspan=6, sticky="ns")  # Adjust column to be closer to Listbox

# Link scrollbar to Listbox
part_list.configure(yscrollcommand=scollbar.set)

add_btn = Button(app,text="Add", width=12, command=add_items )
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app,text="Remove", width=12, command=remove_items )
remove_btn.grid(row=2, column=1)

upd_btn = Button(app,text="Update", width=12, command=upd_items )
upd_btn.grid(row=2, column=2)

clear_btn = Button(app,text="Clear", width=12, command=clear_text)
clear_btn.grid(row=2, column=3)

app.title("Part-manager")
app.geometry("700x350")



popul_List()


app.mainloop()