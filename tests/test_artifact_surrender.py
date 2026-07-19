import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from character import Character
from item import CaretaDePepeda


class DummyEnemy:
    def __init__(self):
        self.name = 'Goblin'
        self.hp = 20
        self.hp_max = 20
        self.sp = 0
        self.sp_max = 0
        self.attack = 1
        self.defense = 0
        self.lost_turn = False
        self.is_boss = False

    def is_alive(self):
        return self.hp > 0


class DummyPlayer(Character):
    def __init__(self):
        super().__init__(name='Jugador', char_class='Test', hp=100, hp_max=100, sp=50, sp_max=50, attack=10, defense=5, level=1, experience=0)
        self.artifacts = []
        self.inventory = []
        self.items = []
        self.skills = []


class ArtifactSurrenderTests(unittest.TestCase):
    @patch('random.random', return_value=0.0)
    def test_careta_de_pepeda_can_surrender_enemy_and_give_reward(self, mock_random):
        player = DummyPlayer()
        enemy = DummyEnemy()
        artifact = CaretaDePepeda()
        player.artifacts.append(artifact)

        result = artifact.on_combat_start(player, enemy)

        self.assertEqual(enemy.hp, 0)
        self.assertIsNotNone(result)
        self.assertTrue(len(player.inventory) == 1 or len(player.artifacts) == 1)


if __name__ == "__main__":
    unittest.main()
