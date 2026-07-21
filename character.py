#character.py
from skills import MadreDeGatos
from skills import CorteBienFiludo
from skills import HallDeLaFama
from item import ManoDeMidas
from item import AlbumChopeaPepeda
from item import GranNispero
import random
import textwrap
from item import AlmohadaDeYuri, BaflesDeSami, Fricandela, Mexicano, EstrellaLevante, Guldendraak, MenuRolloMixto, MenuFritaten, PistolonDeMatabufalez, RunasDeFreakmaster
from colorama import init, Fore, Back, Style
from ui import imprimir_texto, mostrar_titulo_gigante, C_HEROE, C_ENEMIGO, C_ARTIFACT, C_SISTEMA, C_SKILL, C_BOSS, C_ITEM, RESET

class Character:
    def __init__(self, name, char_class, hp, hp_max, sp, sp_max, attack, defense, level, experience):
        self.name = name
        self.char_class = char_class
        self.hp = hp
        self.hp_max = hp_max
        self.sp = sp
        self.sp_max = sp_max
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = experience
        self.inventory = []
        self.artifacts = []
        self.lose_turn = False
        self.chapter = 1
        self.current_node_id = "n0"
        self.gold = 0
        self.active_buffs = set()
        self.experience_multiplier = 1
        self.gold_multiplier = 1
        self.avoid_damage = False
        self.is_boss = False

    @property
    def lost_turn(self):
        return self.lose_turn

    @lost_turn.setter
    def lost_turn(self, value):
        self.lose_turn = value

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        if getattr(self, "avoid_damage", False):
            self.avoid_damage = False
            return f"{C_HEROE}{self.name}{RESET} evita el daño de este turno."

        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

        if self.hp <= 0:
            for artifact in list(self.artifacts):
                if getattr(artifact, "revives_on_death", False) and not getattr(artifact, "used", False):
                    artifact.used = True
                    self.hp = self.hp_max
                    self.sp = self.sp_max
                    self.lose_turn = False
                    return f"El {C_ARTIFACT}{artifact.name}{RESET} que había en el bolsillo de {C_HEROE}{self.name}{RESET} se ilumina y entra en su boca.\n{C_HEROE}{self.name}{RESET} ha sido resucitado por {C_ARTIFACT}{artifact.name}{RESET}."

        return None

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def get_status(self):
        return f"{C_HEROE}{self.name}{RESET} - HP: {C_ARTIFACT}{self.hp}{RESET}/{C_HEROE}{self.hp_max}{RESET}, SP: {C_ARTIFACT}{self.sp}{RESET}/{C_HEROE}{self.sp_max}{RESET}, level: {C_BOSS}{self.level}{RESET}"
    
    def get_stats(self):
        return f"{C_HEROE}{self.name}{RESET} - HP: {C_ARTIFACT}{self.hp}{RESET}/{C_HEROE}{self.hp_max}{RESET}, SP: {C_ARTIFACT}{self.sp}{RESET}/{C_HEROE}{self.sp_max}{RESET}, level: {C_BOSS}{self.level}{RESET}\nAttack: {C_HEROE}{self.attack}{RESET}, Defense: {C_HEROE}{self.defense}{RESET}, Experience: {C_SKILL}{self.experience}{RESET}, Gold: {C_ITEM}{self.gold}{RESET}, Chapter: {C_BOSS}{self.chapter}{RESET}"

    def get_available_skills(self):
        return [skill for skill in self.skills if skill.level_required <= self.level and not skill.is_passive]
        
    def check_level_up(self):
        messages = []
        while self.experience >= self.level * 100:
            self.experience -= self.level * 100
            self.level += 1
            self.on_level_up()
            messages.append(f"¡{C_HEROE}{self.name}{RESET} ha subido al nivel {C_SKILL}{self.level}{RESET}!")
            new_skills = [skill for skill in self.skills if skill.level_required == self.level]
            for skill in new_skills:
                messages.append(f"¡{C_HEROE}{self.name}{RESET} ha aprendido {C_SKILL}{skill.name}{RESET}!")
        return messages if messages else None

    def add_item(self, item):
        self.inventory.append(item)
        return f"¡{C_HEROE}{self.name}{RESET} ha obtenido {C_ITEM}{item.name}{RESET}!"
    
    def add_artifact(self, artifact):
        for a in self.artifacts:
            if type(a) is type(artifact) or a.name == artifact.name:
                price = getattr(artifact, 'price', 0)
                if price:
                    compensation = int(price // 2)
                    self.gold += compensation
                    return f"{C_HEROE}{self.name}{RESET} ya posee el artefacto {C_ARTIFACT}{artifact.name}{RESET}. Recibe {C_ITEM}{compensation}{RESET} de oro en compensación."
                return f"{C_HEROE}{self.name}{RESET} ya posee el artefacto {C_ARTIFACT}{artifact.name}{RESET}, no puede adquirirlo de nuevo."
        self.artifacts.append(artifact)
        mensaje_final = f"{C_HEROE}{self.name}{RESET} ha obtenido el artefacto {C_ARTIFACT}{artifact.name}{RESET}: {C_BOSS}{artifact.description}{RESET}."
        if getattr(artifact, "active_once", False):
            mensaje_efecto = artifact.apply_passive(player=self, enemy=None)
            if mensaje_efecto:
                mensaje_final += f"\n🌟 {mensaje_efecto}"                
        return mensaje_final    

    def get_epilogue(self):
        return "Epilogo del personaje: " + self.name + " ha completado su aventura en el capítulo " + str(self.chapter) + " con nivel " + str(self.level) + " y experiencia " + str(self.experience) + "."

class Matabufalez(Character):
    def __init__(self):
        super().__init__(name="Matabufalez", char_class="Matabufalez", hp=120, hp_max=120, sp=50, sp_max=50, attack=14, defense=6, level=1, experience=0)
        self.skills = [DisparoDeBalin(), GiroHipnotico(), OllaExplosiva()]
        self.inventory = [EstrellaLevante()]
        self.artifacts = [PistolonDeMatabufalez()]
        self.chapter = 1
    
    def on_level_up(self):
        self.hp_max += 15      
        self.attack += 2
        self.defense += 1
        self.sp_max += 5
        self.hp = self.hp_max
        self.sp = self.sp_max

    def get_epilogue(self):
        return textwrap.dedent(f"""\
{C_HEROE}{self.name}{RESET}, conseguiste vencer a Pepeda y, como antiguo antipepeda, lo disfrutaste durante un momento.
El cadáver de Pepeda se empezó a desvanecer en un humo azulado.
Su bastón, ahora sin dueño, cayó al suelo destruyendo su gema central. Esto activó algo, pues el suelo empezó a temblar.
Unas escaleras secretas aparecieron frente al trono donde se encontraba Pepeda.
Al bajar, te encontraste con un mapa gigantesco del mundo y distintos puntos parpadeando en rojo.
Frente al mapa había una consola con botones y pantalla. Al probarla, se confirmaron tus peores sospechas:
Pepeda no es un solo ente, el mundo está lleno de versiones tematizadas de él.
Seleccionas al Pepeda Cowboy, sonríes y, desenfundando tu pistolón, le disparas a la cabeza en la pantalla.
{C_HEROE}{self.name}{RESET}: "Tú eres el próximo..."
""")
class Yuri(Character):
    def __init__(self):
        super().__init__(name="JayC", char_class="Yuri", hp=110, hp_max=110, sp=70, sp_max=70, attack=14, defense=8, level=1, experience=0)
        self.skills = [VozConfusa(), RecitalMarxista(), SiestaMaldita()]
        self.inventory = [Fricandela()]
        self.artifacts = [AlmohadaDeYuri()]
        self.chapter = 1

    def on_level_up(self):
        self.hp_max += 10
        self.attack += 1
        self.defense += 1
        self.sp_max += 10
        self.hp = self.hp_max
        self.sp = self.sp_max

    def get_epilogue(self):
        return textwrap.dedent(f"""\
{C_HEROE}{self.name}{RESET}, conseguiste vencer a Pepeda y, como antiguo antipepeda, lo disfrutaste durante un momento.
El cadáver de Pepeda se empezó a desvanecer en un humo azulado.
Su bastón, ahora sin dueño, cayó al suelo destruyendo su gema central. Esto activó algo, pues el suelo empezó a temblar.
Unas escaleras secretas aparecieron frente al trono donde se encontraba Pepeda.
Al bajar, te encontraste con un mapa gigantesco del mundo y distintos puntos parpadeando en rojo.
Frente al mapa había una consola con botones y pantalla. Al probarla, se confirmaron tus peores sospechas:
Pepeda no es un solo ente, el mundo está lleno de versiones tematizadas de él.
Seleccionas al Zar Pepeda, bostezas y sales de la sala con muchas tranquilidad.
{C_HEROE}{self.name}{RESET}: "¡Necesito una siesta!"
""")
class Freakmaster(Character):
    def __init__(self):
        super().__init__(name="Freakmaster", char_class="Freakmaster", hp=100, hp_max=100, sp=60, sp_max=60, attack=12, defense=8, level=1, experience=0)
        self.skills = [InvocacionNatural(), SustanciasPeligrosas(), MeriendaCenaMedieval()]
        self.inventory = [EstrellaLevante()]
        self.artifacts = [RunasDeFreakmaster()]
        self.chapter = 1

    def on_level_up(self):
        self.hp_max += 8
        self.attack += 1
        self.defense += 2
        self.sp_max += 8
        self.hp = self.hp_max
        self.sp = self.sp_max

    def get_epilogue(self):
        return textwrap.dedent(f"""\
{C_HEROE}{self.name}{RESET}, conseguiste vencer a Pepeda y, como antiguo antipepeda, lo disfrutaste durante un momento.
El cadáver de Pepeda se empezó a desvanecer en un humo azulado.
Su bastón, ahora sin dueño, cayó al suelo destruyendo su gema central. Esto activó algo, pues el suelo empezó a temblar.
Unas escaleras secretas aparecieron frente al trono donde se encontraba Pepeda.
Al bajar, te encontraste con un mapa gigantesco del mundo y distintos puntos parpadeando en rojo.
Frente al mapa había una consola con botones y pantalla. Al probarla, se confirmaron tus peores sospechas:
Pepeda no es un solo ente, el mundo está lleno de versiones tematizadas de él.
Seleccionas al Ganon Pepeda, sonríes y, acariciando a Colega, sales de la sala, dispuesto a seguir con tu aventura.
{C_HEROE}{self.name}{RESET}: "¡Habrá que encontrar la Espada Maestra!"
""")
class Sami(Character):
    def __init__(self):
        super().__init__(name="Sami", char_class="Sami", hp=90, hp_max=90, sp=50, sp_max=50, attack=12, defense=6, level=1, experience=0)
        self.skills = [TeknoDiario(), TurraEterna(), BFG9000()]
        self.inventory = [Fricandela()]
        self.artifacts = [BaflesDeSami()]
        self.chapter = 1

    def on_level_up(self):
        self.hp_max += 5
        self.attack += 2
        self.defense += 2
        self.sp_max += 5
        self.hp = self.hp_max
        self.sp = self.sp_max

    def get_epilogue(self):
        return textwrap.dedent(f"""\
{C_HEROE}{self.name}{RESET}, conseguiste vencer a Pepeda y, como antiguo Propepeda, te estristeces un momento.
El cadáver de Pepeda se empezó a desvanecer en un humo azulado.
Su bastón, ahora sin dueño, cayó al suelo destruyendo su gema central. Esto activó algo, pues el suelo empezó a temblar.
Unas escaleras secretas aparecieron frente al trono donde se encontraba Pepeda.
Al bajar, te encontraste con un mapa gigantesco del mundo y distintos puntos parpadeando en rojo.
Frente al mapa había una consola con botones y pantalla. Al probarla, se confirmaron tus peores sospechas:
Pepeda no es un solo ente, el mundo está lleno de versiones tematizadas de él.
Te percatas de que bajo la consola hay una carpeta, en su portada sale una foto de una tecnosacerdote y en su primera pagina pone "PROYECTO CASTELLA".
Esa portada u el nombre del proyecto te suenan, sonries, descargas todos los archivos de la consola en un pen y sales de ahi.
{C_HEROE}{self.name}{RESET}: "¡¿En que lio te has metido Pepeda?!"
""")

class Ana(Character):
    def __init__(self):
        super().__init__(name="Ana", char_class="Ana", hp=150, hp_max=150, sp=120, sp_max=120, attack=20, defense=15, level=1, experience=0)
        self.skills = [HallDeLaFama(), CorteBienFiludo(), MadreDeGatos()]
        self.inventory = [MenuRolloMixto(), MenuRolloMixto(), MenuRolloMixto(), MenuRolloMixto(), MenuRolloMixto()]
        self.artifacts = []
        self.add_artifact(AlbumChopeaPepeda())
        self.add_artifact(ManoDeMidas())
        self.chapter = 1

    def on_level_up(self):
        self.hp_max += 10
        self.attack += 3
        self.defense += 3
        self.sp_max += 10
        self.hp = self.hp_max
        self.sp = self.sp_max

    def get_epilogue(self):
        return textwrap.dedent(f"""\
{C_HEROE}{self.name}{RESET}, conseguiste vencer a Pepeda y, como su esposa, lo disfrutaste bastante pero tambien te entristece.
Tu ultimo golpe fue certero pero Pepeda aun respira, te acercas a el y con una caricia en su cara le dices: {C_ARTIFACT}"Te lo dije".{RESET}
{C_ENEMIGO}Pepeda:{C_SKILL}"Sabes que lo hacia por nosotros, pero sin darme cuenta perdi el control... no queria haceros daño..."{RESET}
{C_HEROE}{self.name}{RESET}: {C_ARTIFACT}"Lo se, por eso debia pararte. Tu no eres asi."{RESET}
{C_ENEMIGO}Pepeda:{C_SKILL}"Gracias por perdonarme... toma esto..."{RESET}
El cuerpo de Pepeda se ilumina y desaparece dejando en tu mano un trozo metalico con inscripciones, tiene pestañas o clavijas que te hacen pensar que forma parte de algo mas grande.
Su bastón, ahora sin dueño, cayó al suelo destruyendo su gema central. Esto activó algo, pues el suelo empezó a temblar.
Unas escaleras secretas aparecieron frente al trono donde se encontraba Pepeda.
Al bajar, te encontraste con un mapa gigantesco del mundo y distintos puntos parpadeando en rojo.
Frente al mapa había una consola con botones y pantalla. Al probarla, se confirmaron tus peores sospechas:
Pepeda no es un solo ente, el mundo está lleno de versiones tematizadas de él.
Localizas un hueco en la consola donde encaja el trozo metalico que tienes en la mano, al colocarlo se abre un portal frente al mapa.
Miras a Darwin y Ragnar que te contestan con un maullido y sin dudarlo, entrais en el portal.
{C_HEROE}{self.name}{RESET}: {C_ARTIFACT}"¡Ya le dije que si seguia obsesionandose con la kebabtologia pasaria esto!"{RESET}
""")

from skills import DisparoDeBalin, GiroHipnotico, OllaExplosiva, VozConfusa, RecitalMarxista, SiestaMaldita, InvocacionNatural, SustanciasPeligrosas, MeriendaCenaMedieval, TeknoDiario, TurraEterna, BFG9000