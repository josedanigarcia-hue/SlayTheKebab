import unittest

from character import Matabufalez
from combat import get_experience_gain
from item import AlbumChopeaPepeda


class ArtifactExperienceMultiplierTests(unittest.TestCase):
    def test_album_chopea_pepeda_doubles_experience_gain(self):
        player = Matabufalez()
        artifact = AlbumChopeaPepeda()
        artifact.apply_passive(player, None)

        self.assertEqual(get_experience_gain(player, 100), 200)


if __name__ == "__main__":
    unittest.main()
