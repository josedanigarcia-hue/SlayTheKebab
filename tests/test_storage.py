import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from character import Matabufalez
from item import Fricandela, AcreditacionMLP
from storage import delete_saved_game, load_player, save_player


def setup_function():
    if os.path.exists("saved_players.db"):
        os.remove("saved_players.db")


def teardown_function():
    if os.path.exists("saved_players.db"):
        os.remove("saved_players.db")


def test_save_and_load_player_round_trip():
    player = Matabufalez()
    player.hp = 77
    player.sp = 33
    player.attack = 15
    player.defense = 7
    player.level = 2
    player.experience = 120
    player.chapter = 2
    player.current_node_id = "n5"

    save_player(player)
    loaded_player = load_player()

    assert loaded_player is not None
    assert loaded_player.name == player.name
    assert loaded_player.char_class == player.char_class
    assert loaded_player.hp == 77
    assert loaded_player.sp == 33
    assert loaded_player.attack == 15
    assert loaded_player.defense == 7
    assert loaded_player.level == 2
    assert loaded_player.experience == 120
    assert loaded_player.chapter == 2
    assert loaded_player.current_node_id == "n5"

    delete_saved_game()
    assert load_player() is None


def test_save_and_load_restores_inventory_and_artifacts_without_reapplying_effects():
    player = Matabufalez()
    player.inventory = [Fricandela(), Fricandela()]
    player.add_artifact(AcreditacionMLP())

    attack_before_save = player.attack
    defense_before_save = player.defense

    save_player(player)
    loaded_player = load_player()

    assert loaded_player is not None
    assert len(loaded_player.inventory) == 2
    assert all(isinstance(item, Fricandela) for item in loaded_player.inventory)
    assert len(loaded_player.artifacts) == 1
    assert isinstance(loaded_player.artifacts[0], AcreditacionMLP)
    assert loaded_player.attack == attack_before_save
    assert loaded_player.defense == defense_before_save
