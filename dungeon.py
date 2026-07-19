#dungeon.py

from data import ENEMIES_CHAPTER_1
from data import ENEMIES_CHAPTER_2
from data import ENEMIES_CHAPTER_3
from data import ENEMIES_GENERIC
import random
from combat import combat
from enemy import Enemy, Boss_1, Boss_2, FinalBoss
from item import EstrellaLevante, Guldendraak, Fricandela, Mexicano, MenuRolloMixto, MenuFritaten, SteamMachine, NintendoSwitch2, Trifuerza, Violin, SuperEscopeta, Cortana, TomoDeOnePiece, CartaDragonBlancoOjosAzules, CartaMagoOscuro, get_all_items, get_all_artifacts
from character import Character
from ui import imprimir_texto, mostrar_titulo_gigante, C_HEROE, C_ENEMIGO, C_ARTIFACT, C_SISTEMA, C_SKILL, C_BOSS, C_ITEM, RESET
from colorama import init, Fore, Back, Style

def build_shop_entries(player, item_classes=None, artifact_classes=None):
    item_classes = item_classes or get_all_items()
    artifact_classes = artifact_classes or get_all_artifacts()

    shop_items = [cls() for cls in random.sample(item_classes, min(3, len(item_classes)))]

    owned_artifact_types = {type(a) for a in player.artifacts}
    available_artifact_classes = [
        c for c in artifact_classes if c not in owned_artifact_types and c not in {type(a) for a in player.artifacts}
    ]
    shop_artifacts = [cls() for cls in random.sample(available_artifact_classes, min(3, len(available_artifact_classes)))] if available_artifact_classes else []

    shop_entries = [("item", it) for it in shop_items] + [("artifact", art) for art in shop_artifacts]
    return shop_entries


def spawn_random_enemy(chapter):
    if chapter == 1:
        todos_los_enemigos = ENEMIES_GENERIC + ENEMIES_CHAPTER_1
        pesos = [15, 2.5, 2.5, 20, 20, 20, 20]
        enemy_data = random.choices(todos_los_enemigos, weights=pesos, k=1)[0]   
    elif chapter == 2:
        todos_los_enemigos = ENEMIES_GENERIC + ENEMIES_CHAPTER_2
        pesos = [2.5, 15, 2.5, 20, 20, 20, 20]
        enemy_data = random.choices(todos_los_enemigos, weights=pesos, k=1)[0] 
    else:
        todos_los_enemigos = ENEMIES_GENERIC + ENEMIES_CHAPTER_3
        pesos = [2.5, 2.5, 15, 20, 20, 20, 20]
        enemy_data = random.choices(todos_los_enemigos, weights=pesos, k=1)[0]    
    return Enemy(
        enemy_data["name"],
        enemy_data["hp"],
        enemy_data["hp_max"],
        enemy_data["sp"],
        enemy_data["sp_max"],
        enemy_data["attack"],
        enemy_data["defense"],
        enemy_data["level"],
        enemy_data["experience"],
        gold=enemy_data.get("gold", 0),
        loot_item_chance=enemy_data.get("loot_item_chance", 0),
        loot_items=enemy_data.get("loot_items", []),
        loot_artifact_chance=enemy_data.get("loot_artifact_chance", 0),
        loot_artifacts=enemy_data.get("loot_artifacts", []),
        is_boss=enemy_data.get("is_boss", False)
    )

def random_event_type():
    return random.choices(
        ["Enemigo", "Evento", "Cofre"],
        weights=[60, 30, 10],
        k=1
    )[0]

class Node:
    def __init__(self, event_type, node_id):
        self.event_type = event_type
        self.node_id = node_id
        self.children = []

    def add_child(self, node):
        self.children.append(node)

