import tkinter as tk
from tkinter import messagebox
import json
from email.message import EmailMessage
import smtplib
import ssl
import os
FONT = ("times new roman", 13, "bold")
btnFont = ("Courier", 24, "bold")


def open_send_page(window, cont_button, canvas):
    cont_button.destroy()
    canvas.destroy()
    window.config(padx=150, pady=150)

    # Label
    r_mail_label = tk.Label(text="Recipient's Mail:", font=FONT)
    r_mail_label.grid(column=0, row=1)

    title_label = tk.Label(text="Msg-Title:", font=FONT)
    title_label.grid(column=0, row=2)

    body_label = tk.Label(text="Msg-Body:", font=FONT)
    body_label.grid(column=0, row=3)

    # Entry
    r_mail_entry = tk.Entry(width=24)
    r_mail_entry.focus()
    r_mail_entry.grid(column=1, row=1, pady=7)

    title_entry = tk.Entry(width=25)
    title_entry.grid(column=1, row=2, pady=7)

    # Text
    body_text = tk.Text(height=4, width=20)
    body_text.grid(column=1, row=3, pady=7)

    # Button
    send_button = tk.Button(text="Send", font=FONT, command=lambda: process_mail(r_mail_entry, title_entry, body_text))
    send_img = tk.PhotoImage(file="Emmail-send-logo.png")
    send_button.config(image=send_img)
    send_button.grid(column=2, row=3, padx=5)
    send_button.config(pady=2, padx=2)

    canvas = tk.Canvas(width=150, height=150)
    logo_img = tk.PhotoImage(file="Emmail-logo-sm.png")
    canvas.create_image(75, 75, image=logo_img)
    canvas.grid(column=1, row=0, columnspan=1)

    window.mainloop()


def save_info(mail, subject, message):
    email = mail.get()
    subject = subject.get()
    message = message.get("1.0", tk.END).rstrip("\n")
    temp_msg_dict = {
        "mail": {
            "email": email,
            "title": subject,
            "message": message
        }
    }

    with open("temp.json", "w") as temp_data:
        json.dump(obj=temp_msg_dict, fp=temp_data, indent=4)

    # try:
    #     with open(file="temp.json", mode="r") as temp_data:
    #         data = json.load(fp=temp_data)
    #         data.update(temp_msg_dict)
    #     with open(file="temp.json", mode="w") as temp_data:
    #         json.dump(obj=data, fp=temp_data, indent=4)
    # except FileNotFoundError:
    #     with open("temp.json", "w") as temp_data:
    #         json.dump(obj=temp_msg_dict, fp=temp_data, indent=4)
    # finally:
    #     with open(file="temp.json", mode="r") as temp_data:
    #         data = json.load(fp=temp_data)
    #         print(data)


def send_mail():
    with open(file="temp.json", mode="r") as mail_file:
        mail_data = json.load(fp=mail_file)
    mail_data = mail_data["mail"]
    senders_email = "Your email goes here"
    senders_password = "Your email app password goes here"
    recipients_mail = mail_data["email"]
    mail_subject = mail_data["title"]
    mail_body = mail_data["message"]

    message = EmailMessage()
    message["From"] = senders_email
    message["To"] = recipients_mail
    message["Subject"] = mail_subject
    message.set_content(mail_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=context) as mail:
        mail.login(user=senders_email, password=senders_password)
        mail.sendmail(from_addr=senders_email, to_addrs=recipients_mail, msg=message.as_string())
    os.remove("temp.json")
    # viewport.destroy()


def process_mail(r_mail_entry, title_entry, body_text):
    if "@" not in r_mail_entry.get() or ".com" not in r_mail_entry.get():
        messagebox.showwarning(title="Emmail", message="Incorrect Email address")
    else:
        save_info(r_mail_entry, title_entry, body_text)
        send_mail()
        r_mail_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        body_text.delete("1.0", tk.END)


viewport = tk.Tk()
viewport.title("Emmail")

canva = tk.Canvas(width=550, height=550)
logo = tk.PhotoImage(file="Emmail-faint-logo.png")
canva.create_image(275, 275, image=logo)
canva.grid(column=0, row=0)
continue_button = tk.Button(text="Continue", command=lambda: open_send_page(viewport, continue_button, canva))
continue_button.config(font=btnFont)
continue_button.grid(column=0, row=0)

viewport.mainloop()

# main()
