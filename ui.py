import sys
import time
import re
import os
import pyfiglet
from colorama import init, Fore, Style

init(autoreset=True)
os.system("")

try:
    import msvcrt
except ImportError:
    msvcrt = None

# Paleta de colores del juego
C_HEROE = Fore.GREEN + Style.BRIGHT     # Verde brillante para Alan, Sami, Yuri...
C_ENEMIGO = Fore.RED + Style.BRIGHT     # Rojo brillante para los monstruos
C_BOSS = Fore.MAGENTA + Style.BRIGHT    # Magenta para los jefes
C_SKILL = Fore.CYAN                     # Ciano para las habilidades
C_ITEM = Fore.YELLOW                    # Amarillo para consumibles
C_ARTIFACT = Fore.LIGHTBLUE_EX          # Azul claro para los artefactos mágicos
C_SISTEMA = Fore.WHITE + Style.DIM      # Blanco apagado para turnos o separadores "==="
RESET = Style.RESET_ALL

def imprimir_texto(texto, velocidad=0.02):
    """Imprime el texto letra a letra, manteniendo el color activo en cada letra."""
    ansi_escape = re.compile(r'(\x1b\[.*?m)')
    partes = ansi_escape.split(texto)
    color_actual = ""  # Aquí guardaremos el color que esté sonando
    
    if msvcrt:
        while msvcrt.kbhit():
            msvcrt.getch()

    saltar_efecto = False # Bandera que nos dirá si debemos ir a máxima velocidad

    for parte in partes:
        if parte.startswith('\x1b['):
            if parte == Style.RESET_ALL or parte == '\x1b[0m':
                color_actual = ""
            else:
                color_actual += parte
        else:
            for letra in parte:
                print(color_actual + letra, end="", flush=True)
                
                # Si no han pulsado nada, hacemos la pausa normal
                if not saltar_efecto:
                    time.sleep(velocidad)
                    
                    # Comprobamos si el jugador acaba de pulsar una tecla (Intro, Espacio, etc.)
                    if msvcrt and msvcrt.kbhit():
                        msvcrt.getch() # "Tragamos" la pulsación para que no estorbe
                        saltar_efecto = True # ¡Activamos el turbo para el resto de la frase!
    print()

def mostrar_titulo_gigante(texto, color=Fore.WHITE, fuente="slant"):
    """
    Imprime un texto en formato ASCII gigante.
    Fuentes recomendadas: 'slant', 'doom', 'big', 'standard'
    """
    try:
        ascii_art = pyfiglet.figlet_format(texto, font=fuente)
        print(color + Style.BRIGHT + ascii_art + Style.RESET_ALL)
    except pyfiglet.FontNotFound:
        # Por si te equivocas escribiendo el nombre de la fuente
        ascii_art = pyfiglet.figlet_format(texto)
        print(color + Style.BRIGHT + ascii_art + Style.RESET_ALL)
