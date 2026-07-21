from skills import EraTanFacil, SKILLS_PLAYER, JuicioFinal, Thor, Boreal, MeVoyAFumar, Meteoro, PorlaPaz
import random
from ui import imprimir_texto, mostrar_titulo_gigante, C_HEROE, C_ENEMIGO, C_ARTIFACT, C_SISTEMA, C_SKILL, C_BOSS, C_ITEM, RESET


class Item:
    def __init__(self, name, heal_hp=0, heal_sp=0, price=0, description=""):
        self.name = name
        self.heal_hp = heal_hp
        self.heal_sp = heal_sp
        self.price = price
        self.description = description

    def use(self, player):
        player.heal(self.heal_hp)
        player.sp = min(player.sp + self.heal_sp, player.sp_max)
        return f"{C_HEROE}{player.name}{RESET} usa {C_ITEM}{self.name}{RESET} y recupera {C_ARTIFACT}{self.heal_hp}{RESET} HP y {C_ARTIFACT}{self.heal_sp}{RESET} SP."
    
class EstrellaLevante(Item):
    def __init__(self):
        super().__init__(name="Quinto de Estrella", price=20, description="Un quinto de la mejor cerveza murciana.\nRecupera 50% de SP.")
        
    def use(self, player):
        sp_amount = int(player.sp_max * 0.5)
        player.sp = min(player.sp + sp_amount, player.sp_max)
        return f"{C_HEROE}{player.name}{RESET} se bebe un {C_ITEM}{self.name}{RESET} y recupera {C_ARTIFACT}{sp_amount}{RESET} SP."
    
class Guldendraak(Item):
    def __init__(self):
        super().__init__(name="Pinta de Gulden Draak", price=40, description="Una pinta de la cerveza mas potente.\nRecupera 100% de SP.")

    def use(self, player):
        sp_amount = int(player.sp_max)
        player.sp = min(player.sp + sp_amount, player.sp_max)
        return f"{C_HEROE}{player.name}{RESET} se bebe una {C_ITEM}{self.name}{RESET} y recupera {C_ARTIFACT}{sp_amount}{RESET} SP."
    
class Fricandela(Item):
    def __init__(self):
        super().__init__(name="Fricandela Especial", price=20, description="Una salchicha belga con un acompañamiento muy especial.\nRecupera 50% de HP.")

    def use(self, player):
        hp_amount = int(player.hp_max * 0.5)
        player.heal(hp_amount)
        return f"{C_HEROE}{player.name}{RESET} se come una {C_ITEM}{self.name}{RESET} y recupera {C_ARTIFACT}{hp_amount}{RESET} HP."

class Mexicano(Item):
    def __init__(self):
        super().__init__(name="Mexicano", price=40, description="Un trozo de carne especiada, bueno que te cagas.\nRecupera 100% de HP.")

    def use(self, player):
        hp_amount = int(player.hp_max)
        player.heal(hp_amount)
        return f"{C_HEROE}{player.name}{RESET} se come un {C_ITEM}{self.name}{RESET} y recupera {C_ARTIFACT}{hp_amount}{RESET} HP."

class MenuRolloMixto(Item):
    def __init__(self):
        super().__init__(name="Menu de Rollo Mixto", price=70, description="Un delicioso menu rollo mixto con patatas y bebida\nRecupera 50% de HP y 50% de SP")

    def use(self, player):
        hp_amount = int(player.hp_max * 0.5)
        player.heal(hp_amount)
        sp_amount = int(player.sp_max * 0.5)
        player.sp = min(player.sp + sp_amount, player.sp_max)
        return f"{C_HEROE}{player.name}{RESET} se toma un {C_ITEM}{self.name}{RESET} y recupera {C_ARTIFACT}{hp_amount}{RESET} HP y {C_ARTIFACT}{sp_amount}{RESET} SP."

class MenuFritaten(Item):
    def __init__(self):
        super().__init__(name="Menu del Fritaten", price=100, description="Un menu completo del Fritaten con patatas y bebida\nRecupera 100% de HP y 100% de SP")

    def use(self, player):
        hp_amount = int(player.hp_max)
        player.heal(hp_amount)
        sp_amount = int(player.sp_max)
        player.sp = min(player.sp + sp_amount, player.sp_max)
        return f"{C_HEROE}{player.name}{RESET} se toma un {C_ITEM}{self.name}{RESET} y recupera {C_ARTIFACT}{hp_amount}{RESET} HP y {C_ARTIFACT}{sp_amount}{RESET} SP."

