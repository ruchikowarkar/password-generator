from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please make sure you haven't left any fields empty")

    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered: \nUsername: {username}\nPassword: {password}\nClick Ok to save.")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(new_data, data_file, indent=4)

            else:
                # Updating old data with new data
                data.update(new_data)

            finally:
                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)

                    # data_file.write(f"{website} | {username} | {password}\n")
                    website_input.delete(0, END)
                    password_input.delete(0, END)
# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except json.decoder.JSONDecodeError:
        messagebox.showinfo(message="No data in the manager.")

    else:
        search = website_input.get()
        if search in data:
            messagebox.showinfo(title=search,
                                message=f"Username: {data[search]['username']}\nPassword: {data[search]['password']}")
        else:
            messagebox.showinfo(message=f"No details for the website {search} exists.")
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1, sticky="EW")

website_input = Entry(width=35)
website_input.grid(column=1, row=1, sticky="EW")
website_input.focus()

search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="EW")

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2, sticky="EW")

username_input = Entry(width=35)
username_input.grid(column=1, row=2, columnspan=2, sticky="EW")
username_input.insert(0, "my@email.com")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3, sticky="EW")

password_input = Entry(width=21)
password_input.grid(column=1, row=3, sticky="EW")

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()
