import os
import mysql.connector

from app.schemas import DocumentCreate


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )

def check_db_connection():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            category VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    cursor.close()
    conn.close()

def get_documents():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM documents")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_document(id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, title, content, category, created_at
        FROM documents
        WHERE id = %s
        """,
        (id,)
    )
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row

def insert_document(document: DocumentCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
    """
    INSERT INTO documents (title, content, category)
    VALUES (%s, %s, %s)
    """,
    (document.title, document.content, document.category)
    )
    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return new_id