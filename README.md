# 🗡️ Slay the Papada
*Un RPG clasico de terminal por turnos con mucho lore interno, bromas y amistad.*

## 📜 Sobre el Proyecto

Este juego nace como un reto personal para dominar **Python** de forma autodidacta y, sobre todo, como una sorpresa para el grupo. Es un RPG de terminal donde una nueva generación de héroes (Matabufalez, Freakmaster, Yuri y Sami) se enfrentan a un mundo regido por el tirano Pepeda.

## ▶️ Jugar ya

¿Solo quieres jugar y no te interesa el código? Descarga el ejecutable desde [Releases](https://github.com/josedanigarcia-hue/SlayTheKebab/releases/tag/Game) y haz doble clic. Así de fácil, no necesitas tener Python instalado.

## 🧙 Los Héroes

| Personaje | Clase | En pocas palabras |
|---|---|---|
| **Matabufalez, El Papucheitor** | Tanque | Aguanta lo que le echen y pega fuerte a la vieja usanza. |
| **Freakmaster, El Tecnodruida** | Soporte / Invocador | Mezcla naturaleza, sustancias raras y tecnología con resultados impredecibles. |
| **JayC, The Chillman** | Equilibrado | No tiene prisa ni se altera por nada, ni siquiera en combate. |
| **Sami, HardcoreGuy** | Ofensivo | Sube el ritmo del combate a golpe de bombo. |
| **Secreto** | Modo Dios | Sed testigos de la fecha en que todo cambio. |


Cada uno tiene su propio árbol de habilidades, su forma de jugar y su ración de chistes internos del grupo.

## 🛠️ Tecnologías y Arquitectura

Para los colegas que venís a cotillear el código, el juego está estructurado usando Programación Orientada a Objetos (POO) y cuenta con varias mecánicas construidas desde cero:

* **Python 3:** Lógica central, sistema de combate y generación de mazmorras.
* **SQLite:** Sistema de guardado y carga de perfiles persistente.
* **Motor de Texto Custom (`colorama` + `re`):** Un sistema propio para renderizar texto estilo "máquina de escribir" que procesa códigos ANSI en tiempo real para mantener colores sin parpadeos visuales.
* **Pyfiglet:** Generación de arte ASCII para los títulos y pantallas clave.
* **Msvcrt:** Lectura de interrupciones de teclado en segundo plano (para poder saltar los textos rápidamente con el "Modo Turbo").

## 🗂️ Mapa del código

Si quieres tocar algo concreto, aquí tienes dónde mirar:

| Fichero | Qué hace |
|---|---|
| `character.py` | Los héroes, sus stats y su sistema de niveles |
| `enemy.py` | Enemigos genéricos y los jefes con su propia IA |
| `skills.py` | Habilidades, cooldowns y desbloqueos por nivel |
| `items.py` | Objetos consumibles y artefactos pasivos |
| `combat.py` | El motor de combate por turnos |
| `dungeon.py` | El árbol de nodos de la mazmorra y sus eventos |
| `storage.py` | Guardado y carga de partidas en SQLite |
| `data.py` | Datos del juego: enemigos, textos, listas |
| `main.py` | El bucle principal que lo une todo |

## 🎮 Características Principales

* **Combate Estratégico:** Gestión de vida (HP), maná (SP), y habilidades únicas escalables por nivel.
* **Inventario y Artefactos:** Sistema de consumibles y objetos pasivos (como la *Mano de Midas* o el *Álbum Chopea Pepeda*) que alteran las estadísticas base.
* **Rutas de Mazmorra:** Generación de capítulos y eventos usando una estructura de árbol de decisiones (Nodos).
* **Personajes Secretos:** Mecánicas ocultas para desbloquear clases especiales.

## 🚀 Cómo ejecutarlo en local

Si ya os habéis pasado el `.exe` y queréis trastear con el código, compilar vuestra propia versión o intentar *nerfear* a los enemigos:

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias:
   ```bash
   pip install colorama pyfiglet
   ```
3. Ejecuta el juego:
   ```bash
   python main.py
   ```

## 🙏 Agradecimientos

Este proyecto empezó como ejercicio de aprendizaje autodidacta de Python y terminó siendo un RPG sencillo pero de alguna manera "Completo". 
Gracias a todo el grupo por ser, sin saberlo, la inspiracion para esforzarme en algo asi. 
Espero que todos lo podais disfrutar tanto como yo haciendolo.
