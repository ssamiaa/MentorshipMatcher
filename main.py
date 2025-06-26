from database import init_db
import sqlite3

print("\nWelcome to the Mentorship Matching Platform!")
print("This tool helps connect people who want to learn with those who can teach.")
print("You can sign up and add skills you want to teach or learn.\n")

def add_user():
    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()

    if not name or not email:
        print("Name and email cannot be empty.")
        return

    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        user_id = c.lastrowid
        conn.commit()
        print(f"User added successfully! Your user ID is: {user_id}")
    except sqlite3.IntegrityError:
        print("A user with this email already exists.")
    finally:
        conn.close()

def add_skills(user_id, skill_type):
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    while True:
        skill = input(f"Enter skill to {'teach' if skill_type == 'has' else 'learn'} (or 'done'): ").lower().strip()
        if skill == 'done':
            break
        if not skill:
            print("Skill cannot be empty.")
            continue
        c.execute("INSERT INTO skills (user_id, skill, type) VALUES (?, ?, ?)", (user_id, skill, skill_type))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email FROM users")
    users = c.fetchall()
    for user in users:
        print(f"ID: {user[0]} | Name: {user[1]} | Email: {user[2]}")
    conn.close()

# Initialize DB and main menu
if __name__ == "__main__":
    init_db()

    while True:
        print("\nWhat would you like to do?")
        print("1. Sign up (Add user)")
        print("2. View all users")
        print("3. Add skills")
        print("4. Run matchmaker")
        print("5. View matches")
        print("6. Exit")

        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                add_user()
            elif choice == "2":
                get_users()
            elif choice == "3":
                user_id = int(input("Enter your user ID: "))
                skill_type = input("Type ('has' to teach or 'wants' to learn): ").lower()
                if skill_type not in ['has', 'wants']:
                    print("Invalid skill type.")
                else:
                    add_skills(user_id, skill_type)
            elif choice == "4":
                from matcher import match_users_by_skills
                match_users_by_skills()
            elif choice == "5":
                from matcher import view_matches
                view_matches()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except sqlite3.OperationalError as e:
            print("Database error:", e)
        except ValueError:
            print("Please enter valid numbers where needed.")
        except Exception as e:
            print("Something went wrong:", e)
