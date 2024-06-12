import subprocess
import tkinter as tk
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
import os

# Function to check if the user already exists in LDAP
def user_exists(conn, username):
    search_filter = f'(uid={username})'
    search_base = 'ou=users,dc=tekup,dc=tn'
    conn.search(search_base, search_filter, attributes=['uid'])
    return len(conn.entries) > 0

def signup(first_name, last_name, username, password, cin, email):
    ldap_server = 'ldap://192.168.17.142:389'
    ldap_user = 'cn=admin,dc=tekup,dc=tn'
    ldap_password = 'root'

    server = Server(ldap_server, get_info=ALL)
    conn = Connection(server, ldap_user, ldap_password, auto_bind=True)

    if user_exists(conn, username):
        print(f"User {username} already exists.")
        conn.unbind()
        return

    id = hash(username) % 9999  # Better way to generate a unique ID

    new_user_dn = 'uid=' + username + ',ou=users,dc=tekup,dc=tn'
    new_user_attributes = {
        'objectClass': ['inetOrgPerson', 'posixAccount', 'top'],
        'cn': first_name + last_name,
        'sn': last_name,
        'givenName': first_name,
        'uid': username,
        "uidNumber": id,
        "gidNumber": id,
        'homeDirectory': '/home/' + username,
        'userPassword': password,
        'carlicense': cin,
        'mail': email
    }

    conn.add(new_user_dn, attributes=new_user_attributes)

    if conn.result['description'] == 'success':
        print("Registration successful")
    else:
        print("Registration failed")

    conn.unbind()

    # Check if the registration was successful
    if conn.result['description'] == 'success':
        # Get the path to the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Run signin.py using subprocess with the correct path
        subprocess.run(["python", os.path.join(script_directory, "signin.py")])

        # Close the current Tkinter window
        root.destroy()

def register_clicked():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    cin = cin_entry.get()
    email = email_entry.get()
    root.destroy()

    signup(first_name, last_name, username, password, cin, email)
    

# Create the main window
root = tk.Tk()
root.title("Sign Up")
root.geometry("1000x520")  # Set the initial size of the window

# Set the background color to white
root.configure(bg="plum2")

# Load the image (replace "path/to/signup.png" with the actual path)
image_path = "signup.png"
if os.path.exists(image_path):
    img = tk.PhotoImage(file=image_path)
    img = img.subsample(4)  # Resize the image by a factor of 4
    tk.Label(root, image=img, bg="plum2").grid(row=0, column=0, rowspan=8, padx=10, pady=10, sticky="w")

# Define a custom font with a larger size
custom_font = ("Arial", 12)  # Change the font and size as needed
custom_font2= ("Helvetica",12,"bold")
# Pink color code (#FF81AE)
pink_color = "gray15"

# First Name entry
tk.Label(root, text="First Name:", font=custom_font, bg="plum2", fg=pink_color).grid(row=1, column=1, padx=10, pady=10)
first_name_entry = tk.Entry(root, font=custom_font)
first_name_entry.grid(row=1, column=2, padx=10, pady=10)

# Last Name entry
tk.Label(root, text="Last Name:", font=custom_font, bg="plum2", fg=pink_color).grid(row=2, column=1, padx=10, pady=10)
last_name_entry = tk.Entry(root, font=custom_font)
last_name_entry.grid(row=2, column=2, padx=10, pady=10)

# Username entry
tk.Label(root, text="Username:", font=custom_font, bg="plum2", fg=pink_color).grid(row=3, column=1, padx=10, pady=10)
username_entry = tk.Entry(root, font=custom_font)
username_entry.grid(row=3, column=2, padx=10, pady=10)

# Password entry
tk.Label(root, text="Password:", font=custom_font, bg="plum2", fg=pink_color).grid(row=4, column=1, padx=10, pady=10)
password_entry = tk.Entry(root, show="*", font=custom_font)
password_entry.grid(row=4, column=2, padx=10, pady=10)

# CIN entry
tk.Label(root, text="CIN:", font=custom_font, bg="plum2", fg=pink_color).grid(row=5, column=1, padx=10, pady=10)
cin_entry = tk.Entry(root, font=custom_font)
cin_entry.grid(row=5, column=2, padx=10, pady=10)

# Email entry
tk.Label(root, text="Email:", font=custom_font, bg="plum2", fg=pink_color).grid(row=6, column=1, padx=10, pady=10)
email_entry = tk.Entry(root, font=custom_font)
email_entry.grid(row=6, column=2, padx=10, pady=10)

# Register button
register_button = tk.Button(root, text="Register", command=register_clicked, font=custom_font2, bg="hot pink", fg="snow",height= 2, width=10)
register_button.grid(row=7, column=1, columnspan=2, pady=10)

# Run the GUI main loop
root.mainloop()
