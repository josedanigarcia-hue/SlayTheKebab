from string import templatelib
from pickle import TRUE
import random
from ui import imprimir_texto, mostrar_titulo_gigante, C_HEROE, C_ENEMIGO, C_ARTIFACT, C_SISTEMA, C_SKILL, C_BOSS, C_ITEM, RESET


class Skill:
    def __init__(self, name, sp_cost, cooldown, level_required, is_passive=False, passive_once=False, used_once=False, hp_threshold=1.0, priority=0, requires_buff=None):
        self.name = name
        self.sp_cost = sp_cost
        self.cooldown = cooldown
        self.level_required = level_required
        self.is_passive = is_passive
        self.passive_once = passive_once
        self.passive_triggered = False  # para habilidades pasivas que solo se activan una vez
        self.last_used = -cooldown  # para que esté disponible al inicio
        self.used_once = used_once
        self.skill_triggered = False
        self.hp_threshold = hp_threshold
        self.priority = priority
        self.requires_buff = requires_buff

    def can_use(self, character, current_turn):
        sp_ok = character.sp >= self.sp_cost
        level_ok = character.level >= self.level_required
        cooldown_ok = current_turn - self.last_used >= self.cooldown
        return sp_ok and level_ok and cooldown_ok

    def get_status_label(self, current_turn, character):
        if not self.can_use(character, current_turn):
            turns_left = self.cooldown - (current_turn - self.last_used)
            if turns_left <= 1:
                return "1 turno restante"
            return f"{C_ENEMIGO}{turns_left} turnos restantes{RESET}"
        return "Disponible"
    
    def passive_effect(self, user, target):
        return None

#Skills de Jugador
class DisparoDeBalin(Skill):
    def __init__(self):
        super().__init__(name="Disparo de Balín", sp_cost=20, cooldown=3, level_required=1)

    def effect(self, user, target):
        damage = int(user.attack * 2.5 - target.defense)
        target.take_damage(damage)
        return f"¡{C_HEROE}{user.name}{RESET} dispara un balín a {C_ENEMIGO}{target.name}{RESET} y hace {C_ARTIFACT}{damage}{RESET} de daño!"

class GiroHipnotico(Skill):
    def __init__(self):
        super().__init__(name="Giro Hipnótico", sp_cost=40, cooldown=5, level_required=5)

    def effect(self, user, target):
        damage = int(target.attack * 3 - target.defense)
        target.take_damage(damage)
        target.lose_turn = True
        return f"¡{C_HEROE}{user.name}{RESET} realiza un giro hipnótico con un final remangandose y {C_ENEMIGO}{target.name}{RESET} intenta imitarlo pero sufre {C_ARTIFACT}{damage}{RESET} de daño y pierde el turno!\n{C_ENEMIGO}{target.name}{RESET}: '¡Haces que parezca facil!'"

class OllaExplosiva(Skill):
    def __init__(self):
        super().__init__(name="Olla Explosiva", sp_cost=50, cooldown=4, level_required=10)

    def effect(self, user, target):
        damage = random.randint(int(user.attack * 6), int(user.attack * 8) - target.defense)
        target.take_damage(damage)
        return f"¡{C_HEROE}{user.name}{RESET} lanza una olla explosiva a {C_ENEMIGO}{target.name}{RESET} y hace {C_ARTIFACT}{damage}{RESET} de daño!\n{random.choice(['¡Ha sido una explosion incendiaria!', '¿Estaba llena de cerveza?', '¿Eso son garbanzos? Joder, que hambre'])}"
    
class VozConfusa(Skill):
    def __init__(self):
        super().__init__(name="Voz Confusa", sp_cost=0, cooldown=0, level_required=1, is_passive=True)

    def passive_effect(self, user, target):
        success = random.choices([True, False], weights=[30, 70], k=1)[0]
        if success:
            target.lose_turn = True
            target.defense = int(target.defense * 0.5)
            return f"{C_SKILL}¡Voz Confusa!{RESET} {C_ENEMIGO}{target.name}{RESET} pierde el turno y su defensa es reducida a la mitad.\n{C_ENEMIGO}{target.name}{RESET}: '¿No decias que solo habria hombres?'"
    