class Artifact:
    def __init__(self, name, description, active_once=False, special=False, trigger_mode="passive", price=0):
        self.name = name
        self.description = description
        self.active_once = active_once
        self.special = special
        self.trigger_mode = trigger_mode
        self.price = price

    def apply_passive(self, player, enemy):
        pass

    def on_combat_start(self, player, enemy):
        return None

class AcreditacionMLP(Artifact):
    def __init__(self):
        super().__init__(name="Acreditacion de la MLP", description="Acreditacion de la aclamada Murcia Lan Party\nDa tanto Hype que sube todas tus estadisticas 5 puntos", active_once=True, price=45)

    def apply_passive(self, player, enemy):
        player.hp_max += 5
        player.sp_max += 5
        player.attack += 5
        player.defense += 5
        return f"{C_HEROE}{player.name}{RESET} siente el poder de la {C_ARTIFACT}MLP{RESET} y sus estadisticas aumentan 5 puntos."

class SteamMachine(Artifact):
    def __init__(self):
        super().__init__(name="SteamMachine", description="La ultima maravilla tecnologica de Gabe Newell\nAumenta tu potencia de juego, aumentando tus estadisticas 15 puntos", active_once=True, price=1039)

    def apply_passive(self, player, enemy):
        player.hp_max += 15
        player.sp_max += 15
        player.attack += 15
        player.defense += 15
        return f"{C_HEROE}{player.name}{RESET} enchufa la {C_ARTIFACT}{self.name}{RESET} y sus estadisticas aumentan 15 puntos."

class NintendoSwitch2(Artifact):
    def __init__(self):
        super().__init__(name="Nintendo Switch 2", description="Ultima consola de Nintendo\nAumenta tu potencia de juego, aumentando tus estadisticas 10 puntos", active_once=True, price=540)

    def apply_passive(self, player, enemy):
        player.hp_max += 10
        player.sp_max += 10
        player.attack += 10
        player.defense += 10
        return f"{C_HEROE}{player.name}{RESET} tiene el morro ardiendo con su nueva {C_ARTIFACT}{self.name}{RESET} y sus estadisticas aumentan 10 puntos."

class RedDeVoley(Artifact):
    def __init__(self):
        super().__init__(name="Red de Voley", description="Red de voley para jugar con los colegas\nSiempre acaba montandose mal, asi que a la minima acaba algun enemigo enredado.", price=80)

    def apply_passive(self, player, enemy):
        if random.random() < 0.25:
            enemy.lose_turn = True
            return f"{C_ENEMIGO}{enemy.name}{RESET} se ha enredado en la {C_ARTIFACT}{self.name}{RESET}, pierde su turno."

class Ocarina(Artifact):
    def __init__(self):
        super().__init__(name="Ocarina", description="Una Ocarina magica\nEs bastante dificil de tocar, pero al llevarla sientes cierto poder magico", active_once=True, price=30)

    def apply_passive(self, player, enemy):
        player.sp_max += 25
        return f"{C_HEROE}{player.name}{RESET} siente el poder de la {C_ARTIFACT}{self.name}{RESET} y sus SP aumenta 25 puntos."

class Trifuerza(Artifact):
    def __init__(self):
        super().__init__(name="Trifuerza", description="La legendaria Trifuerza\nAl obtenerla, sientes un poder increible. Aumentan tus estadisticas en 30 puntos", active_once=True, special=True, price=333)

    def apply_passive(self, player, enemy):
        player.hp_max += 30
        player.sp_max += 30
        player.attack += 30
        player.defense += 30
        return f"{C_HEROE}{player.name}{RESET} siente el poder de la {C_ARTIFACT}{self.name}{RESET} y sus estadisticas aumentan 30 puntos."

class Violin(Artifact):
    def __init__(self):
        super().__init__(name="Violin", description="Un violin magico\nCada vez que pierdes turno, aprovechas para tocarselo un poco a tu señora", price=50)

    def apply_passive(self, player, enemy):
        if player.lose_turn:
            player.heal(int(player.hp_max * 0.1))
            player.sp = min(player.sp + int(player.sp_max * 0.1), player.sp_max)
            return f"{C_HEROE}{player.name}{RESET} aprovecha su turno perdido para tocar el {C_ARTIFACT}{self.name}{RESET} y recupera {int(player.hp_max * 0.1)} HP y {int(player.sp_max * 0.1)} SP"
        
