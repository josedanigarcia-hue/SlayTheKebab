#data.py

from ui import imprimir_texto, mostrar_titulo_gigante, C_HEROE, C_ENEMIGO, C_ARTIFACT, C_SISTEMA, C_SKILL, C_BOSS, C_ITEM, RESET
from item import ManoDeMidas
from item import CaretaDePepeda
from item import (
    AcreditacionMLP,
    EstrellaLevante,
    Fricandela,
    Guldendraak,
    GranNispero,
    MenuFritaten,
    MenuRolloMixto,
    Mexicano,
    Ocarina,
    PiedraBruja,
    RedDeVoley,
    DjinnDeAgua,
    DjinnDeFuego,
    DjinnDeTierra,
    DjinnDeViento,
    LlaveEspada,
    PaqueteDeTabaco,
    TartaShawarma,
    FiguraStandCrazyDiamond,
    CalcetinSucio,
    TrajeZeta,
    Clackers,
    TomoDeOnePiece,
    PorroDeLasTeorias
)


ENEMIES_GENERIC = [
    {"name": "Radnes, Haki Teorico", "hp": 100, "hp_max": 100, "sp": 100, "sp_max": 100, "attack": 30, "defense": 1, "level": 5, "experience": 500, "loot_item_chance": 0.5, "gold": 100, "loot_items": [MenuRolloMixto], "loot_artifact_chance": 0.3, "loot_artifacts": [PorroDeLasTeorias, CaretaDePepeda]},
    {"name": "Gordrim, El Exiliado", "hp": 200, "hp_max": 200, "sp": 50, "sp_max": 50, "attack": 40, "defense": 10, "level": 5, "experience": 1000, "loot_item_chance": 0.5, "gold": 250, "loot_items": [MenuFritaten], "loot_artifact_chance": 0.3, "loot_artifacts": [PaqueteDeTabaco, CalcetinSucio]},
    {"name": "Voralzuki, Disformidad Garrota", "hp": 300, "hp_max": 300, "sp": 200, "sp_max": 200, "attack": 60, "defense": 30, "level": 5, "experience": 2000, "loot_item_chance": 0.5, "gold": 500, "loot_items": [MenuRolloMixto, MenuFritaten], "loot_artifact_chance": 0.3, "loot_artifacts": [LlaveEspada, PiedraBruja]},
]

ENEMIES_CHAPTER_1 = [
    {"name": "Garrota", "hp": 30, "hp_max": 30, "sp": 20, "sp_max": 20, "attack": 16, "defense": 2, "level": 1, "experience": 50, "gold": 10, "loot_item_chance": 0.3, "loot_items": [Fricandela], "loot_artifact_chance": 0.1, "loot_artifacts": [PiedraBruja]},
    {"name": "Lanero", "hp": 50, "hp_max": 50, "sp": 30, "sp_max": 30, "attack": 18, "defense": 5, "level": 2, "experience": 60, "gold": 20, "loot_item_chance": 0.3, "loot_items": [Mexicano], "loot_artifact_chance": 0.1, "loot_artifacts": [AcreditacionMLP]},
    {"name": "Miembro de Mulas", "hp": 80, "hp_max": 80, "sp": 40, "sp_max": 40, "attack": 20, "defense": 7, "level": 3, "experience": 80, "gold": 30, "loot_item_chance": 0.3, "loot_items": [EstrellaLevante], "loot_artifact_chance": 0.1, "loot_artifacts": [RedDeVoley]},
    {"name": "Dotero", "hp": 40, "hp_max": 40, "sp": 50, "sp_max": 50, "attack": 17, "defense": 8, "level": 4, "experience": 100, "gold": 50, "loot_item_chance": 0.3, "loot_items": [Guldendraak], "loot_artifact_chance": 0.1, "loot_artifacts": [ManoDeMidas]},
]

ENEMIES_CHAPTER_2 = [
    {"name": "Buggy", "hp": 100, "hp_max": 100, "sp": 60, "sp_max": 60, "attack": 20, "defense": 15, "level": 4, "experience": 100, "gold": 70, "loot_item_chance": 0.3, "loot_items": [Guldendraak], "loot_artifact_chance": 0.1, "loot_artifacts": [TomoDeOnePiece]},
    {"name": "Hans", "hp": 120, "hp_max": 120, "sp": 70, "sp_max": 70, "attack": 25, "defense": 15, "level": 4, "experience": 120, "gold": 60, "loot_item_chance": 0.3, "loot_items": [EstrellaLevante], "loot_artifact_chance": 0.1, "loot_artifacts": [DjinnDeAgua, DjinnDeFuego, DjinnDeTierra, DjinnDeViento]},
    {"name": "Joseph Joestar", "hp": 140, "hp_max": 140, "sp": 80, "sp_max": 80, "attack": 32, "defense": 18, "level": 4, "experience": 170, "gold": 100, "loot_item_chance": 0.3, "loot_items": [Mexicano], "loot_artifact_chance": 0.1, "loot_artifacts": [Clackers]},
    {"name": "Izuku Midoriya", "hp": 120, "hp_max": 120, "sp": 80, "sp_max": 80, "attack": 29, "defense": 14, "level": 4, "experience": 140, "gold": 90, "loot_item_chance": 0.3, "loot_items": [Fricandela], "loot_artifact_chance": 0.1, "loot_artifacts": [TrajeZeta]},
]

ENEMIES_CHAPTER_3 = [
    {"name": "Hiroshi", "hp": 160, "hp_max": 160, "sp": 100, "sp_max": 100, "attack": 33, "defense": 20, "level": 4, "experience": 140, "gold": 140, "loot_item_chance": 0.3, "loot_items": [Mexicano], "loot_artifact_chance": 0.1, "loot_artifacts": [CalcetinSucio]},
    {"name": "Josuke Higashikata", "hp": 200, "hp_max": 200, "sp": 100, "sp_max": 100, "attack": 38, "defense": 24, "level": 4, "experience": 180, "gold": 100, "loot_item_chance": 0.3, "loot_items": [Guldendraak], "loot_artifact_chance": 0.1, "loot_artifacts": [FiguraStandCrazyDiamond]},
    {"name": "Mascota Rollo de Kebab", "hp": 240, "hp_max": 240, "sp": 80, "sp_max": 80, "attack": 40, "defense": 24, "level": 4, "experience": 220, "gold": 120, "loot_item_chance": 0.3, "loot_items": [MenuRolloMixto], "loot_artifact_chance": 0.1, "loot_artifacts": [TartaShawarma]},
    {"name": "Ojala_Pepeda", "hp": 340, "hp_max": 340, "sp": 80, "sp_max": 80, "attack": 44, "defense": 30, "level": 4, "experience": 250, "gold": 150, "loot_item_chance": 0.3, "loot_items": [MenuFritaten], "loot_artifact_chance": 0.1, "loot_artifacts": [CaretaDePepeda, GranNispero]},
]

ENEMIES_ELITE = [

]

