from tkinter import *
from tkinter import ttk, messagebox

contacts = {}

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    for name, info in contacts.items():
        tree.insert("", END, values=(name, info["email"], info["phone"]))

def add_contact():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Name cannot be empty!")
        return

    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Invalid Email!")
        return

    if not (phone.isdigit() and len(phone) == 10):
        messagebox.showerror("Error", "Phone must be 10 digits!")
        return

    contacts[name] = {"email": email, "phone": phone}

    refresh_table()
    clear_entries()
    messagebox.showinfo("Success", "Contact Added Successfully!")

def search_contact():
    name = name_entry.get().strip()
    if name in contacts:
        email_entry.delete(0, END)
        phone_entry.delete(0, END)

        email_entry.insert(0, contacts[name]["email"])
        phone_entry.insert(0, contacts[name]["phone"])

        messagebox.showinfo("Found", "Contact Found!")
    else:
        messagebox.showerror("Error", "Contact Not Found!")

def update_contact():
    name = name_entry.get().strip()
    if name not in contacts:
        messagebox.showerror("Error", "Contact Not Found!")
        return
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Invalid Email!")
        return

    if not (phone.isdigit() and len(phone) == 10):
        messagebox.showerror("Error", "Invalid Phone Number!")
        return

    contacts[name] = {"email": email, "phone": phone}

    refresh_table()
    messagebox.showinfo("Success", "Contact Updated!")

def delete_contact():
    name = name_entry.get().strip()
    if name in contacts:
        del contacts[name]
        refresh_table()
        clear_entries()
        messagebox.showinfo("Deleted", "Contact Deleted!")
    else:
        messagebox.showerror("Error", "Contact Not Found!")

def save_contacts():
    try:
        with open("CONTACTS.txt", "w") as f:
            for name, info in contacts.items():
                f.write(f"{name},{info['email']},{info['phone']}\n")

        messagebox.showinfo("Success", "Contacts Saved!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def load_contacts():
    try:
        contacts.clear()
        with open("CONTACTS.txt", "r") as f:
            for line in f:
                name, email, phone = line.strip().split(",")

                contacts[name] = {
                    "email": email,
                    "phone": phone
                }

        refresh_table()
        messagebox.showinfo("Success", "Contacts Loaded!")
    except FileNotFoundError:
        messagebox.showerror("Error", "No Saved File Found!")

def clear_entries():
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    phone_entry.delete(0, END)

def select_contact(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    clear_entries()
    name_entry.insert(0, values[0])
    email_entry.insert(0, values[1])
    phone_entry.insert(0, values[2])

root = Tk()
root.title("Contact Management System")
root.geometry("750x500")
root.resizable(False, False)

title = Label(
    root,
    text="CONTACT MANAGEMENT SYSTEM",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)

frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Name", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5)
name_entry = Entry(frame, width=30)
name_entry.grid(row=0, column=1)

Label(frame, text="Email", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5)
email_entry = Entry(frame, width=30)
email_entry.grid(row=1, column=1)

Label(frame, text="Phone", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=5)
phone_entry = Entry(frame, width=30)
phone_entry.grid(row=2, column=1)

btn_frame = Frame(root)
btn_frame.pack(pady=10)
Button(btn_frame, text="Add", width=12, command=add_contact).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Search", width=12, command=search_contact).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Update", width=12, command=update_contact).grid(row=0, column=2, padx=5)
Button(btn_frame, text="Delete", width=12, command=delete_contact).grid(row=1, column=0, padx=5, pady=5)
Button(btn_frame, text="Save", width=12, command=save_contacts).grid(row=1, column=1, padx=5, pady=5)
Button(btn_frame, text="Load", width=12, command=load_contacts).grid(row=1, column=2, padx=5, pady=5)

tree = ttk.Treeview(
    root,
    columns=("Name", "Email", "Phone"),
    show="headings",
    height=12
)
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Phone", text="Phone")
tree.column("Name", width=180)
tree.column("Email", width=280)
tree.column("Phone", width=180)
tree.pack(pady=15)
tree.bind("<<TreeviewSelect>>", select_contact)
root.mainloop()