class SuperEscopeta(Artifact):
    def __init__(self):
        super().__init__(name="Super Escopeta", description="Una escopeta de doble cañon\nAumenta tu ataque en 15 puntos", active_once=True, price=70)

    def apply_passive(self, player, enemy):
        player.attack += 15
        return f"{C_HEROE}{player.name}{RESET} carga la {C_ARTIFACT}{self.name}{RESET} y sus ataque aumenta 15 puntos."

class Cortana(Artifact):
    def __init__(self):
        super().__init__(name="Cortana", description="Una IA de ultima generacion, capaz de anticipar cualquier movimiento enemigo\nAumenta tu defensa en 10 puntos", active_once=True, price=70)

    def apply_passive(self, player, enemy):
        player.defense += 10
        return f"{C_HEROE}{player.name}{RESET} se equipa a {C_ARTIFACT}{self.name}{RESET} y su defensa aumenta 10 puntos."

class PiedraDePsinergia(Artifact):
    def __init__(self):
        super().__init__(name="Piedra de Psinergia", description="Una piedra que aumenta tu poder magico\nAumenta tu SP en 50 puntos", active_once=True, price=40)

    def apply_passive(self, player, enemy):
        player.sp_max += 50
        return f"{C_HEROE}{player.name}{RESET} siente el poder de la {C_ARTIFACT}{self.name}{RESET} y sus SP aumenta 50 puntos."

class PiedraBruja(Artifact):
    def __init__(self):
        super().__init__(name="Piedra Bruja", description="Una piedra verde brillante, da muy mal rollo\nMucho tu SP, ataque y defensa a costa de tu salud", active_once=True, price=666)

    def apply_passive(self, player, enemy):
        player.attack += 20
        player.defense += 10
        player.sp_max += 100
        player.hp_max -= 30
        if player.hp > player.hp_max:
            player.hp = player.hp_max
        return f"{C_HEROE}{player.name}{RESET} siente el poder de la {C_ARTIFACT}{self.name}{RESET} y sus SP aumenta 100 puntos, su ataque 20 puntos y su defensa 10 puntos, pero sus HP maximos disminuyen 30 puntos."

class TomoDeOnePiece(Artifact):
    def __init__(self):
        super().__init__(name="Tomo de One Piece", description="Un tomo del manga de One Piece, ¡Como mola!\nAumenta tu HP y SP en 20 puntos y tu ataque en 10 puntos", active_once=True, price=50)

    def apply_passive(self, player, enemy):
        player.hp_max += 20
        player.sp_max += 20
        player.attack += 10
        return f"Al leer el Tomo de One Piece, {C_HEROE}{player.name}{RESET} se inspira y aumenta su HP y SP en 20 puntos y su ataque aumenta 10 puntos."

class CartaDragonBlancoOjosAzules(Artifact):
    def __init__(self):
        super().__init__(name="Carta del Dragon Blanco de Ojos Azules", description="Una carta del Dragon Blanco de Ojos Azules de Yu-Gi-Oh! que da mucho poder\nAumenta tu ataque en 20 puntos y tu HP en 50 puntos", active_once=True, price=80)

    def apply_passive(self, player, enemy):
        player.attack += 20
        player.hp_max += 50
        return f"Invoca el poder del poderoso Dragon Blanco de Ojos Azules, {C_HEROE}{player.name}{RESET} aumenta su HP y ataque en 50 y 20 puntos respectivamente"

class CartaMagoOscuro(Artifact):
    def __init__(self):
        super().__init__(name="Carta del Mago Oscuro", description="Una carta del mago oscuro de Yu-Gi-Oh! que da mucho poder\nAumenta tu SP en 50 puntos y tu ataque en 10 puntos", active_once=True, price=80)

    def apply_passive(self, player, enemy):
        player.sp_max += 50
        player.attack += 10
        return f"{C_HEROE}{player.name}{RESET} invoca el poder del Mago Oscuro y aumenta su SP y ataque en 50 y 10 puntos respectivamente"

