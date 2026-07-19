import os
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "saved_players.db"


class InitDbTests(unittest.TestCase):
    def setUp(self):
        os.chdir(ROOT)
        if DB_PATH.exists():
            DB_PATH.unlink()
        sys.modules.pop("main", None)

    def test_init_db_creates_inventory_and_artifacts_columns(self):
        import main

        main.init_db()

        conn = sqlite3.connect(DB_PATH)
        try:
            columns = {row[1] for row in conn.execute("PRAGMA table_info(players)")}
        finally:
            conn.close()

        self.assertIn("inventory", columns)
        self.assertIn("artifacts", columns)


if __name__ == "__main__":
    unittest.main()
