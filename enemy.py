#enemy.py
from item import MenuFritaten, BastonDeAghanim, ManoDeMidas, TartaShawarma, TrajeZeta, GranNispero, FiguraStandCrazyDiamond, SteamMachine, NintendoSwitch2, Trifuerza, Violin, SuperEscopeta, Cortana, TomoDeOnePiece, CartaDragonBlancoOjosAzules, CartaMagoOscuro, MenuRolloMixto
import random
from character import Character
from skills import OracionEspectral, EraTanFacil, IsakAplasta, YameteKudasai, ZokusheiShokan, VoyASerElReyDeLosPiratas, PorlaPaz, GiroFuego, CabelloCejil, LosMilYUnKebab
from ui import imprimir_texto, mostrar_titulo_gigante, C_HEROE, C_ENEMIGO, C_ARTIFACT, C_SISTEMA, C_SKILL, C_BOSS, C_ITEM, RESET


class Enemy(Character):
    def __init__(self, name, hp, hp_max, sp, sp_max, attack, defense, level, experience, gold=0, loot_item_chance=0, loot_items=None, loot_artifact_chance=0, loot_artifacts=None, is_boss=False):
        super().__init__(name, "Enemy", hp, hp_max, sp, sp_max, attack, defense, level=level, experience=experience)
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = experience
        self.gold = gold
        self.loot_item_chance = loot_item_chance
        self.loot_items = loot_items or []
        self.loot_artifact_chance = loot_artifact_chance
        self.loot_artifacts = loot_artifacts or []
        self.skills = []
        self.is_boss = is_boss
        self.introduction = None
        
    def get_status(self):
        return f"{C_HEROE}{self.name}{RESET} - HP: {C_ARTIFACT}{self.hp}{RESET}/{C_HEROE}{self.hp_max}{RESET}"
    
    def attack_player(self, player):
        damage = max(0, self.attack - player.defense)
        player.take_damage(damage)
        return f"{C_ENEMIGO}{self.name}{RESET} ataca a {C_HEROE}{player.name}{RESET} y causa {C_ARTIFACT}{damage}{RESET} de daño."
    
class Boss_1(Enemy):
    def __init__(self):
        super().__init__(name="Isak_90", hp=350, hp_max=350, sp=300, sp_max=300, attack=25, defense=10, level=3, experience=500, gold=300)
        self.is_boss = True
        self.loot_items = [MenuRolloMixto(), MenuFritaten()]
        self.loot_item_chance = 100
        self.loot_artifacts = [ManoDeMidas(), BastonDeAghanim()]
        self.loot_artifact_chance = 100
        self.skills = [OracionEspectral(), EraTanFacil(), IsakAplasta()]
        self.introduction = f"\n{C_BOSS}Isak_90{RESET}: {C_ENEMIGO}'¡Bienvenido a la mansion de casper! ¡Aqui se termina tu camino!'{RESET}"

class Boss_2(Enemy):
    def __init__(self):
        super().__init__(name="Capitan Alansito", hp=550, hp_max=550, sp=500, sp_max=500, attack=35, defense=25, level=5, experience=800, gold=500)
        self.is_boss = True
        self.loot_items = [MenuRolloMixto(), MenuFritaten()]
        self.loot_item_chance = 100
        self.loot_artifacts = [TartaShawarma(), TrajeZeta()]
        self.loot_artifact_chance = 100
        self.skills = [YameteKudasai(), ZokusheiShokan(), VoyASerElReyDeLosPiratas()]
        self.introduction = f"\n{C_BOSS}Capitán Alansito{RESET}: {C_ENEMIGO}'Tienes valor para enfrentar al capitan BlackDicku, ¡muestrame hasta donde llega tu voluntad!'{RESET}"

class FinalBoss(Enemy):
    def __init__(self):
        super().__init__(name="Pepeda", hp=1000, hp_max=1000, sp=700, sp_max=700, attack=50, defense=35, level=13, experience=2000, gold=1000)
        self.is_boss = True
        self.loot_items = [MenuRolloMixto(), MenuFritaten()]
        self.loot_item_chance = 100
        self.loot_artifacts = [GranNispero(), FiguraStandCrazyDiamond()]
        self.loot_artifact_chance = 100
        self.skills = [PorlaPaz(), GiroFuego(), CabelloCejil(), LosMilYUnKebab()]
        self.introduction = f"\n{C_BOSS}Pepeda, el sultan{RESET}: {C_ENEMIGO}'Conque tu eres quien que esta causando problemas en mis dominios, en el pasado eras como mi hermano, pero hoy no puedo dejarte continuar.¡Por la paz!'"
    