class GranNispero(Artifact):
    def __init__(self):
        super().__init__(
            name="El Gran Níspero",
            description="Un gran níspero nispero brillante, símbolo del legendario clan ECDN\nTe da una vida extra: si mueres, revives con HP y SP al máximo.",
            trigger_mode="on_death",
            price=1000,
        )
        self.revives_on_death = True
        self.used = False

    def apply_passive(self, player, enemy):
        if self.revives_on_death and not self.used:
            self.used = True
            self.revives_on_death = False
            player.hp = player.hp_max
            player.sp = player.sp_max
            return f"\n🌟 ¡La luz del clan ECDN resuena! {C_HEROE}{player.name}{RESET} cae en combate, pero el {C_ARTIFACT}{self.name}{RESET} se consume y le devuelve a la vida con todo su poder.\n"

class AlbumChopeaPepeda(Artifact):
    def __init__(self):
        super().__init__(
            name="Album Chopea Pepeda",
            description="Un album de fotos de Pepeda, el legendario Gamer, Lanero, One Piece Teorico, Podcaster, Streamer, Mastodonte, Sultan, Destructor de Mundos...\nHay grandes momentos y enseñanzas en sus paginas, duplica la experiencia obtenida en combate",
            price=250,
            active_once=True
        )
    
    def apply_passive(self, player, enemy):
        player.experience_multiplier = 2
        return f"{C_HEROE}{player.name}{RESET} siente el poder del {C_ARTIFACT}{self.name}{RESET} y duplica la experiencia obtenida en combate"

class DjinnDeFuego(Artifact):
    def __init__(self):
        super().__init__(
            name="Djinn de Fuego",
            description="Un Djinn del elemento fuego\n El jugador puede usar la skill ZokusheiShokan: Meteoro.\n Aumenta su ataque en 10 puntos.",
            active_once=True,
            price=150
        )

    def apply_passive(self, player, enemy):
        player.attack += 10
        skill = Meteoro()
        player.skills.append(skill)
        return f"{C_HEROE}{player.name}{RESET} ha aprendido la habilidad '{C_SKILL}ZokusheiShokan: Meteoro{RESET}'."

class DjinnDeTierra(Artifact):
    def __init__(self):
        super().__init__(
            name="Djinn de Tierra",
            description="Un Djinn del elemento tierra\nEl jugador puede usar la skill ZokusheiShokan: Juicio Final.\n Aumenta su HP maximo en 50 puntos.",
            price=150,
            active_once=True,
        )

    def apply_passive(self, player, enemy):
        player.hp_max += 50
        skill = JuicioFinal()
        player.skills.append(skill)
        return f"{C_HEROE}{player.name}{RESET} ha aprendido la habilidad '{C_SKILL}ZokusheiShokan: Juicio Final{RESET}'."

class DjinnDeViento(Artifact):
    def __init__(self):
        super().__init__(
            name="Djinn de Viento",
            description="Un Djinn del elemento viento\nEl jugador puede usar la skill ZokusheiShokan: Thor.\n Aumenta su defensa en 10 puntos.",
            price=150,
            active_once=True
        )

    def apply_passive(self, player, enemy):
        player.defense += 10
        skill = Thor()
        player.skills.append(skill)
        return f"{C_HEROE}{player.name}{RESET} ha aprendido la habilidad '{C_SKILL}ZokusheiShokan: Thor{RESET}'."
    
class DjinnDeAgua(Artifact):
    def __init__(self):
        super().__init__(
            name="Djinn de Agua",
            description="Un Djinn del elemento agua\nEl jugador puede usar la skill ZokusheiShokan: Boreal.\n Aumenta su SP maximo en 50 puntos.",
            price=150,
            active_once=True,
        )

    def apply_passive(self, player, enemy):
        player.sp_max += 50
        skill = Boreal()
        player.skills.append(skill)
        return f"{C_HEROE}{player.name}{RESET} ha aprendido la habilidad '{C_SKILL}ZokusheiShokan: Boreal{RESET}'."

class TequilaRanchitos(Artifact):
    def __init__(self):
        super().__init__(
            name="Tequila Ranchitos",
            description="Un tequila de la marca Ranchitos, el mejor tequila del mundo, si lo que buscas es una muerte larga y dolorosa\nCuriosamente, aunque te este destruyendo por dentro, sientes un subidon al beberlo\n Obtienes la habilidad 'Por la Paz'",
            active_once=True,
            price=50
        )

    def apply_passive(self, player, enemy):
        skill = PorlaPaz()
        player.skills.append(skill)
        return f"{C_HEROE}{player.name}{RESET} ha aprendido la habilidad '{C_SKILL}Por la paz{RESET}'."
    