class RecitalMarxista(Skill):
    def __init__(self):
        super().__init__(name="Recital Marxista", sp_cost=30, cooldown=4, level_required=4)

    def effect(self, user, target):
        damage = random.randint(int(user.attack * 3.5), int(user.attack * 5))
        target.take_damage(damage)
        return f"¡{C_HEROE}{user.name}{RESET} recita parrafo a parrafo en ruso el manifiesto comunista blandiendo una hoz y martillo contra {C_ENEMIGO}{target.name}{RESET} y provoca {C_ARTIFACT}{damage}{RESET} de daño!"

class SiestaMaldita(Skill):
    def __init__(self):
        super().__init__(name="Siesta Maldita", sp_cost=50, cooldown=5, level_required=8)

    def effect(self, user, target):
        heal_amount = random.randint(int(user.hp_max * 0.5), int(user.hp_max * 0.8))
        user.heal(heal_amount)
        if target.lose_turn:
            damage = random.randint(int(target.attack * 3.5), int(target.attack * 4.5))
            target.take_damage(damage)
            return f"¡{C_HEROE}{user.name}{RESET} se echa una siesta maldita y recupera {C_ARTIFACT}{heal_amount}{RESET} de HP!\n¡{C_ENEMIGO}{target.name}{RESET} cayo en la siesta maldita, pero no supo controlar su poder y se hizo daño a si mismo! ¡{C_ARTIFACT}{damage}{RESET} de daño!"
        else:
            return f"¡{C_HEROE}{user.name}{RESET} se echa una siesta maldita y recupera {C_ARTIFACT}{heal_amount}{RESET} de HP!"

class InvocacionNatural(Skill):
    def __init__(self):
        super().__init__(name="Gatcha Invocación", sp_cost=10, cooldown=2, level_required=1)

    def effect(self, user, target):
        effect = random.choices(["ardilla","colega","elefante"], weights=[25, 50, 25], k=1)[0]
        if effect == "ardilla":
            heal_amount = random.randint(int(user.hp_max * 0.1), int(user.hp_max * 0.3))
            user.heal(heal_amount)
            return f"¡{C_HEROE}{user.name}{RESET} invoca a una ardilla que le entrega una manzana dorada y recupera {C_ARTIFACT}{heal_amount}{RESET} de HP!"
        elif effect == "colega":
            damage = random.randint(int(user.attack * 2.5), int(user.attack * 3.5))
            target.take_damage(damage)
            return f"¡{C_HEROE}{user.name}{RESET} invoca a su fiel perro Colega que ataca a {C_ENEMIGO}{target.name}{RESET} causando {C_ARTIFACT}{damage}{RESET} de daño!"
        else:
            damage = random.randint(int(user.attack * 5), int(user.attack * 6))
            target.take_damage(damage)
            return f"¡{C_HEROE}{user.name}{RESET} invoca a un Doble Elefante Telepata de Guerra que arrolla a {C_ENEMIGO}{target.name}{RESET} causando {C_ARTIFACT}{damage}{RESET} de daño!"

class SustanciasPeligrosas(Skill):
    def __init__(self):
        super().__init__(name="Sustancias Peligrosas", sp_cost=20, cooldown=3, level_required=5)

    def effect(self, user, target):
        amount = random.randint(int(user.attack * 3), int(user.attack * 5))
        heal = int(amount/2)
        user.heal(heal) # el usuario se cura la mitad del daño que va a causar
        target.take_damage(amount)
        return f"¡{C_HEROE}{user.name}{RESET} prepara un brebaje con sustancias de dudosa procedenciay se lo bebe, recupera {C_ARTIFACT}{heal}{RESET} de HP y arroja lo que queda a {C_ENEMIGO}{target.name}{RESET} causando {C_ARTIFACT}{amount}{RESET} de daño!\n{random.choice(['¡Eso huele fatal!', '¿Que es eso? ¿Cristal? ¿Veneno? ¡¿Sangre?!', '¡Espero que sea mayonesa!'])}"

class MeriendaCenaMedieval(Skill):
    def __init__(self):
        super().__init__(name="MeriendaCena 40K", sp_cost=40, cooldown=4, level_required=10)

    def effect(self, user, target):
        damage = random.choice([int(user.attack * 5), int(user.attack * 6), int(user.attack * 7), int(user.attack * 8), int(user.attack * 40000)])
        target.take_damage(damage)
        return f"¡{C_HEROE}{user.name}{RESET} invoca a todas las razas del universo de Warhammer 40K para darse un festin, tras la comida todos entran en un frenesi de violencia y atacan a {C_ENEMIGO}{target.name}{RESET} causando {C_ARTIFACT}{damage}{RESET} de daño!\n{random.choice(['¡Eso es un exterminatus!', 'Eso no es una morcilla de burgos', '¡¿donde esta mi brazo?!', '¡¿Ese es un dios del caos?!'])}"

