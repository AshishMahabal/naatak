from streamlit_authenticator.utilities.hasher import Hasher

# List of plain-text passwords to hash
passwords_to_hash = ['naatak_adman', 'naatak_man']  # Replace with your passwords

# Generate the password hashes
hashed_passwords = Hasher(passwords_to_hash).generate()

# Print the hashes
for i, password in enumerate(passwords_to_hash):
    print(f"Plain: {password} -> Hash: {hashed_passwords[i]}")

