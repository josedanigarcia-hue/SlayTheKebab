#storage.py

import os
import pickle
import sqlite3
from character import Freakmaster, Matabufalez, Yuri, Sami

CLASSES = {
    "Matabufalez": Matabufalez,
    "Yuri": Yuri,
    "Freakmaster": Freakmaster,
    "Sami": Sami
}

DB_PATH = os.path.join(os.path.dirname(__file__), "saved_players.db")


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_schema():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            name TEXT PRIMARY KEY,
            char_class TEXT,
            hp INTEGER,
            hp_max INTEGER,
            sp INTEGER,
            sp_max INTEGER,
            attack INTEGER,
            defense INTEGER,
            level INTEGER,
            experience INTEGER,
            chapter INTEGER,
            current_node_id TEXT,
            inventory TEXT,
            artifacts TEXT
        )
        """
    )

    existing_columns = {
        row[1] for row in cursor.execute("PRAGMA table_info(players)")
    }
    required_columns = {
        "char_class": "TEXT",
        "hp": "INTEGER",
        "hp_max": "INTEGER",
        "sp": "INTEGER",
        "sp_max": "INTEGER",
        "attack": "INTEGER",
        "defense": "INTEGER",
        "level": "INTEGER",
        "experience": "INTEGER",
        "chapter": "INTEGER",
        "current_node_id": "TEXT",
        "inventory": "TEXT",
        "artifacts": "TEXT"
    }

    for column_name, column_type in required_columns.items():
        if column_name not in existing_columns:
            cursor.execute(f"ALTER TABLE players ADD COLUMN {column_name} {column_type}")

    conn.commit()
    conn.close()


def save_player(player):
    _init_schema()
    conn = _get_connection()
    cursor = conn.cursor()
    inventory_data = pickle.dumps(player.inventory)
    artifacts_data = pickle.dumps(player.artifacts)
    cursor.execute(
        """
        INSERT OR REPLACE INTO players (
            name, char_class, hp, hp_max, sp, sp_max, attack, defense, level, experience, chapter, current_node_id, inventory, artifacts
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            player.name,
            player.char_class,
            player.hp,
            player.hp_max,
            player.sp,
            player.sp_max,
            player.attack,
            player.defense,
            player.level,
            player.experience,
            player.chapter,
            player.current_node_id,
            inventory_data,
            artifacts_data
        ),
    )
    conn.commit()
    conn.close()


def has_saved_players():
    _init_schema()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM players")
    count = cursor.fetchone()["count"]
    conn.close()
    return count > 0


def load_player():
    _init_schema()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        clase = CLASSES[row["char_class"]]
        player = clase()
        player.hp = row["hp"]
        player.hp_max = row["hp_max"]
        player.sp = row["sp"]
        player.sp_max = row["sp_max"]
        player.attack = row["attack"]
        player.defense = row["defense"]
        player.level = row["level"]
        player.experience = row["experience"]
        player.chapter = row["chapter"]
        player.current_node_id = row["current_node_id"]
        if row["inventory"]:
            player.inventory = pickle.loads(row["inventory"])
        else:
            player.inventory = []
        if row["artifacts"]:
            player.artifacts = pickle.loads(row["artifacts"])
        else:
            player.artifacts = []
        return player
    return None


def delete_saved_game():
    _init_schema()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()