class TeknoDiario(Skill):
    def __init__(self):
        super().__init__(name="Tekno Diario", sp_cost=0, cooldown=0, level_required=1, is_passive=True, passive_once=True)

    def passive_effect(self, user, target):
        user.attack += (user.level * 2)  # aumenta el ataque en función del nivel
        user.defense += (user.level * 2) # aumenta la defensa en función del nivel
        return f"¡{C_HEROE}{user.name}{RESET} pone su temazo diario y se siente más fuerte! Ataque y defensa aumentados en {C_ARTIFACT}{user.level * 2}{RESET} puntos cada uno."

class TurraEterna(Skill):
    def __init__(self):
        super().__init__(name="Turra Eterna", sp_cost=25, cooldown=2, level_required=4)

    def effect(self, user, target):
        damage = random.randint(int(user.attack * 3.5), int(user.attack * 5.5) - target.defense)
        target.take_damage(damage)
        return f"¡{C_HEROE}{user.name}{RESET} suelta una turra eterna y destroza mentalmente a {C_ENEMIGO}{target.name}{RESET} causando {C_ARTIFACT}{damage}{RESET} de daño!\n{random.choice(['¡¿Quien cojones es Hardcore Schwarzenegger!?', '¡¿Cuantas veces has repetido eso?!', '¡¿Por qué no te callas?!'])}"

class BFG9000(Skill):
    def __init__(self):
        super().__init__(name="BFG 9000", sp_cost=150, cooldown=5, level_required=8)

    def effect(self, user, target):
        damage = int(user.attack * 8 - target.defense)
        target.take_damage(damage)
        return f"¡{C_HEROE}{user.name}{RESET} utiliza el {C_ARTIFACT}BFG 9000{RESET} y destruye a {C_ENEMIGO}{target.name}{RESET} causando {C_ARTIFACT}{damage}{RESET} de daño!"

class HallDeLaFama(Skill):
    def __init__(self):
        super().__init__(name="Hall de la Fama", sp_cost=20, cooldown=1, level_required=0)

    def effect(self, user, target):
        pokeball = random.choice(["Pokeball","Superball","Ultraball","Masterball"])
        if pokeball == "Pokeball":
            damage = random.randint(int(user.attack * 1.5), int(user.attack * 2.5) - target.defense)
            if damage < 1:
                damage = 0
            target.take_damage(damage)
            return f"¡{C_HEROE}{user.name}{RESET} lanza una {C_ENEMIGO}Pokeball{RESET} frente a {C_ENEMIGO}{target.name}{RESET} y aparece Espeon usando Psiquico, causando {C_ENEMIGO}{damage}{RESET} de daño!"
        elif pokeball == "Superball":
            damage = random.randint(int(user.attack * 2.5), int(user.attack * 3.5) - target.defense)
            if damage < 1:
                damage = 0
            target.take_damage(damage)
            return f"¡{C_HEROE}{user.name}{RESET} lanza una {C_SKILL}Superball{RESET} frente a {C_ENEMIGO}{target.name}{RESET} y aparece Feraligatr usando Hidrobomba, causando {C_ENEMIGO}{damage}{RESET} de daño!"
        elif pokeball == "Ultraball":
            damage = random.randint(int(user.attack * 3.5), int(user.attack * 4.5) - target.defense)
            if damage < 1:
                damage = 0
            target.take_damage(damage)
            return f"¡{C_HEROE}{user.name}{RESET} lanza una {C_ITEM}Ultraball{RESET} frente a {C_ENEMIGO}{target.name}{RESET} y aparece Dragonite usando Hiper Rayo, causando {C_ENEMIGO}{damage}{RESET} de daño!"
        else:
            damage = random.randint(int(user.attack * 4.5), int(user.attack * 5.5) - target.defense)
            if damage < 1:
                damage = 0
            target.take_damage(damage)
            return f"¡{C_HEROE}{user.name}{RESET} lanza una {C_BOSS}Masterball{RESET} frente a {C_ENEMIGO}{target.name}{RESET} y aparece Rayquaza usando Cometa Draco, causando {C_ENEMIGO}{damage}{RESET} de daño!"

