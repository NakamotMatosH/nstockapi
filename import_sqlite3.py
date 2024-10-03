import sqlite3

# 데이터베이스 연결 (없으면 새로 생성)
conn = sqlite3.connect('example.db')

# 커서 생성
cursor = conn.cursor()

# users 테이블 생성 (없으면 새로 생성)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')

# 데이터 삽입 예시
cursor.execute("INSERT INTO users (name, age) VALUES ('John Doe', 30)")
cursor.execute("INSERT INTO users (name, age) VALUES ('Jane Smith', 25)")
conn.commit()  # 변경 사항 저장

# 데이터 조회
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# 조회한 데이터 출력
print("Users in the database:")
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

# 데이터 업데이트 예시
cursor.execute("UPDATE users SET age = 31 WHERE name = 'John Doe'")
conn.commit()

# 업데이트된 데이터 조회
cursor.execute("SELECT * FROM users WHERE name = 'John Doe'")
updated_user = cursor.fetchone()
print(f"\nUpdated User: ID: {updated_user[0]}, Name: {updated_user[1]}, Age: {updated_user[2]}")

# 데이터 삭제 예시
cursor.execute("DELETE FROM users WHERE name = 'Jane Smith'")
conn.commit()

# 삭제 후 데이터 조회
cursor.execute("SELECT * FROM users")
rows_after_delete = cursor.fetchall()

print("\nUsers after deletion:")
for row in rows_after_delete:
    print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

# 커서 및 데이터베이스 연결 종료
cursor.close()
conn.close()
