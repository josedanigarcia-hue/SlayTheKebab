import unittest
from unittest.mock import patch

from character import Character
from combat import combat
from item import PistolonDeMatabufalez


class DummyPlayer(Character):
    def __init__(self):
        super().__init__(name='Jugador', char_class='Test', hp=100, hp_max=100, sp=50, sp_max=50, attack=10, defense=0, level=1, experience=0)
        self.skills = []
        self.artifacts = []
        self.inventory = []


class DummyEnemy(Character):
    def __init__(self):
        super().__init__(name='Enemigo', char_class='Enemy', hp=20, hp_max=20, sp=0, sp_max=0, attack=0, defense=0, level=1, experience=0)
        self.skills = []
        self.loot_items = []
        self.loot_artifacts = []
        self.gold = 0


class ArtifactPistolonTests(unittest.TestCase):
    def test_attack_can_trigger_artifact_shot(self):
        player = DummyPlayer()
        enemy = DummyEnemy()
        player.artifacts.append(PistolonDeMatabufalez())

        with patch('builtins.input', side_effect=['1']):
            with patch('item.random.random', return_value=0.0):
                combat(player, enemy)

        self.assertLess(enemy.hp, 1)


if __name__ == '__main__':
    unittest.main()