class AlmohadaDeYuri(Artifact):
    def __init__(self):
        super().__init__(
            name="Almohada de Yuri",
            description="La siempre confiable Almohada de Yuri, para las siestas mas duras y placenteras\nRecupera cada turno 10% de HP y 10% de SP",
            price=100,
            trigger_mode="turn_start"
        )
    
    def apply_passive(self, player, enemy):
        player.heal(int(player.hp_max * 0.05))
        player.sp = min(player.sp + int(player.sp_max * 0.05), player.sp_max)
        return f"{C_HEROE}{player.name}{RESET} se siente descansado gracias a la {C_ARTIFACT}{self.name}{RESET}, recupera {C_HEROE}{int(player.hp_max * 0.05)}{RESET} HP y {C_HEROE}{int(player.sp_max * 0.05)}{RESET} SP."
    
class PistolonDeMatabufalez(Artifact):
    def __init__(self):
        super().__init__(
            name="Pistolon de Matabufalez",
            description="La temida arma de Matabufalez, huyen de ella tanto amigos como enemigos\nTras realizar un ataque existe la posibilidad que dispare con ella.",
            price=150,
            trigger_mode="attack"
        )
    
    def apply_passive(self, player, enemy):
        if random.random() < 0.5:
            damage = int(max(0, player.attack * 1.5 - enemy.defense))
            enemy.take_damage(damage)
            return f"{C_HEROE}{player.name}{RESET} dispara con el {C_ARTIFACT}{self.name}{RESET} y causa {damage} de daño a {C_ENEMIGO}{enemy.name}{RESET}."
        
class RunasDeFreakmaster(Artifact):
    def __init__(self):
        super().__init__(
            name="Runas de Freakmaster",
            description="Unas runas que predicen el futuro.\nNo siempre aciertan, pero si lo hacen, evitan el daño ese turno.",
            price=150,
            trigger_mode="turn_start"
        )

    def apply_passive(self, player, enemy):
        if random.random() < 0.3:
            player.avoid_damage = True
            return f"Las {C_ARTIFACT}{self.name}{RESET} brillan y mandan un aviso del proximo movimiento del enemigo a la mente de {C_HEROE}{player.name}{RESET}\n {C_HEROE}{player.name}{RESET} evita el daño de este turno."
        
class BaflesDeSami(Artifact):
    def __init__(self):
        super().__init__(
            name="Bafles de Sami",
            description="Unos bafles que resuenan con el poder acumulado de tus artefactos.\n Al inicio del combate, ganas +5 HP, +5 SP, +0.5 ATQ y +0.5 DEF por cada artefacto que poseas.",
            price=150,
            trigger_mode="combat_start"
        )
        self.triggered = False
    
    def on_combat_start(self, player, enemy):
        if self.triggered or enemy is None:
            return None
        self.triggered = True
        cantidad_artefactos = len(player.artifacts)
        bono_max = int(cantidad_artefactos * 5)
        bono_stats = int(cantidad_artefactos / 2)
        player.hp_max += bono_max
        player.sp_max += bono_max
        player.hp += bono_max
        player.sp += bono_max
        player.attack += bono_stats
        player.defense += bono_stats
        return f"🔊 El ritmo de los {C_ARTIFACT}{self.name}{RESET} resuena con tus {C_ITEM}{cantidad_artefactos}{RESET} artefactos. ¡{C_HEROE}{player.name}{RESET} aumenta hasta {bono_max} HP/SP y {bono_stats} ATQ/DEF!"

class LlaveEspada(Artifact):
    def __init__(self):
        super().__init__(
            name="Llave Espada",
            description="La llave espada, un arma legendaria que blanden los elegidos.\nAumenta tu ataque en 50 puntos y tu HP y SP en 100 puntos",
            price=200,
            active_once=True
        )
    
    def apply_passive(self, player, enemy):
        player.attack += 25
        player.sp_max += 50
        player.hp_max += 50
        return f"{C_HEROE}{player.name}{RESET} blande la {C_ARTIFACT}{self.name}{RESET} y aumenta su ataque en 25 puntos y su HP y SP en 50 puntos."

class PaqueteDeTabaco(Artifact):
    def __init__(self):
        super().__init__(
            name="Paquete de Tabaco",
            description="Un paquete de tabaco\nObtienes la habilidad 'Me voy a fumar' y tu defensa aumenta en 5 puntos.",
            price=50,
            active_once=True
        )

    def apply_passive(self, player, enemy):
        player.defense += 5
        skill = MeVoyAFumar()
        player.skills.append(skill)
        return f"{player.name} se coloca el paquete en el bolsillo de la camisa y aprende la habilidad 'Me voy a fumar'."

