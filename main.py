   import random

import arcade

# import arcade.gui

from AttackAnimation import AttackType, AttackAnimation
from game_state import GameState

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45  # The default line height for text.


class MyGame(arcade.Window):

    PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
    PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
    COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    ATTACK_FRAME_WIDTH = 154 / 2
    ATTACK_FRAME_HEIGHT = 154 / 2

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.player = None
        self.computer = None
        self.rock = None
        self.paper = None
        self.scissors = None
        self.player_score = 0
        self.computer_score = 0
        self.computer_attack_type = None
        self.computer_attack_sprite = None
        self.player_attack_chosen = False
        self.player_won_round = None
        self.draw_round = None
        self.game_state = None
        self.gameResults = None

    def setup(self):
        """
        On initialise les variables du jeu ainsi que certains sprites. 
       """
        self.game_state = GameState.NOT_STARTED
        self.player = arcade.Sprite("Assets/faceBeard.png", 0.5, center_x=200, center_y=350)
        self.computer = arcade.Sprite("Assets/compy.png", 2.40, center_x=800, center_y=350)

        self.rock = AttackAnimation(AttackType.Rock)
        self.rock.center_x = 200
        self.rock.center_y = 150

        self.paper = AttackAnimation(AttackType.Paper)
        self.paper.center_x = 300
        self.paper.center_y = 150

        self.scissors = AttackAnimation(AttackType.Scissors)
        self.scissors.center_x = 400
        self.scissors.center_y = 150

    def victory_logic(self):
    	
    	#on verifie chaque posible situation et on analyse qui a gagné selon les regles de roche papier sciceaux
    	#on return le resultat à la fin de l'anaylyse

        if self.player_attack_chosen == AttackType.Rock and self.computer_attack_type == AttackType.Rock:
            return "Draw"
        elif self.player_attack_chosen == AttackType.Rock and self.computer_attack_type == AttackType.Paper:
            return "Loss"
        elif self.player_attack_chosen == AttackType.Rock and self.computer_attack_type == AttackType.Scissors:
            return "Win"

        if self.player_attack_chosen == AttackType.Paper and self.computer_attack_type == AttackType.Paper:
            return "Draw"
        elif self.player_attack_chosen == AttackType.Paper and self.computer_attack_type == AttackType.Scissors:
            return "Loss"
        elif self.player_attack_chosen == AttackType.Paper and self.computer_attack_type == AttackType.Rock:
            return "Win"

        if self.player_attack_chosen == AttackType.Scissors and self.computer_attack_type == AttackType.Scissors:
            return "Draw"
        elif self.player_attack_chosen == AttackType.Scissors and self.computer_attack_type == AttackType.Rock:
            return "Loss"
        elif self.player_attack_chosen == AttackType.Scissors and self.computer_attack_type == AttackType.Paper:
            return "Win"

    def draw_possible_attack(self):  
    	
    	#on desinne les "outline" des attaques possibles
        arcade.draw_rectangle_outline(
            200,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        arcade.draw_rectangle_outline(
            300,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        arcade.draw_rectangle_outline(
            400,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        arcade.draw_rectangle_outline(
            825,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))
        
        #chaque fois que le jouer choisi une attaque, on dessine l'attaque à l'ecran
        if self.player_attack_chosen == AttackType.Rock:
            self.rock.draw()
        elif self.player_attack_chosen == AttackType.Paper:
            self.paper.draw()
        elif self.player_attack_chosen == AttackType.Scissors:
            self.scissors.draw()
        else: #si aucun attaque a été choisi, on dessine toutes les attaques pour montrer les options que le jouer a pour attaquer
            self.rock.draw()
            self.paper.draw()
            self.scissors.draw()
        
    def validate_victory(self):
        
        #on "ramdomize"/ chosi l'attaque de l'ordinateur
        attack_compy = random.randint(0, 2)
        if attack_compy == 0:
            self.computer_attack_type = AttackType.Rock
            self.computer_attack_sprite = AttackAnimation(AttackType.Rock)
        elif attack_compy == 1:
            self.computer_attack_type = AttackType.Paper
            self.computer_attack_sprite = AttackAnimation(AttackType.Paper)
        elif attack_compy == 2:
            self.computer_attack_type = AttackType.Scissors
            self.computer_attack_sprite = AttackAnimation(AttackType.Scissors)

        playerResults = self.victory_logic() #on verifie le resultat en appelant la fuction victory_logic()

        if playerResults: #on set le game state à Round done après que veirifier qui a gagné
            self.game_state = GameState.ROUND_DONE
            
        #on note le resultat du ROUND selon qui a gagné 

        if playerResults == "Win": #si jouer a gagné
            self.player_score += 1
            self.gameResults = "Win"
            
        elif playerResults == "Loss": #si joueur a perdu
            self.computer_score += 1
            self.gameResults = "Loss"

        elif playerResults == "Draw": #si personne a gagné
            self.gameResults = "Draw"

        if self.player_score == 3 or self.computer_score == 3: #si quelqu'un arrive à 3 points , on change le game state à GAME_OVER
            self.game_state = GameState.GAME_OVER

    def draw_computer_attack(self): #on dessine l'attaque de l'ordi 
        if self.computer_attack_sprite:
            self.computer_attack_sprite.center_x = 825
            self.computer_attack_sprite.center_y = 150
            self.computer_attack_sprite.draw()

    def draw_text(self):
        """
       Dépendemment de l'état de jeu, afficher les instructions d'utilisation au joueur.
       """
        
        arcade.draw_text("Votre score :" + str(self.player_score),
            -220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")
        
        arcade.draw_text(" Score  de l'ordinateur :" + str(self.computer_score),
            220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")
        
        string = None

        arcade.draw_text("Votre score :" + str(self.player_score),
            -220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")
        
        arcade.draw_text(" Score de l'ordinateur :" + str(self.computer_score),
            220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")

        if self.game_state == GameState.GAME_OVER: #si le game State est GAME_Over, on reboot le jeu
            if self.player_score > self.computer_score: 
                string = "Partie gagné, Appuyer sur espace pour rejouer !"
            else:
                string = "Partie perdu, Appuyer sur espace pour rejouer !"

        elif self.game_state == GameState.NOT_STARTED: #si game state est NOT_STARTED, on attend à que le joueur commence la partie
            string = "Appuyer sur espace pour commencer la partie !"
        elif self.game_state == GameState.ROUND_ACTIVE: #si game state est ROUND_ACTIVE, on donne les options d'attaque au joueur
            string = "Clicker sur une image pour jouer !"
        elif self.game_state == GameState.ROUND_DONE: #si game state est ROUND_DONE, on affiche le resultat du "round"
            if self.gameResults == "Win":
                string = "Gagné, Appuyer sur espace pour commencer une nouvelle ronde !"
            elif self.gameResults == "Loss":
                string = "Perdu, Appuyer sur espace pour commencer une nouvelle ronde !"
            elif self.gameResults == "Draw":
                string = "Égalité ! Appuyer sur espace pour commencer une nouvelle ronde !"
        
        #on alingne le texte

        arcade.draw_text(string, 
            350,
            300,
            arcade.color.BLACK,
            20,
            width=300,
            align="center",)
        
    def on_draw(self):
        arcade.start_render()

        # Display title
        arcade.draw_text(SCREEN_TITLE,
                         0,
                         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                         arcade.color.BLACK_BEAN,
                         60,
                         width=SCREEN_WIDTH,
                         align="center")
        #on desinne les images de l'ecran
        self.player.draw()
        self.computer.draw()

        self.draw_computer_attack()

        self.draw_text()
        self.draw_possible_attack()

    def on_update(self, delta_time): #on desinne les animations des attauqes chauqe fois que le game state est ROUND ACTIVE

        if self.game_state == GameState.ROUND_ACTIVE:
            self.rock.on_update()
            self.paper.on_update()
            self.scissors.on_update()   

    def on_key_press(self, key, key_modifiers):
        """Cette méthode est invoquée à chaque fois que l'usager tape une touche
        sur le clavier."""
        if key == 32: #chaque fois que le jouer appuie la touche MOD_WINDOWS, on change le game state en raison du game state actuel
            if self.game_state == GameState.NOT_STARTED: #DE NOT STARTED à ROUND ACTIVE(debut d'une ROUND
                self.game_state = GameState.ROUND_ACTIVE

            elif self.game_state == GameState.ROUND_DONE: #Quand la ROUND est fini, on reactive on une autr ROUND
                self.game_state = GameState.ROUND_ACTIVE
                self.gameResults = None
                self.computer_attack_sprite = None
                self.player_attack_chosen = None

            elif self.game_state == GameState.GAME_OVER: #quand la parti est fini, on "reboot" le jeu
                self.game_state = GameState.ROUND_ACTIVE
                self.player_score = 0
                self.computer_score = 0
                self.computer_attack_type = None
                self.player_attack_chosen = False
                self.draw_round = None

    def on_mouse_press(self, x, y, button, key_modifiers): 
    	#on veirifie quel attaque le jouer a chosi selon où il a clicker sur l'ecran, on nite l'attque chosi

        if self.game_state == GameState.ROUND_ACTIVE:
            if self.rock.collides_with_point((x,y)):
                self.player_attack_chosen = AttackType.Rock
                self.validate_victory()

            elif self.paper.collides_with_point((x, y)):
                self.player_attack_chosen = AttackType.Paper
                self.validate_victory()

            elif self.scissors.collides_with_point((x, y)):
                self.player_attack_chosen = AttackType.Scissors
                self.validate_victory()

# on initialise  le jeu
def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
