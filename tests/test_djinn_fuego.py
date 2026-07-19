import unittest
from character import Character
from item import DjinnDeFuego
from skills import Meteoro

class DummyPlayer(Character):
    def __init__(self):
        super().__init__(name='Jugador', char_class='Test', hp=100, hp_max=100, sp=50, sp_max=50, attack=10, defense=0, level=1, experience=0)
        self.skills = []
        self.artifacts = []
        self.inventory = []

class DjinnDeFuegoTests(unittest.TestCase):
    def test_djinn_de_fuego_gives_stat_and_skill(self):
        player = DummyPlayer()
        djinn = DjinnDeFuego()
        
        # Test adding artifact
        player.add_artifact(djinn)
        
        # Verify stat increase
        self.assertEqual(player.attack, 20)
        
        # Verify skill added
        self.assertEqual(len(player.skills), 1)
        self.assertIsInstance(player.skills[0], Meteoro)
        
        # Verify skill execution works
        enemy = DummyPlayer()
        skill = player.skills[0]
        self.assertEqual(skill.name, "ZokusheiShokan: Meteoro")
        
        # Execute skill effect
        message = skill.effect(player, enemy)
        self.assertIn("Meteoro", message)
        self.assertLess(enemy.hp, enemy.hp_max)

if __name__ == '__main__':
    unittest.main()
