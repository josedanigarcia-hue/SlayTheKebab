import unittest
from unittest.mock import patch

from character import Character
from combat import combat


class DummyPlayer(Character):
    def __init__(self):
        super().__init__(name='Jugador', char_class='Test', hp=100, hp_max=100, sp=50, sp_max=50, attack=10, defense=5, level=1, experience=0)
        self.skills = []
        self.artifacts = []
        self.inventory = []
        self.is_alive_calls = 0

    def is_alive(self):
        self.is_alive_calls += 1
        return self.is_alive_calls <= 1


class DummyEnemy(Character):
    def __init__(self):
        super().__init__(name='Enemigo', char_class='Enemy', hp=100, hp_max=100, sp=0, sp_max=0, attack=0, defense=0, level=1, experience=0)
        self.skills = []
        self.loot_items = []
        self.loot_artifacts = []
        self.gold = 0


class CombatTurnSkipTests(unittest.TestCase):
    def test_combat_skips_player_turn_when_lost_turn_flag_is_set(self):
        player = DummyPlayer()
        enemy = DummyEnemy()
        player.lost_turn = True

        with patch('builtins.input', side_effect=AssertionError('input should not be called')):
            combat(player, enemy)


if __name__ == '__main__':
    unittest.main()
