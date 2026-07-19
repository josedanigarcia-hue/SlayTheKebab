import unittest

from character import Matabufalez
from item import GranNispero


class ArtifactResurrectionTests(unittest.TestCase):
    def test_gran_nispero_revives_player_with_full_stats_on_death(self):
        player = Matabufalez()
        player.hp = 1
        player.sp = 5
        player.add_artifact(GranNispero())

        player.take_damage(999)

        self.assertTrue(player.is_alive())
        self.assertEqual(player.hp, player.hp_max)
        self.assertEqual(player.sp, player.sp_max)


if __name__ == "__main__":
    unittest.main()
