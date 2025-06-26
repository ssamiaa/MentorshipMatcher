import sqlite3

def get_users_by_role(role):
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM users WHERE role = ?", (role,))
    users = c.fetchall()
    conn.close()
    return users  # List of (id, name)
