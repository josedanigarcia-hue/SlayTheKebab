import unittest

from character import Matabufalez


class ArtifactDamageAvoidanceTests(unittest.TestCase):
    def test_avoid_damage_prevents_one_damage_instance(self):
        player = Matabufalez()
        player.avoid_damage = True

        message = player.take_damage(20)

        self.assertEqual(player.hp, player.hp_max)
        self.assertFalse(player.avoid_damage)
        self.assertIsNotNone(message)
        self.assertIn("evita", message.lower())

    def test_runas_de_freakmaster_trigger(self):
        from item import RunasDeFreakmaster
        from unittest.mock import patch
        
        player = Matabufalez()
        artifact = RunasDeFreakmaster()
        
        with patch('random.random', return_value=0.1):
            message = artifact.apply_passive(player, None)
            
        self.assertTrue(player.avoid_damage)
        self.assertIsNotNone(message)
        self.assertIn("brillan", message.lower())


if __name__ == "__main__":
    unittest.main()
