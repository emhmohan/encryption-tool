import os
from tkinter import Tk, Label, Button, filedialog, Entry, StringVar, messagebox
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def encrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = filename + ".enc"
    file_size = str(os.path.getsize(filename)).zfill(16)
    iv = Random.new().read(16)

    encryptor = AES.new(get_key(key), AES.MODE_CBC, iv)

    with open(filename, 'rb') as infile:
        with open(output_file, 'wb') as outfile:
            outfile.write(file_size.encode('utf-8'))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = filename[:-4]

    with open(filename, 'rb') as infile:
        orig_size = int(infile.read(16))
        iv = infile.read(16)

        decryptor = AES.new(get_key(key), AES.MODE_CBC, iv)

        with open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(orig_size)

def select_file_encrypt():
    file = filedialog.askopenfilename()
    if file:
        encrypt(password.get(), file)
        messagebox.showinfo("Success", "File encrypted successfully.")

def select_file_decrypt():
    file = filedialog.askopenfilename()
    if file:
        decrypt(password.get(), file)
        messagebox.showinfo("Success", "File decrypted successfully.")

# GUI
app = Tk()
app.title("AES-256 File Encryption Tool")
app.geometry("400x200")

Label(app, text="Enter Password:", font=("Arial", 12)).pack(pady=10)

password = StringVar()
Entry(app, textvariable=password, show='*', width=30).pack()

Button(app, text="Encrypt File", command=select_file_encrypt, bg="#2ecc71", fg="white").pack(pady=10)
Button(app, text="Decrypt File", command=select_file_decrypt, bg="#e74c3c", fg="white").pack()

app.mainloop()
