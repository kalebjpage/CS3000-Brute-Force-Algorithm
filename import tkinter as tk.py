import tkinter as tk
import threading
import time
from hashlib import sha256
import BFCracker

def crack_password(entry, result_label, loader_label, crack_button):
    password = entry.get().strip()
    if not password:
        result_label.config(text="Please enter a password.")
        return

    password_hash = sha256(password.encode("utf-8")).digest()
    result_label.config(text="")
    loader_label.config(text="Cracking, please wait...")
    crack_button.config(state=tk.DISABLED)

    def run_crack():
        start_time = time.time()
        cracked_password, guess_count = BFCracker.CrackHashMulti(
            password_hash,
            1,
            3,
            BFCracker.GenerateCharset(5),  # a-z + A-Z
            3
        )
        elapsed = time.time() - start_time

        def update_ui():
            if cracked_password is None:
                result_label.config(text=f"❌ Password not found.\nTime: {elapsed:.2f}s\nGuesses: {guess_count}")
            else:
                result_label.config(text=f"✅ Password: {cracked_password}\nTime: {elapsed:.2f}s\nGuesses: {guess_count}")
            loader_label.config(text="")
            crack_button.config(state=tk.NORMAL)

        root.after(0, update_ui)

    threading.Thread(target=run_crack, daemon=True).start()

def main():
    global root
    root = tk.Tk()
    root.title("Simple Brute Force Cracker")

    tk.Label(root, text="🔐 Enter Password:").pack(padx=10, pady=(10, 2))
    entry = tk.Entry(root)
    entry.pack(padx=10, pady=5)

    crack_button = tk.Button(
        root,
        text="🚀 Crack Password",
        command=lambda: crack_password(entry, result_label, loader_label, crack_button)
    )
    crack_button.pack(pady=10)

    loader_label = tk.Label(root, text="")
    loader_label.pack()

    result_label = tk.Label(root, text="", justify="center")
    result_label.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
