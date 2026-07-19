import unittest

from dungeon import build_shop_entries


class DummyPlayer:
    def __init__(self):
        self.name = "Test"
        self.gold = 100
        self.inventory = []
        self.artifacts = []


class DummyItem:
    def __init__(self):
        self.name = "Item de prueba"
        self.price = 10


class DummyArtifact:
    def __init__(self):
        self.name = "Artefacto de prueba"
        self.price = 20


class ShopEntriesTests(unittest.TestCase):
    def test_purchased_artifact_disappears_from_shop_without_replacement(self):
        player = DummyPlayer()
        entries = build_shop_entries(
            player,
            item_classes=[DummyItem],
            artifact_classes=[DummyArtifact],
        )

        self.assertTrue(any(kind == "artifact" and obj.name == "Artefacto de prueba" for kind, obj in entries))

        player.artifacts.append(DummyArtifact())
        entries_after_purchase = build_shop_entries(
            player,
            item_classes=[DummyItem],
            artifact_classes=[DummyArtifact],
        )

        self.assertFalse(any(kind == "artifact" and obj.name == "Artefacto de prueba" for kind, obj in entries_after_purchase))

    def test_all_actual_artifacts_can_be_instantiated(self):
        from item import get_all_artifacts
        for cls in get_all_artifacts():
            try:
                instance = cls()
                self.assertIsNotNone(instance.name)
                self.assertIsNotNone(instance.description)
            except Exception as e:
                self.fail(f"Failed to instantiate {cls.__name__}: {e}")


if __name__ == "__main__":
    unittest.main()
