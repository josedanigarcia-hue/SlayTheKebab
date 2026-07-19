#combat.py

from character import Character
from enemy import Enemy
from data import ENEMIES_CHAPTER_1, ENEMIES_CHAPTER_2, ENEMIES_CHAPTER_3, ENEMIES_GENERIC
import random
from inventory_utils import summarize_inventory, get_item_by_display_index
from ui import imprimir_texto, mostrar_titulo_gigante, C_HEROE, C_ENEMIGO, C_ARTIFACT, C_SISTEMA, C_SKILL, C_BOSS, C_ITEM, RESET
from colorama import init, Fore, Back, Style

def get_experience_gain(player, base_experience):
    multiplier = getattr(player, "experience_multiplier", 1) or 1
    return int(base_experience * multiplier)

def get_gold_gain(player, base_gold):
    multiplier = getattr(player, "gold_multiplier", 1) or 1
    return int(base_gold * multiplier)

def combat(player, enemy):
    imprimir_texto(f"¡Un {C_ENEMIGO}{enemy.name}{RESET} aparece!")
    turn = 0
    original_attack = player.attack
    original_defense = player.defense
    original_hp_max = player.hp_max
    original_sp_max = player.sp_max
    enemy_original_defense = enemy.defense
    for skill in player.skills:
        skill.passive_triggered = False

    for artifact in player.artifacts:
        if not enemy.is_alive():
            break
        if artifact.active_once:
            continue
        if getattr(artifact, "trigger_mode", "passive") == "combat_start":
            if hasattr(artifact, "triggered"):
                artifact.triggered = False
            message = artifact.on_combat_start(player, enemy)
            if message:
                imprimir_texto(message)

    while player.is_alive() and enemy.is_alive():
        turn += 1
        enemy.defense = enemy_original_defense
        for artifact in player.artifacts:
            if artifact.active_once:
                continue
            if getattr(artifact, "trigger_mode", "passive") == "turn_start":
                if hasattr(artifact, "apply_passive"): 
                    message = artifact.apply_passive(player, enemy)
                    if message:
                        imprimir_texto(message)
        imprimir_texto(f"\nTurno {turn}")
        imprimir_texto(player.get_status())
        imprimir_texto(enemy.get_status())
        fled = False
        for artifact in player.artifacts:
            if artifact.active_once:
                continue
            if getattr(artifact, "trigger_mode", "passive") != "passive":
                continue
            message = artifact.apply_passive(player, enemy)
            if message:
                imprimir_texto(message)
        for skill in player.skills:
            if not skill.is_passive:
                continue
            if skill.passive_once and skill.passive_triggered:
                continue
            message = skill.passive_effect(player, enemy)
            if message:
                imprimir_texto(message)
            skill.passive_triggered = True

        if player.lose_turn:
            imprimir_texto(f"{C_HEROE}{player.name} no puede actuar.{RESET}")
            player.lose_turn = False
        else:
            while True:
                action = input(
                    "¿Qué quieres hacer?\n"
                    "1. Atacar\n"
                    "2. Usar una habilidad\n"
                    "3. Usar objeto\n"
                    "4. Huir\n"
                    "Elige: "
                )
                if action == "1":
                    damage = max(0, player.attack - enemy.defense)
                    enemy.take_damage(damage)
                    imprimir_texto(f"{C_HEROE}{player.name}{RESET} ataca a {C_ENEMIGO}{enemy.name}{RESET} y causa {C_ENEMIGO}{damage}{RESET} de daño.")

                    for artifact in player.artifacts:
                        if artifact.active_once:
                            continue
                        if getattr(artifact, "trigger_mode", "passive") != "attack":
                            continue
                        if not hasattr(artifact, "apply_passive"):
                            continue
                        message = artifact.apply_passive(player, enemy)
                        if message:
                            imprimir_texto(message)
                    break
                elif action == "2":
                    available_skills = player.get_available_skills()
                    if not available_skills:
                        imprimir_texto("No tienes ninguna habilidad activa disponible todavía.")
                        continue

                    imprimir_texto("0. Volver")
                    for i, skill in enumerate(available_skills):
                        status = skill.get_status_label(turn, player)
                        imprimir_texto(f"{C_SKILL}{i + 1}. {skill.name} (SP: {skill.sp_cost}) - {status}{RESET}")

                    while True:
                        try:
                            skill_choice = int(input("Elige habilidad: ")) - 1
                            if skill_choice == -1:
                                break
                            if 0 <= skill_choice < len(available_skills):
                                break
                            else:
                                imprimir_texto(f"{C_ENEMIGO}Elige un número entre 0 y {len(available_skills)}.{RESET}")
                        except ValueError:
                            imprimir_texto(f"{C_ENEMIGO}Introduce un número válido.{RESET}")

                    if skill_choice == -1:
                        continue
                    skill = available_skills[skill_choice]
                    if player.sp < skill.sp_cost:
                        imprimir_texto(f"{C_ENEMIGO}No tienes suficiente SP.{RESET}")
                    elif turn - skill.last_used < skill.cooldown:
                        turns_left = skill.cooldown - (turn - skill.last_used)
                        imprimir_texto(f"{C_SKILL}{skill.name}{RESET} no está lista. Faltan {C_SKILL}{turns_left}{RESET} turnos.")
                    else:
                        player.sp -= skill.sp_cost
                        skill.last_used = turn
                        imprimir_texto(skill.effect(player, enemy))
                        if getattr(player, "fled", False):
                            fled = True
                            player.fled = False
                            break
                        break

                elif action == "3":
                    if not player.inventory:
                        imprimir_texto(f"{C_ENEMIGO}No tienes ningún objeto en el inventario.{RESET}")
                        continue

                    grouped_items = summarize_inventory(player.inventory)
                    imprimir_texto("0. Volver")
                    for i, (name, count) in enumerate(grouped_items, 1):
                        imprimir_texto(f"{C_ITEM}{i}. {name} x{count}{RESET}")

                    while True:
                        try:
                            item_choice = int(input("Elige objeto: ")) - 1
                            if item_choice == -1:
                                break
                            if 0 <= item_choice < len(grouped_items):
                                break
                            else:
                                imprimir_texto(f"{C_ENEMIGO}Elige un número entre 0 y {len(grouped_items)}.{RESET}")
                        except ValueError:
                            imprimir_texto(f"{C_ENEMIGO}Introduce un número válido.{RESET}")

                    if item_choice == -1:
                        continue

                    item = get_item_by_display_index(player.inventory, item_choice + 1)
                    if item is None:
                        imprimir_texto(f"{C_ENEMIGO}No se pudo encontrar ese objeto.{RESET}")
                        continue

                    imprimir_texto(item.use(player))
                    player.inventory.remove(item)
                    break
                elif action == "4":
                    if getattr(enemy, "is_boss", False):
                        imprimir_texto(f"{C_ENEMIGO}¡No puedes huir de esta batalla! {enemy.name} te bloquea la salida.{RESET}")
                        break
                    success = random.choice([True, False])
                    if success:
                        imprimir_texto(f"{C_HEROE}{player.name}{RESET} huye del combate.")
                        fled = True
                        break
                    else:
                        imprimir_texto(f"{C_HEROE}{player.name}{RESET} no puede huir.{RESET}")
                        break
                else:
                    imprimir_texto("Acción no válida.")

        if fled:
            break

        if enemy.is_alive():
            if enemy.lose_turn:
                imprimir_texto(f"{C_ENEMIGO}{enemy.name}{RESET} no puede actuar.")
                enemy.lose_turn = False
            else:
                hp_percent = enemy.hp /enemy.hp_max
                available_skills =[]
                for skill in enemy.skills:
                    if skill.used_once and skill.skill_triggered:
                        continue  # ya se usó, descartar
                    if hp_percent > skill.hp_threshold:
                        continue  # todavía no se desbloquea con esta vida
                    if enemy.sp < skill.sp_cost:
                        continue  # sin SP suficiente
                    if turn - skill.last_used < skill.cooldown:
                        continue  # en cooldown
                    if skill.requires_buff and skill.requires_buff not in enemy.active_buffs:
                        continue  # no disponible, falta el buff
                    available_skills.append(skill)
                if available_skills:
                    skill = max(available_skills, key=lambda s: s.priority)
                    enemy.sp -= skill.sp_cost
                    skill.last_used = turn
                    if skill.used_once:
                        skill.skill_triggered = True
                    imprimir_texto(skill.effect(enemy, player))
                else:
                    damage = max(0, enemy.attack - player.defense)
                    message = player.take_damage(damage)
                    imprimir_texto(f"{C_ENEMIGO}{enemy.name}{RESET} ataca a {C_HEROE}{player.name}{RESET} y causa {C_ENEMIGO}{damage}{RESET} de daño.")
                    if message:
                        imprimir_texto(message)
        if not player.is_alive():
            for artifact in player.artifacts:
                if getattr(artifact, "trigger_mode", "passive") == "on_death":
                    message = artifact.apply_passive(player, enemy)
                    if message:
                        imprimir_texto(message)
                        
    player.attack = original_attack
    player.defense = original_defense
    player.hp_max = original_hp_max
    player.hp = min(player.hp, player.hp_max)
    player.sp_max = original_sp_max
    player.sp = min(player.sp, player.sp_max)
    for skill in player.skills:
        skill.last_used = -skill.cooldown
    if not player.is_alive():
        imprimir_texto(f"{C_BOSS}{player.name}{RESET} ha sido derrotado.")
    elif not enemy.is_alive():
        gold_gain = get_gold_gain(player, enemy.gold)
        player.gold += gold_gain
        imprimir_texto(f"{C_HEROE}{player.name}{RESET} obtiene {C_ITEM}{gold_gain}{RESET} de oro.")

        # Evitar dar múltiples botines: priorizar artefacto (si hay uno nuevo), si no, caer a item
        got_loot = False

        if enemy.loot_artifacts and random.random() < enemy.loot_artifact_chance:
            # Filtrar artefactos que el jugador ya posee
            possible = []
            for a in enemy.loot_artifacts:
                cls = a if callable(a) else type(a)
                if not any(isinstance(p, cls) for p in player.artifacts):
                    possible.append(a)

            if possible:
                artifact_choice = random.choice(possible)
                artifact = artifact_choice() if callable(artifact_choice) else artifact_choice
                imprimir_texto(player.add_artifact(artifact))
                got_loot = True

        # Solo dar item si no se otorgó artefacto
        if not got_loot and enemy.loot_items and random.random() < enemy.loot_item_chance:
            item_choice = random.choice(enemy.loot_items)
            item = item_choice() if callable(item_choice) else item_choice
            imprimir_texto(player.add_item(item))

        experience_gain = get_experience_gain(player, enemy.experience)
        player.experience += experience_gain
        imprimir_texto(f"{C_HEROE}{player.name}{RESET} ha derrotado a {C_ENEMIGO}{enemy.name}{RESET} y gana {C_ITEM}{experience_gain}{RESET} de experiencia.")
        level_up_messages = player.check_level_up()
        if level_up_messages:
            for message in level_up_messages:
                imprimir_texto(message)        