class Clackers(Artifact):
    def __init__(self):
        super().__init__(
            name="Clackers",
            description="Los clasicos clackers, ideales para romper narices y causar un gran daño a los enemigos",
            price=100,
        )
    
    def apply_passive(self, player, enemy):
        player.attack += 5
        return f"{C_HEROE}{player.name}{RESET} golpea con los {C_ARTIFACT}{self.name}{RESET} y aumenta su ataque en 5 puntos."

class TrajeZeta(Artifact):
    def __init__(self):
        super().__init__(
            name="Traje Zeta",
            description="Un traje usado por un gran heroe\nAl comienzo del combate multiplica por dos tu ataque y defensa",
            price=150,
            trigger_mode="combat_start"
        )
        self.triggered = False
    
    def on_combat_start(self, player, enemy):
        if self.triggered or enemy is None:
            return None
        self.triggered = True
        player.attack *= 2
        player.defense *= 2
        return f"{C_HEROE}{player.name}{RESET} viste el {C_ARTIFACT}{self.name}{RESET} y duplica su ataque y defensa durante este combate."

class CalcetinSucio(Artifact):
    def __init__(self):
        super().__init__(
            name="Calcetin Sucio",
            description="Un calcetin apestoso, usado durante una larga jornada de Verano en Murcia\nSu olor es tan intenso, que reduce un 25% la vida del enemigo al iniciar el combate",
            price= 200,
            trigger_mode="combat_start"
        )
        self.triggered = False
    
    def on_combat_start(self, player, enemy):
        if self.triggered or enemy is None or not enemy.is_alive():
            return None
        self.triggered = True
        enemy.hp = max(1, int(enemy.hp * 0.75))
        return f"{C_HEROE}{player.name}{RESET} lanza a la cara de {C_ENEMIGO}{enemy.name}{RESET} el {C_ARTIFACT}{self.name}{RESET} y reduce su vida en un 25%."

class FiguraStandCrazyDiamond(Artifact):
    def __init__(self):
        super().__init__(
            name="Figura de Crazy Diamond",
            description="Una figura de coleccionismo de Crazy Diamond\nNo entiendes porque pero te hace sentir mejor",
            price=250,
            trigger_mode="combat_start"
        )
        self.triggered = False
    
    def on_combat_start(self, player, enemy):
        if self.triggered or enemy is None:
            return None
        self.triggered = True
        heal_amount = int(player.hp_max * 0.30)
        player.hp = min(player.hp + heal_amount, player.hp_max)
        return f"{C_HEROE}{player.name}{RESET} admira la {C_ARTIFACT}{self.name}{RESET} y siente sus energias volver, {C_HEROE}{player.name}{RESET} recupera {heal_amount} HP."

class TartaShawarma(Artifact):
    def __init__(self):
        super().__init__(
            name="Tarta Shawarma",
            description="Una tarta de shawarma, la especialidad de Alan\nrecupera un 10% de la vida maxima cada turno",
            price=555,
            trigger_mode="turn_start"
        )
    
    def apply_passive(self, player, enemy):
        heal_amount = int(player.hp_max * 0.10)
        player.hp = min(player.hp + heal_amount, player.hp_max)
        return f"{C_HEROE}{player.name}{RESET} come la {C_ARTIFACT}{self.name}{RESET} y recupera {C_HEROE}{heal_amount}{RESET} HP."

class PorroDeLasTeorias(Artifact):
    def __init__(self):
        super().__init__(
            name="Porro de las Teorías",
            description="Un porro con el que cada calada te ilumina con una nueva teoría loca\nTeorizas sobre ti mismo y obtienes una habilidad aleatoria nueva",
            active_once=True,
            price=100
        )

    def apply_passive(self, player, enemy):
        habilidades_actuales = [type(skill) for skill in player.skills]
        habilidades_futuras = getattr(player, "habilidades_futuras", []) 
        habilidades_disponibles = [
            skill_class for skill_class in SKILLS_PLAYER
            if skill_class not in habilidades_actuales and skill_class not in habilidades_futuras
        ]
        if not habilidades_disponibles:
            return f"{player.name} fuma el {self.name}, ¡pero su mente ya está en un plano superior y no hay nada nuevo que pueda aprender!"
        skill_class = random.choice(habilidades_disponibles)
        new_skill = skill_class()
        new_skill.level_required = 0
        player.skills.append(new_skill)
        return f"{player.name} fuma de las teorías y ha aprendido la nueva habilidad '{new_skill.name}'."

