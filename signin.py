import subprocess
import os
import tkinter as tk
from ldap3 import Server, Connection, ALL
from Verify_signature import result

def check_user_and_password(user_uid, user_password):
    ldap_server = "ldap://192.168.17.142:389" 
    search_base = "dc=tekup,dc=tn" 
    search_filter = f"(uid={user_uid})"
    server = Server(ldap_server, use_ssl=True, get_info=ALL)
    
    try:
        with Connection(server, auto_bind=True) as conn:
            conn.search(search_base, search_filter, attributes='cn')
            if len(conn.entries) == 0:
                return False
            user_dn = conn.entries[0].entry_dn
            
            user_conn = Connection(server, user_dn, user_password, auto_bind=False)
            user_conn.bind()
            if user_conn.bound:
                return True
            else:
                return False
    except:
        print("erreur")
        return False

def login_clicked():
    root.withdraw() # To hide the default root window you can use
    username = username_entry.get()
    password = password_entry.get()

    if check_user_and_password(username, password) and result:
        env = os.environ.copy()
        env["RABBITMQ_USERNAME"] = username
        env["RABBITMQ_PASSWORD"] = password
        subprocess.run(["python", "chat.py"], env=env)
    else:
        login_status_label.config(text="Login failed", fg="#FF81AE")
    root.withdraw() # To hide the default root window you can use



# Create the main window
root = tk.Tk()
root.title("Sign In")
root.geometry("850x460")  # Set the initial size of the window

# Set the background color to white
root.configure(bg="plum2")

# Load the image (resize it if needed)
image_path = "signin.png"  # Change this to the path of your image
if os.path.exists(image_path):
    img = tk.PhotoImage(file=image_path)
    img = img.subsample(5)  # Resize the image by a factor of 4
    tk.Label(root, image=img, bg="plum2").grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="w")

# Define a custom font with a larger size
custom_font = ("Arial", 12)  # Change the font and size as needed
custom_font2= ("Helvetica",12,"bold")
# Username entry
tk.Label(root, text="Username:", font=custom_font, bg="plum2", fg="gray15").grid(row=1, column=1, padx=10, pady=10)
username_entry = tk.Entry(root, font=custom_font)
username_entry.grid(row=1, column=2, padx=10, pady=10)

# Password entry
tk.Label(root, text="Password:", font=custom_font, bg="plum2", fg="gray15").grid(row=2, column=1, padx=10, pady=10)
password_entry = tk.Entry(root, show="*", font=custom_font)
password_entry.grid(row=2, column=2, padx=10, pady=10)

# Login button
login_button = tk.Button(root, text="Login", command=login_clicked, font=custom_font2, bg="hot pink", fg="snow",height= 2, width=10)
login_button.grid(row=3, column=1, columnspan=2, pady=10)

# Login status label
login_status_label = tk.Label(root, text="", fg="#FF81AE", font=custom_font, bg="plum2")
login_status_label.grid(row=4, column=1, columnspan=2, pady=10)

# Run the GUI main loop
root.mainloop()
