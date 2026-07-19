from inventory_utils import summarize_inventory


class DummyItem:
    def __init__(self, name):
        self.name = name


def test_summarize_inventory_groups_repeated_items():
    items = [DummyItem("Poción"), DummyItem("Poción"), DummyItem("Espada")]

    result = summarize_inventory(items)

    assert result == [("Poción", 2), ("Espada", 1)]