def build_dungeon():
    # Piso 1: Inicio
    start = Node("start", "n0")
    # Piso 2
    combat_1 = Node("Enemigo", "n1")
    combat_2 = Node("Enemigo", "n2")
    start.add_child(combat_1)
    start.add_child(combat_2)
    #Piso 3
    nodo_a = Node(random_event_type(), "n3")
    nodo_b = Node(random_event_type(), "n4")
    nodo_c = Node(random_event_type(), "n5")
    nodo_d = Node(random_event_type(), "n6")
    combat_1.add_child(nodo_a)
    combat_1.add_child(nodo_b)
    combat_2.add_child(nodo_c)
    combat_2.add_child(nodo_d)
    #Piso 4
    nodo_e = Node(random_event_type(), "n7")
    nodo_f = Node(random_event_type(), "n8")
    nodo_g = Node(random_event_type(), "n9")
    nodo_h = Node(random_event_type(), "n10")
    nodo_i = Node(random_event_type(), "n11")
    nodo_a.add_child(nodo_e)
    nodo_a.add_child(nodo_f)
    nodo_b.add_child(nodo_f)
    nodo_b.add_child(nodo_g)
    nodo_c.add_child(nodo_g)
    nodo_c.add_child(nodo_h)
    nodo_d.add_child(nodo_h)
    nodo_d.add_child(nodo_i)
    #Piso 5
    chest_1 = Node("Cofre", "n12")
    chest_2 = Node("Cofre", "n13")
    chest_3 = Node("Cofre", "n14")
    chest_4 = Node("Cofre", "n15")
    nodo_e.add_child(chest_1)
    nodo_f.add_child(chest_1)
    nodo_f.add_child(chest_2)
    nodo_g.add_child(chest_2)
    nodo_g.add_child(chest_3)
    nodo_h.add_child(chest_3)
    nodo_h.add_child(chest_4)
    nodo_i.add_child(chest_4)
    #Piso 6
    nodo_j = Node(random_event_type(), "n16")
    nodo_k = Node(random_event_type(), "n17")
    nodo_l = Node(random_event_type(), "n18")
    nodo_m = Node(random_event_type(), "n19")
    nodo_n = Node(random_event_type(), "n20")
    chest_1.add_child(nodo_j)
    chest_1.add_child(nodo_k)
    chest_2.add_child(nodo_k)
    chest_2.add_child(nodo_l)
    chest_3.add_child(nodo_l)
    chest_3.add_child(nodo_m)
    chest_4.add_child(nodo_m)
    chest_4.add_child(nodo_n)
    #Piso 7
    nodo_o = Node(random_event_type(), "n21")
    nodo_p = Node(random_event_type(), "n22")
    nodo_q = Node(random_event_type(), "n23")
    nodo_r = Node(random_event_type(), "n24")
    nodo_j.add_child(nodo_o)
    nodo_k.add_child(nodo_o)
    nodo_k.add_child(nodo_p)
    nodo_l.add_child(nodo_p)
    nodo_l.add_child(nodo_q)
    nodo_m.add_child(nodo_q)
    nodo_m.add_child(nodo_r)
    nodo_n.add_child(nodo_r)
    #Piso 8
    nodo_s = Node(random_event_type(), "n25")
    nodo_t = Node(random_event_type(), "n26")
    nodo_u = Node(random_event_type(), "n27")
    nodo_v = Node(random_event_type(), "n28")
    nodo_w = Node(random_event_type(), "n29")
    nodo_o.add_child(nodo_s)
    nodo_o.add_child(nodo_t)
    nodo_p.add_child(nodo_t)
    nodo_p.add_child(nodo_u)
    nodo_q.add_child(nodo_u)
    nodo_q.add_child(nodo_v)
    nodo_r.add_child(nodo_v)
    nodo_r.add_child(nodo_w)
    #Piso 9
    rest_1 = Node("Descanso", "n30")
    rest_2 = Node("Descanso", "n31")
    rest_3 = Node("Descanso", "n32")
    rest_4 = Node("Descanso", "n33")
    nodo_s.add_child(rest_1)
    nodo_t.add_child(rest_1)
    nodo_t.add_child(rest_2)
    nodo_u.add_child(rest_2)
    nodo_u.add_child(rest_3)
    nodo_v.add_child(rest_3)
    nodo_v.add_child(rest_4)
    nodo_w.add_child(rest_4)
    #Piso 10
    boss = Node("Jefe", "n34")
    rest_1.add_child(boss)
    rest_2.add_child(boss)
    rest_3.add_child(boss)
    rest_4.add_child(boss)
    return start

def run_node(player, node, chapter):
    if node.event_type == "Enemigo":
        enemy = spawn_random_enemy(chapter)
        combat(player, enemy)
    elif node.event_type == "Cofre":
        # Seleccionar un artefacto entre los disponibles que el jugador no tenga
        possible = get_all_artifacts()
        available = [c for c in possible if not any(isinstance(a, c) for a in player.artifacts)]
        if not available:
            imprimir_texto(f"{C_HEROE}{player.name}{RESET} encuentra un cofre vacío (ya posees todos los artefactos disponibles).")
        else:
            artifact_class = random.choice(available)
            artifact = artifact_class()
            imprimir_texto(player.add_artifact(artifact))
    elif node.event_type == "Evento":
        event_outcome = random.random()
        if event_outcome < 0.80:  # 80% chance of positive outcome
            event = random.choice(["Tienda", "Item", "Artefacto"])
            if event == "Tienda":
                open_shop(player)
            elif event == "Item":
                item_class = random.choice([EstrellaLevante, Guldendraak, Fricandela, Mexicano, MenuRolloMixto, MenuFritaten])
                item = item_class()
                player.add_item(item)
                imprimir_texto(f"{C_HEROE}{player.name}{RESET} ha encontrado un bar abandonado y descubre {C_ITEM}{item.name}{RESET} en una mochila de Glovo tirada.")
            elif event == "Artefacto":
                possible = get_all_artifacts()
                available = [c for c in possible if not any(isinstance(a, c) for a in player.artifacts)]
                if not available:
                    imprimir_texto(f"{C_HEROE}{player.name}{RESET} encuentras al legendario Siko que sonriendo te ofrece un artefacto, pero ya posees todos los que ofrece.")
                else:
                    artifact_class = random.choice(available)
                    artifact = artifact_class()
                    imprimir_texto(f"{C_HEROE}{player.name}{RESET} encuentras al legendario Siko que sonriendo te ofrece: {C_ARTIFACT}{artifact.name}{RESET}")
                    imprimir_texto(player.add_artifact(artifact))
        else:  # 20% chance of negative outcome
            event = random.choice(["Trampa", "Enemigo"])
            if event == "Trampa":
                damage = random.randint(10, 30)
                player.take_damage(damage)
                imprimir_texto(f"{C_HEROE}{player.name}{RESET} ha caído en una trampa y recibe {C_ENEMIGO}{damage}{RESET} de daño.")
            elif event == "Enemigo":
                enemy = spawn_random_enemy(chapter)
                combat(player, enemy)
    elif node.event_type == "Jefe":
        if chapter == 1:
            boss = Boss_1()
        elif chapter == 2:
            boss = Boss_2()
        else:
            boss = FinalBoss()
        if getattr(boss, "introduction", None):
            imprimir_texto(boss.introduction)
        combat(player, boss)
    elif node.event_type == "Descanso":
        heal_amount = player.hp_max
        player.heal(heal_amount)
        sp_amount = int(player.sp_max * 1)
        player.sp = min(player.sp + sp_amount, player.sp_max)
        imprimir_texto(f"{C_HEROE}{player.name}{RESET} se recuesta en un campamento abandonado y recupera todos sus hp y sp")