class CorteBienFiludo(Skill):
    def __init__(self):
        super().__init__(name="Corte Bien Filudo", sp_cost=40, cooldown=3, level_required=7)

    def effect(self, user, target):
        damage = random.randint(int(user.attack * 4), int(user.attack * 6) - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        user.attack += 10
        return f"¡{C_HEROE}{user.name}{RESET} saca unas tijeras bien filudas y le hace un nuevo corte de pelo a {C_ENEMIGO}{target.name}{RESET} causando {C_ENEMIGO}{damage}{RESET} de daño!\nCuanto mas se usan las tijeras, mas filudas estan y su ataque aumenta en 10 puntos."

class MadreDeGatos(Skill):
    def __init__(self):
        super().__init__(name="Madre de Gatos", sp_cost=50, cooldown=5, level_required=10)

    def effect(self, user, target):
        damage = random.randint(int(user.attack * 7), int(user.attack * 10) - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        return f"¡{C_HEROE}{user.name}{RESET} llama a sus fieles gatos, Ragnar y Darwin, y ellos masacran a {C_ENEMIGO}{target.name}{RESET} causando {C_ENEMIGO}{damage}{RESET} de daño!\n¡MIAAAAAUUUUUUUU!"

#Skills de Enemigos:    
class OracionEspectral(Skill):
    def __init__(self):
        super().__init__(name="Cuñadismo Espectral", sp_cost=20, cooldown=4, level_required=1, hp_threshold=1.0, priority=0)

    def effect(self, user, target):
        damage = int(user.attack * 1.5 - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        success = random.choice([True, False])
        target.lose_turn = success
        if target.lose_turn:
            return f"¡{C_ENEMIGO}{user.name}{RESET} usa {C_BOSS}Cuñadismo Espectral{RESET}!\n¡{C_ENEMIGO}{user.name}{RESET} recita un frason de lo mas cuñado y fantasma, haciendo {C_ARTIFACT}{damage}{RESET} de daño a {C_HEROE}{target.name}{RESET}.\nAdemas, {C_HEROE}{target.name}{RESET} ha quedado tan impactado necesita un turno para recuperarse."
        else:
            return f"¡{C_ENEMIGO}{user.name}{RESET} usa {C_BOSS}Cuñadismo Espectral{RESET}!\n¡{C_ENEMIGO}{user.name}{RESET} recita un frason de lo mas cuñado y fantasma, haciendo {C_ARTIFACT}{damage}{RESET} de daño a {C_HEROE}{target.name}{RESET}."

class EraTanFacil(Skill):
    def __init__(self):
        super().__init__(name="Era Tan Facil", sp_cost=40, cooldown=4, level_required=2, hp_threshold=0.75, priority=1)

    def effect(self, user, target):
        effect = random.choice(["1","1","1","2","2","3"])
        if effect == "1":
            damage = random.randint(int(user.attack * 2) - target.defense, int(user.attack * 3) - target.defense)
            if damage < 1:
                damage = 0
            target.take_damage(damage)
            return f"¡{C_ENEMIGO}{user.name}{RESET} grita {C_BOSS}ERA TAN FACIL{RESET}!\nTras ello invoca a sniper que carga su rifle y dispara causando {C_ARTIFACT}{damage}{RESET} de daño a {C_HEROE}{target.name}{RESET}."
        elif effect == "2":
            meepos = random.randint(1, 6)
            damage = int(user.attack * meepos - target.defense)
            if damage < 1:
                damage = 0
            target.take_damage(damage)
            return f"¡{C_ENEMIGO}{user.name}{RESET} grita {C_BOSS}ERA TAN FACIL{RESET}!\nTras ello invoca {meepos} meepo(s) que captura con sus redes a {C_HEROE}{target.name}{RESET} y tras un baile explosivo le causa {C_ARTIFACT}{damage}{RESET} de daño a {C_HEROE}{target.name}{RESET}."
        else:
            return f"¡{C_ENEMIGO}{user.name}{RESET} grita {C_BOSS}ERA TAN FACIL{RESET}!\nTras ello invoca a Antimage pero ignora el combate y se queda farmeando la linea"
        
class IsakAplasta(Skill):
    def __init__(self):
        super().__init__(name="Isak Aplasta", sp_cost=80, cooldown=8, level_required=3, hp_threshold=0.5, priority=2, used_once=True)

    def effect(self, user, target):
        damage = int(user.attack * 4 - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        user.lose_turn = True
        return f"{C_ENEMIGO}{user.name}{RESET}: Te voy a enseñar mi tecnica definitiva, heredada del maestro de batalla Hualk\n{C_ENEMIGO}{user.name}{RESET} levanta sus brazos y sus manos, de por si grandes, empiezan a crecer desmesuradamente\n{C_ENEMIGO}{user.name}{RESET} cierra los puños y golpea el suelo gritando: {C_BOSS}¡ISAK SMASH!{RESET}\nEl choque provoca una explosion que deja un crater en la estancia y provoca {C_ARTIFACT}{damage}{RESET} de daño a {C_HEROE}{target.name}{RESET}."
    
class YameteKudasai(Skill):
    def __init__(self):
        super().__init__(name="Yamete Kudasai", sp_cost=35, cooldown=5, level_required=1, hp_threshold=1.0, priority=0)

    def effect(self, user, target):
        target.lost_turn = True
        effect = random.choice(["hp", "sp"])
        if effect == "hp":
            user.heal(50)
            return f"¡{C_ENEMIGO}{user.name}{RESET} gime diciendo {C_BOSS}'¡¡¡YAMETE KUDASAI!!!'{RESET}\nEsto aturde a {C_HEROE}{target.name}{RESET} perdiendo su siguiente turno.\n{C_ENEMIGO}{user.name}{RESET} recupera 50 puntos de vida."
        else:
            user.sp += 30
            return f"¡{C_ENEMIGO}{user.name}{RESET} gime diciendo {C_BOSS}'¡¡¡YAMETE KUDASAI!!!'{RESET}\nEsto aturde a {C_HEROE}{target.name}{RESET} perdiendo su siguiente turno.\n{C_ENEMIGO}{user.name}{RESET} recupera 50 puntos de mana."

class  ZokusheiShokan(Skill):
    def __init__(self):
        super().__init__(name="Zousheki Shōkan", sp_cost=55, cooldown=5, level_required=1, hp_threshold=0.75, priority=1)

    def effect(self, user, target):
        effect = random.choice(["JuicioFinal", "Meteoro", "Thor", "Boreal"])
        if effect == "JuicioFinal":
            return self.juicio_final(user, target)
        elif effect == "Meteoro":
            return self.meteoro(user, target)
        elif effect == "Thor":
            return self.thor(user, target)
        else:
            return self.boreal(user, target)

    def juicio_final(self, user, target):
        damage = int(user.attack * 5 - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        return f"¡{C_ENEMIGO}{user.name}{RESET} grita '{C_BOSS}Zousheki Shōkan: Juicio Final{RESET}' y aparecen a su alrededor decenas de djinn de Tierra!\n¡Los djinn de tierra se unen y mandan su energia al cielo!\n¡{C_ENEMIGO}{user.name}{RESET} alza el brazo, sonrie y al levantar la mirada ve a una especie de angel con una cabeza de leon en el brazo cargando un rayo que cae directamente sobre {C_HEROE}{target.name}{RESET}\n{C_HEROE}{target.name}{RESET} recibe {C_ARTIFACT}{damage}{RESET} puntos de daño."

    def meteoro(self, user, target):
        damage_1 = int(user.attack * 2 - target.defense)
        damage_2 = int(user.attack * 2 - target.defense)
        damage_3 = int(user.attack * 2 - target.defense)
        if damage_1 < 1:
            damage_1 = 0
        if damage_2 < 1:
            damage_2 = 0
        if damage_3 < 1:
            damage_3 = 0
        target.take_damage(damage_1 + damage_2 + damage_3)
        return f"¡{C_ENEMIGO}{user.name}{RESET} grita '{C_BOSS}Zousheki Shōkan: Meteoro{RESET}' y aparecen a su alrededor decenas de djinn de fuego!\n¡Los djinn de fuego se unen y mandan su energia al cielo!\n¡{C_ENEMIGO}{user.name}{RESET} alza el brazo, sonrie y al levantar la mirada ve un meteorito gigante acompañado de otros mas pequeños que caen sobre {C_HEROE}{target.name}{RESET}\n{C_HEROE}{target.name}{RESET} recibe daño de varios meteoritos: {C_ARTIFACT}{damage_1}{RESET} + {C_ARTIFACT}{damage_2}{RESET} + {C_ARTIFACT}{damage_3}{RESET} puntos de daño."

    def thor(self, user, target):
        damage = int(user.attack * 2 - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        user.heal(100)
        return f"¡{C_ENEMIGO}{user.name}{RESET} grita '{C_BOSS}Zousheki Shōkan: Thor{RESET}' y aparecen a su alrededor decenas de djinn de viento!\n¡Los djinn de viento se unen y mandan su energia al cielo!\n¡{C_ENEMIGO}{user.name}{RESET} alza el brazo, sonrie y al levantar la mirada ve como de una runa en el cielo cae el dios Thor, saca su mjolnir y lanza descargas electricas a todos lados\n{C_HEROE}{target.name}{RESET} recibe {C_ARTIFACT}{damage}{RESET} puntos de daño.\n{C_ENEMIGO}{user.name}{RESET} recibe algunas descargas, pero lo fortalecen.\n{C_ENEMIGO}{user.name}{RESET} recupera 100 de hp."

    def boreal(self, user, target):
        damage = int(user.attack * 2 - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        user.sp += 50
        return f"¡{C_ENEMIGO}{user.name}{RESET} grita '{C_BOSS}Zousheki Shōkan: Boreal{RESET}' y aparecen a su alrededor decenas de djinn de agua!\n¡Los djinn de agua se unen y mandan su energia al cielo!\n¡{C_ENEMIGO}{user.name}{RESET} alza el brazo, sonrie y al levantar la mirada ve... ¿una picadora de hielo?\n{C_HEROE}{target.name}{RESET} acaba congelado y recibe {C_ARTIFACT}{damage}{RESET} puntos de daño.\n{C_ENEMIGO}{user.name}{RESET} aprovecha el hielo para prepararse una copa\n{C_ENEMIGO}{user.name}{RESET} recupera 50 de sp"

class VoyASerElReyDeLosPiratas(Skill):
    def __init__(self):
        super().__init__(name="Kaizoku ou ni ore wa naru!", sp_cost=100, cooldown=8, level_required=1, hp_threshold=0.50, priority=2)

    def effect(self, user, target):
        damage = int(user.attack * 5 - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        user.attack += 10
        user.defense += 10
        return f"¡{C_ENEMIGO}{user.name}{RESET} cierra un momento los ojos mientras aparecen rayos negros a su alrededor. El aire de la sala se vuelve muy pesado\nTe mira desafiante y grita '{C_BOSS}¡Kaizoku ou ni ore wa naru!{RESET}' mientras concentra el haki del rey en su puño y se lanza contra ti\n{C_HEROE}{target.name}{RESET} sale volando y recibe {C_ARTIFACT}{damage}{RESET} puntos de daño."
    
class PorlaPaz(Skill):
    def __init__(self):
        super().__init__(name="Por la paz", sp_cost=15, cooldown=10, level_required=1, hp_threshold=1.0, priority=0)

    def effect(self, user, target):
        if user.is_boss:
            user.heal(200)
            message = f"¡{C_ENEMIGO}{user.name}{RESET} grita: {C_SKILL}¡Por la paz!{RESET} y se bebe de un trago un chupito de tequila ranchitos\n{C_ENEMIGO}{user.name}{RESET} recupera {C_HEROE}200{RESET} de hp"
            user.active_buffs.add("Por_la_paz")
        else:
            user.heal(50)
            message = f"{C_HEROE}{user.name}{RESET} grita: {C_SKILL}¡Por la paz!{RESET} y se bebe de un trago un chupito de tequila ranchitos\n{C_HEROE}{user.name}{RESET} recupera {C_HEROE}50{RESET} de hp"
        return message
    
class GiroFuego(Skill):
    def __init__(self):
        super().__init__(name="Giro de fuego", sp_cost=50, cooldown=3, level_required=1, hp_threshold=1.0, priority=0, requires_buff="Por_la_paz")

    def effect(self, user, target):
        damage = int(user.attack * 2 - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        return f"¡{C_ENEMIGO}{user.name}{RESET} comienzan a brotar llamas de su boca y ano lo que le hace girar rápidamente y formar un torbellino de fuego que se lanza sobre ti!\n{C_HEROE}{target.name}{RESET} recibe {C_ARTIFACT}{damage}{RESET} puntos de daño\n{C_ENEMIGO}{user.name}{RESET}: {C_BOSS}'No deberia haberme bebido ese chupito de ranchitos...'{RESET}"
    
class CabelloCejil(Skill):
    def __init__(self):
        super().__init__(name="Por el Poder del Cabello Cejil", sp_cost=80, cooldown=4, level_required=1, hp_threshold=0.75, priority=1, requires_buff="Por_la_paz")

    def effect(self, user, target):
        damage = int(user.attack * 3 - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        user.attack += 5
        user.defense += 5
        return f"¡{C_ENEMIGO}{user.name}{RESET} grita: {C_BOSS}'Por el Poder del Cabello Cejil'{RESET} y sus cejas comienzan a crecer y algunos pelos, como latigos, salen disparados en direccion a {C_HEROE}{target.name}{RESET}.\n{C_HEROE}{target.name}{RESET} recibe {C_ARTIFACT}{damage}{RESET} puntos de daño\n{C_ENEMIGO}{user.name}{RESET} tiene las cejas mas robustas, lo que mejora su fuerza y defensa en 5 puntos."
    
class LosMilYUnKebab(Skill):
    def __init__(self):
        super().__init__(name="Los Mil y Un Kebab", sp_cost=150, cooldown=5, level_required=1, hp_threshold=0.50, priority=2, requires_buff="Por_la_paz")

    def effect(self, user, target):
        damage = int(user.attack * 5 - target.defense)
        if damage < 1:
            damage = 0
        target.take_damage(damage)
        user.heal(100)
        return f"¡{C_ENEMIGO}{user.name}{RESET} grita: {C_BOSS}'Los Mil y un Kebab'{RESET} y empieza a reirse freneticamente mientras golpea la gema que hay en el centro de su baston.\nToda la sala empieza a temblar y las paredes de sala se bajan dejando ver cientos de asadores de kebab.\n{C_ENEMIGO}{user.name}{RESET} golpea con su baston el suelo y todas las espadas de kebab se mueven y lanzan hacia ti, ensartandote y causando {C_ARTIFACT}{damage}{RESET} puntos de daño\n{C_ENEMIGO}{user.name}{RESET} ha cogido una espada de kebab en el aire y aprovecha para comersela, recuperando {C_HEROE}100{RESET} de hp"

class Meteoro(Skill):
    def __init__(self):
        super().__init__(name="ZokusheiShokan: Meteoro", sp_cost=50, cooldown=3, level_required=1)

    def effect(self, user, target):
        skill = ZokusheiShokan()
        return skill.meteoro(user, target)

class JuicioFinal(Skill):
    def __init__(self):
        super().__init__(name="Juicio Final", sp_cost=50, cooldown=4, level_required=1)

    def effect(self, user, target):
        skill = ZokusheiShokan()
        return skill.juicio_final(user, target)

class Thor(Skill):
    def __init__(self):
        super().__init__(name="Thor", sp_cost=50, cooldown=4, level_required=1)

    def effect(self, user, target):
        skill = ZokusheiShokan()
        return skill.thor(user, target)

class Boreal(Skill):
    def __init__(self):
        super().__init__(name="Boreal", sp_cost=50, cooldown=4, level_required=1)

    def effect(self, user, target):
        skill = ZokusheiShokan()
        return skill.boreal(user, target)

class MeVoyAFumar(Skill):
    def __init__(self):
        super().__init__(name="Me voy a fumar", sp_cost=15, cooldown=4, level_required=1)

    def effect(self, user, target):
        if getattr(target, "is_boss", False):
            return f"¡{C_HEROE}{user.name}{RESET} intenta encenderse un cigarro para irse, pero la imponente presencia de {C_ENEMIGO}{target.name}{RESET} no se lo permite!"
        user.fled = True
        return f"¡{C_HEROE}{user.name}{RESET} se enciende un cigarro y se va del combate tranquilamente!"

SKILLS_PLAYER = [DisparoDeBalin, GiroHipnotico, OllaExplosiva, VozConfusa, RecitalMarxista, SiestaMaldita, InvocacionNatural, SustanciasPeligrosas, MeriendaCenaMedieval, TeknoDiario, TurraEterna, BFG9000]
