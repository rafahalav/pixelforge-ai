import sqlite3

from datetime import datetime, timezone

from config.settings import DATABASE_PATH


class Database:

    def __init__(self):
        self.initialize()

    def connect(self):
        return sqlite3.connect(DATABASE_PATH)

    def initialize(self):

        with self.connect() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS generations (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    image_id TEXT NOT NULL UNIQUE,

                    prompt TEXT NOT NULL,

                    model TEXT NOT NULL,

                    size TEXT NOT NULL,

                    quality TEXT NOT NULL,

                    output_format TEXT NOT NULL,

                    image_path TEXT NOT NULL,

                    created_at TEXT NOT NULL,

                    steps INTEGER NOT NULL DEFAULT 4

                )
            """)

            columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(generations)"
                ).fetchall()
            }

            if "steps" not in columns:

                connection.execute("""
                    ALTER TABLE generations
                    ADD COLUMN steps INTEGER NOT NULL DEFAULT 4
                """)

            connection.commit()

    def add_generation(
        self,
        image_id,
        prompt,
        model,
        steps,
        output_format,
        image_path,
        size="1024x1024",
        quality="N/A"
    ):

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        with self.connect() as connection:

            connection.execute("""
                INSERT INTO generations (
                    image_id,
                    prompt,
                    model,
                    size,
                    quality,
                    output_format,
                    image_path,
                    created_at,
                    steps
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                image_id,
                prompt,
                model,
                size,
                str(quality),
                output_format,
                str(image_path),
                created_at,
                steps
            ))

            connection.commit()

    def get_history(self, limit=50):

        with self.connect() as connection:

            connection.row_factory = sqlite3.Row

            rows = connection.execute("""
                SELECT *
                FROM generations
                ORDER BY id DESC
                LIMIT ?
            """, (limit,)).fetchall()

            return [dict(row) for row in rows]

    def delete_generation(self, image_id):

        with self.connect() as connection:

            connection.execute("""
                DELETE FROM generations
                WHERE image_id = ?
            """, (image_id,))

            connection.commit()
