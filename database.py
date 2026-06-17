import sqlite3


def connect_db():

    conn = sqlite3.connect("tasks.db")

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS tasks(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT,

            priority TEXT,

            due_date TEXT,

            completed TEXT

        )

    """)

    conn.commit()

    return conn, cursor


def insert_task(title, priority, due_date):

    conn, cursor = connect_db()

    cursor.execute(

        """

        INSERT INTO tasks

        (title, priority, due_date, completed)

        VALUES (?, ?, ?, ?)

        """,

        (title, priority, due_date, "Pending")

    )

    conn.commit()

    conn.close()


def get_tasks():

    conn, cursor = connect_db()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def delete_task(task_id):

    conn, cursor = connect_db()

    cursor.execute(

        "DELETE FROM tasks WHERE id=?",

        (task_id,)

    )

    conn.commit()

    conn.close()


def complete_task(task_id):

    conn, cursor = connect_db()

    cursor.execute(

        """

        UPDATE tasks

        SET completed='Completed'

        WHERE id=?

        """,

        (task_id,)

    )

    conn.commit()

    conn.close()


def update_task(task_id, title, priority, due_date):

    conn, cursor = connect_db()

    cursor.execute(

        """

        UPDATE tasks

        SET title=?,

            priority=?,

            due_date=?

        WHERE id=?

        """,

        (title, priority, due_date, task_id)

    )

    conn.commit()

    conn.close()


def search_tasks(keyword):

    conn, cursor = connect_db()

    cursor.execute(

        """

        SELECT * FROM tasks

        WHERE title LIKE ?

        """,

        ('%' + keyword + '%',)

    )

    results = cursor.fetchall()

    conn.close()

    return results