def open_shop(player):
    """Abre una tienda con 3 items y 3 artefactos disponibles para comprar"""
    print(f"\n{'='*60}")
    imprimir_texto(f"¡Bienvenido a la tienda de {C_BOSS}Valeria{RESET}!")
    imprimir_texto(f"Tu oro actual: {C_ITEM}{player.gold}{RESET}")
    print(f"{'='*60}\n")

    # 1. MOVER FUERA DEL BUCLE: Generamos la oferta de la tienda UNA SOLA VEZ
    shop_entries = build_shop_entries(player)

    while True:
        if not shop_entries:
            imprimir_texto("No hay artículos disponibles en la tienda en este momento.")
            return

        imprimir_texto("ARTÍCULOS DISPONIBLES:")
        for idx, (kind, obj) in enumerate(shop_entries, 1):
            print(f"  {C_ARTIFACT}{idx}. {obj.name}{RESET} - {C_ITEM}{obj.price} oro{RESET} ({kind})")

        print(f"\n  0. Salir de la tienda")
        print(f"{'='*60}\n")

        try:
            choice = input("¿Qué deseas comprar? (elige número o 0 para salir): ").strip()
            choice = int(choice)

            if choice == 0:
                imprimir_texto(f"\n{C_HEROE}{player.name}{RESET} se va de la tienda.")
                break

            index = choice - 1
            if 0 <= index < len(shop_entries):
                kind, obj = shop_entries[index]
                price = getattr(obj, 'price', 0)
                
                if player.gold >= price:
                    if kind == "item":
                        # COMPRA DE ITEM: Infinito, no lo quitamos de la lista
                        player.gold -= price
                        player.add_item(obj)
                        imprimir_texto(f"\n{C_HEROE}{player.name}{RESET} compra {C_ITEM}{obj.name}{RESET} por {C_ITEM}{price} oro{RESET}. Oro restante: {C_ITEM}{player.gold}{RESET}\n")
                    else:
                        # COMPRA DE ARTEFACTO
                        player.gold -= price
                        added_message = player.add_artifact(obj)
                        imprimir_texto(added_message)
                        
                        # Comprobamos si realmente se lo equipó (por si ya lo tenía)
                        if not any(isinstance(a, type(obj)) for a in player.artifacts):
                            player.gold += price
                            imprimir_texto(f"\n✗ No se pudo añadir el artefacto {C_ARTIFACT}{obj.name}{RESET}. Se devuelve el oro.\n")
                        else:
                            imprimir_texto(f"\n{C_HEROE}{player.name}{RESET} compra {C_ARTIFACT}{obj.name}{RESET} por {C_ITEM}{price} oro{RESET}. Oro restante: {C_ITEM}{player.gold}{RESET}\n")
                            # 2. ELIMINAR ARTEFACTO: Lo sacamos de la lista para que no vuelva a salir
                            shop_entries.pop(index)
                else:
                    imprimir_texto(f"\n✗ No tienes suficiente oro. Necesitas {C_ITEM}{price}{RESET} y tienes {C_ITEM}{player.gold}{RESET}\n")
            else:
                imprimir_texto(f"\n✗ Opción inválida. Por favor, elige un número entre 0 y {len(shop_entries)}.\n")
        except ValueError:
            imprimir_texto(f"\n✗ Entrada inválida. Por favor, ingresa un número.\n")

def find_node(root, node_id):
    if root.node_id == node_id:
        return root
    for child in root.children:
        found = find_node(child, node_id)
        if found:
            return found
    return None