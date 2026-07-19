#main.py

import sqlite3
import sys
import time
import re
import os
from colorama import init, Fore, Back, Style
init(autoreset=True)
os.system("")
# pyrefly: ignore [missing-import]
import pyfiglet
from character import Matabufalez, Yuri, Freakmaster, Sami, Ana
from combat import combat
from dungeon import build_dungeon, run_node, find_node
from storage import save_player, load_player, has_saved_players, delete_saved_game
from inventory_utils import summarize_inventory, get_item_by_display_index
from ui import imprimir_texto, mostrar_titulo_gigante, C_HEROE, C_ENEMIGO, C_ARTIFACT, C_SISTEMA, C_SKILL, C_BOSS, C_ITEM, RESET

def init_db():
    conn = sqlite3.connect("saved_players.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            name TEXT PRIMARY KEY,
            char_class TEXT,
            hp INTEGER,
            hp_max INTEGER,
            sp INTEGER,
            sp_max INTEGER,
            attack INTEGER,
            defense INTEGER,
            level INTEGER,
            experience INTEGER,
            chapter INTEGER,
            current_node_id TEXT,
            inventory TEXT,
            artifacts TEXT
        )
        """
    )

    existing_columns = {row[1] for row in cursor.execute("PRAGMA table_info(players)")}
    required_columns = {
        "char_class": "TEXT",
        "hp": "INTEGER",
        "hp_max": "INTEGER",
        "sp": "INTEGER",
        "sp_max": "INTEGER",
        "attack": "INTEGER",
        "defense": "INTEGER",
        "level": "INTEGER",
        "experience": "INTEGER",
        "chapter": "INTEGER",
        "current_node_id": "TEXT",
        "inventory": "TEXT",
        "artifacts": "TEXT",
    }

    for column_name, column_type in required_columns.items():
        if column_name not in existing_columns:
            cursor.execute(f"ALTER TABLE players ADD COLUMN {column_name} {column_type}")

    conn.commit()
    conn.close()

def intro_screen():
    print("\n" * 2) # Limpiamos un poco la pantalla
    mostrar_titulo_gigante("Slay the Kebab", Fore.CYAN, "doom")
    
    imprimir_texto("En un mundo donde la bondad ha desaparecido y el mayor ejemplo de virtud se volvio un tirano...", 0.04)
    imprimir_texto("Te levantas resignado, pues ya no aguantas mas la represion.", 0.04)
    imprimir_texto("Justo cuando esa idea asoma en tu cabeza una luz resplandeciente ilumina tu habitacion, en ella aparece una diosa", 0.04)
    imprimir_texto(f"{C_BOSS}Ana, reencarnacion de Freya:{RESET} Solo tu, amigo de {C_BOSS}Pepeda, el Sultan{RESET}, puedes acabar con esta pesadilla.", 0.04)

def select_player():
    intro_screen()
    imprimir_texto(f"{C_BOSS}Ana, Reencarnacion de Freya{RESET}: ¿Quien eres tu?")
    imprimir_texto(f"{C_HEROE}1. Matabufalez, El Papucheitor{RESET}")
    imprimir_texto(f"{C_HEROE}2. Freakmaster, El Tecnodruida{RESET}")
    imprimir_texto(f"{C_HEROE}3. JayC, The Chillman{RESET}")
    imprimir_texto(f"{C_HEROE}4. Sami, El HardcoreGuy{RESET}")
    while True:
        choice = input("Ingresa el número de tu personaje: ")
        if choice == "1":
            return Matabufalez()
        elif choice == "2":
            return Freakmaster()
        elif choice == "3":
            return Yuri()
        elif choice == "4":
            return Sami()
        elif choice == "210522":
            return Ana()
        else:
            print(f"{C_ENEMIGO}Opción no válida.{RESET}")

def show_epilogue(player):
    print(f"\n{'='*60}")
    mostrar_titulo_gigante("EPILOGO", C_BOSS, "slant")
    print(f"{'='*60}\n")
    imprimir_texto(player.get_epilogue())

def show_credits():
    print(f"\n{'='*60}")
    mostrar_titulo_gigante("Slay The Kebab", C_ARTIFACT, "slant")
    print(f"{'='*60}\n")
    imprimir_texto("Un juego creado con cariño y aprecio, espero que lo hayais disfrutado")
    imprimir_texto("\n¡Gracias por jugar!")

def main():
    init_db()
    while True:
        mostrar_titulo_gigante("PAPADAS GAMES", C_BOSS, "doom")
        imprimir_texto(f"{C_BOSS}Presenta{RESET}")
        if has_saved_players():
            choice = input("¿Quieres continuar una partida existente?\n1. Nueva partida\n2. Continuar partida\nElige: ")
            if choice == "2":
                player = load_player()
                imprimir_texto(f"¡Bienvenido de nuevo, {C_HEROE}{player.name}{RESET}! Continuemos tu aventura.")                
            else:
                delete_saved_game()  # Eliminar partida guardada para evitar confusión
                player = select_player()
                imprimir_texto(f"¡Bienvenido, {C_HEROE}{player.name}{RESET}! Tu aventura comienza ahora.")        
        else: 
            player = select_player()
            imprimir_texto(f"¡Bienvenido, {C_HEROE}{player.name}{RESET}! Tu aventura comienza ahora.")
        dungeon_root = build_dungeon()
        current_node = find_node(dungeon_root, player.current_node_id)
        while player.is_alive():
            imprimir_texto("\n¿Qué quieres hacer?:")
            imprimir_texto("1. Avanzar")
            imprimir_texto("2. Ver estado")
            imprimir_texto("3. Guardar partida")
            action = input("Elige: ")
            if action == "1":
                if current_node.children:
                    imprimir_texto("\n¿Hacia dónde quieres ir?")
                    for i, child in enumerate(current_node.children):
                        imprimir_texto(f"{i + 1}. {child.event_type}")
                    while True:
                        try:
                            choice = int(input("Elige: ")) - 1
                            if 0 <= choice < len(current_node.children):
                                current_node = current_node.children[choice]
                                player.current_node_id = current_node.node_id
                                break
                            else:
                                imprimir_texto (f"Elige entre 1 y {len(current_node.children)}.")
                        except ValueError:
                            imprimir_texto("Introduce un número valido")
                    run_node(player, current_node, player.chapter)
                else:
                    # no hay más caminos — fin del árbol actual
                    if player.is_alive():
                        if player.chapter == 3:
                            # ¡Fin del juego!
                            show_epilogue(player)
                            show_credits()
                            break  # o break, según cómo esté estructurado el bucle en main()
                        else:
                            player.chapter += 1
                            imprimir_texto(f"\n{C_SKILL}¡Capítulo {C_BOSS}{player.chapter - 1}{C_SKILL} completado! Comienza el Capítulo {C_BOSS}{player.chapter}{C_SKILL}.{RESET}")
                            dungeon_root = build_dungeon()
                            current_node = find_node(dungeon_root, "n0")
                            player.current_node_id = "n0"
                    else:
                        imprimir_texto(f"{C_SISTEMA}Has sido derrotado.{RESET}")            
            elif action == "2":
                # Submenu Ver estado
                while True:
                    imprimir_texto("\nVer estado:")
                    imprimir_texto("0. Volver")
                    imprimir_texto("1. Estadisticas")
                    imprimir_texto("2. Inventario")
                    sub = input("Elige: ")
                    if sub == "0":
                        break
                    elif sub == "1":
                        imprimir_texto(player.get_stats())
                    elif sub == "2":
                        while True:
                            imprimir_texto("\nInventario:")
                            imprimir_texto("0. Volver")
                            imprimir_texto("1. Objetos")
                            imprimir_texto("2. Artefactos")
                            inv_sub = input("Elige: ")
                            if inv_sub == "0":
                                break
                            elif inv_sub == "1":
                                if not player.inventory:
                                    imprimir_texto("No tienes objetos.")
                                    continue
                                grouped_items = summarize_inventory(player.inventory)
                                imprimir_texto("\nTus objetos:")
                                for i, (name, count) in enumerate(grouped_items, 1):
                                    imprimir_texto(f"{i}. {C_ITEM}{name}{RESET} x{count}")
                                imprimir_texto("0. Volver")
                                while True:
                                    try:
                                        choice = int(input("Elige objeto para ver descripción (0 volver): "))
                                        if choice == 0:
                                            break
                                        item = get_item_by_display_index(player.inventory, choice)
                                        if item is not None:
                                            imprimir_texto(f"\n{C_ITEM}{item.name}{RESET}: {item.description}\n")
                                            input(f"{C_SISTEMA}Presiona Enter para volver a la lista de objetos...{RESET}")
                                        else:
                                            imprimir_texto(f"Elige un número entre 0 y {len(grouped_items)}.")
                                    except ValueError:
                                        imprimir_texto("Introduce un número válido.")
                            elif inv_sub == "2":
                                if not player.artifacts:
                                    imprimir_texto("No tienes artefactos.")
                                    continue
                                grouped_artifacts = summarize_inventory(player.artifacts)
                                imprimir_texto("\nTus artefactos:")
                                for i, (name, count) in enumerate(grouped_artifacts, 1):
                                    imprimir_texto(f"{i}. {C_ARTIFACT}{name}{RESET} x{count}")
                                imprimir_texto("0. Volver")
                                while True:
                                    try:
                                        choice = int(input("Elige artefacto para ver descripción (0 volver): "))
                                        if choice == 0:
                                            break
                                        art = get_item_by_display_index(player.artifacts, choice)
                                        if art is not None:
                                            imprimir_texto(f"\n{C_ARTIFACT}{art.name}{RESET}: {art.description}\n")
                                            input(f"{C_SISTEMA}Presiona Enter para volver a la lista de artefactos...{RESET}")
                                        else:
                                            imprimir_texto(f"Elige un número entre 0 y {len(grouped_artifacts)}.")
                                    except ValueError:
                                        imprimir_texto("Introduce un número válido.")
                            else:
                                imprimir_texto("Opción no válida.")
                    else:
                        imprimir_texto("Opción no válida.")
            elif action == "3":
                save_player(player)
            else:
                imprimir_texto("Opción no válida.")
        if player.is_alive():
            imprimir_texto("\n¡Felicidades por completar tu aventura!")
        else:
            imprimir_texto("Game Over. Gracias por jugar.")
        restart = input("¿Quieres jugar de nuevo? (s/n) ")
        if restart.lower() != "s":
            imprimir_texto("¡Hasta la próxima, aventurero!")
            break


if __name__ == "__main__":
    main()