class ManoDeMidas(Artifact):
    def __init__(self):
        super().__init__(
            name="Mano de Midas",
            description="Una mano dorada que atrae la fortuna\nDuplica el oro obtenido de los enemigos",
            price=300,
            active_once=True
        )
    
    def apply_passive(self, player, enemy):
        player.gold_multiplier *= 2
        return f"{C_HEROE}{player.name}{RESET} coge la {C_ARTIFACT}{self.name}{RESET} y duplica el oro que obtiene de los enemigos."

class BastonDeAghanim(Artifact):
    def __init__(self):
        super().__init__(
            name="Cetro de Aghanim",
            description="Un cetro que potencia tus habilidades\nObtiene la habilidad 'ERA TAN FACIL",
            price=300,
            active_once=True
        )
    
    def apply_passive(self, player, enemy):
        skill = EraTanFacil()
        player.skills.append(skill)
        return f"{C_HEROE}{player.name}{RESET} empuña el {C_ARTIFACT}{self.name}{RESET} y obtiene la habilidad '{skill.name}'."

def get_all_items():
    """Devuelve una lista con todas las clases de items disponibles"""
    return [Fricandela, Mexicano, EstrellaLevante, Guldendraak, MenuRolloMixto, MenuFritaten]

def get_all_artifacts():
    """Devuelve una lista con todas las clases de artefactos disponibles"""
    return [
        AcreditacionMLP, SteamMachine, NintendoSwitch2, RedDeVoley, Ocarina, Trifuerza,
        Violin, SuperEscopeta, Cortana, PiedraDePsinergia, PiedraBruja, TomoDeOnePiece,
        CartaDragonBlancoOjosAzules, CartaMagoOscuro, GranNispero, CaretaDePepeda,
        AlbumChopeaPepeda, DjinnDeFuego, DjinnDeTierra, DjinnDeViento, DjinnDeAgua,
        PorroDeLasTeorias, CalcetinSucio, TrajeZeta, Clackers, FiguraStandCrazyDiamond,
        TartaShawarma, PaqueteDeTabaco, LlaveEspada, BaflesDeSami, RunasDeFreakmaster, AlmohadaDeYuri,
        PistolonDeMatabufalez, TequilaRanchitos, ManoDeMidas, BastonDeAghanim
    ]

def grant_random_reward(player):
    reward_items = get_all_items()
    if not reward_items:
        return f"{C_HEROE}{player.name}{RESET} rebusca, pero extrañamente no encuentra nada de valor."
    reward_artifacts = [c for c in get_all_artifacts() if not any(isinstance(a, c) for a in player.artifacts)]
    if random.random() < 0.75 or not reward_artifacts:
        reward = random.choice(reward_items)()
        player.add_item(reward)
        return f"{C_HEROE}{player.name}{RESET} recibe un premio: {C_ITEM}{reward.name}{RESET}"
    reward = random.choice(reward_artifacts)()
    return player.add_artifact(reward)

class CaretaDePepeda(Artifact):
    def __init__(self):
        super().__init__(
            name="Careta de Pepeda",
            description="Una careta de Pepeda, el legendario Gamer, Lanero, One Piece Teorico, Podcaster, Streamer, Mastodonte, Sultan, Destructor de Mundos...\nSus siervos pueden confundirte con el y ofrecer un tributo en vez de pelear",
            trigger_mode="combat_start",
            price=500
        )
        self.triggered = False

    def on_combat_start(self, player, enemy):
        if self.triggered or enemy is None or getattr(enemy, "is_boss", False):
            return None
        self.triggered = True
        if random.random() < 0.3:
            enemy.hp = 0
            reward_message = grant_random_reward(player)
            enemy.loot_items = []
            enemy.loot_artifacts = []
            return f"{C_ENEMIGO}{enemy.name}{RESET} confunde a {C_HEROE}{player.name}{RESET} con Pepeda gracias a la {C_ARTIFACT}{self.name}{RESET} y le ofrece un tributo, ¡{C_ENEMIGO}{enemy.name}{RESET} ha sido derrotado!\n{reward_message}"
        return None
