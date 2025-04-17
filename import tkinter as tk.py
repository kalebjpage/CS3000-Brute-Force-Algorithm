import tkinter as tk
import threading
import time
import itertools
import string

def brute_force_crack(password):
    """
    Brute‑force search over lowercase, uppercase, digits, and punctuation.
    """
    start_time = time.time()
    # Full character set
    chars = (
        string.ascii_lowercase +    # a–z
        string.ascii_uppercase +    # A–Z
        string.digits +             # 0–9
        string.punctuation          # special chars !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    )

    for length in itertools.count(1):
        for attempt_tuple in itertools.product(chars, repeat=length):
            attempt = ''.join(attempt_tuple)
            if attempt == password:
                elapsed = time.time() - start_time
                return attempt, elapsed

def crack_password():

    password = entry.get()
    if not password:
        result_label.config(text="Please enter a password.")
        return
    
    # Reset result and display loader message
    result_label.config(text="")
    loader_label.config(text="Cracking, please wait...")
    crack_button.config(state=tk.DISABLED)
    
    def run_crack():
        # Run the brute force algorithm
        cracked_password, elapsed = brute_force_crack(password)
        # Once done, update the UI on the main thread using 'after'
        def update_ui():
            loader_label.config(text="")
            result_label.config(text=f"Password: {cracked_password}\nTime Elapsed: {elapsed:.2f} seconds")
            crack_button.config(state=tk.NORMAL)
        root.after(0, update_ui)
    
    # Start the cracking process in a new thread
    threading.Thread(target=run_crack, daemon=True).start()

# Create the main Tkinter window
root = tk.Tk()
root.title("Brute Force Password Cracker")

# Create a label for the input
label = tk.Label(root, text="Enter Password:")
label.pack(padx=10, pady=10)

# Create an entry widget for user input
entry = tk.Entry(root)
entry.pack(padx=10, pady=5)

# Create a button that starts the cracking process
crack_button = tk.Button(root, text="Crack", command=crack_password)
crack_button.pack(padx=10, pady=5)

# Create a label to show a loader message while cracking is in progress
loader_label = tk.Label(root, text="")
loader_label.pack(padx=10, pady=5)

# Create a label to display the final result
result_label = tk.Label(root, text="")
result_label.pack(padx=10, pady=5)


root.mainloop()
