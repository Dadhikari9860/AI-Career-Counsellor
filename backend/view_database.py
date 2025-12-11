"""
Script to view SQLite database contents
Run: python view_database.py
"""
import sqlite3
import os

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'career_guidance.db')

if not os.path.exists(db_path):
    print(f"Database not found at: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
print("=" * 50)
print("TABLES IN DATABASE")
print("=" * 50)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  - {table} ({count} rows)")

# View Users
print("\n" + "=" * 50)
print("USERS TABLE")
print("=" * 50)
cursor.execute("SELECT id, username, email, full_name, created_at FROM users")
users = cursor.fetchall()
if users:
    for user in users:
        print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Name: {user[3]}, Created: {user[4]}")
else:
    print("  No users found.")

# View Career Roles
print("\n" + "=" * 50)
print("CAREER ROLES TABLE")
print("=" * 50)
cursor.execute("SELECT id, title, category FROM career_roles LIMIT 10")
roles = cursor.fetchall()
if roles:
    for role in roles:
        print(f"  ID: {role[0]}, Title: {role[1]}, Category: {role[2]}")
else:
    print("  No career roles found.")

conn.close()
print("\n" + "=" * 50)
print("Done!")

