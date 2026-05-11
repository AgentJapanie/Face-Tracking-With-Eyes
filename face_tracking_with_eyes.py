import pygame
import random
import cv2
import dlib

# Définition des constantes
pygame.init()
infos = pygame.display.Info()
screen_size = (infos.current_w, infos.current_h)

WIDTH = infos.current_w
HEIGHT = infos.current_h
SIZE = 64

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Face_Tracking")
clock = pygame.time.Clock()

#constantes pour l'eye-tracking
# Charger le détecteur de visage de dlib
detector = dlib.get_frontal_face_detector()

# Charger le fichier de prédiction pour les points caractéristiques du visage
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Charger le vidéo à partir de la webcam
cap = cv2.VideoCapture(0)

# Obtenir la résolution de la caméra
WIDTHCAM = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
HEIGHTCAM = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#print(WIDTHCAM, HEIGHTCAM)

class Yeux:
    def __init__(self, hauteur:int, largeur:int, couleur:tuple, pos:list) -> None:
        self.hauteur = hauteur
        self.hauteur_max = hauteur
        self.largeur = largeur
        self.couleur = couleur
        self.pos = pos
        self.posOeilG = [pos[0]-(self.largeur+2),pos[1]+self.hauteur_max/2]
        self.posOeilD = [pos[0]+(largeur/2),pos[1]+self.hauteur_max/2]
        self.is_blinking = False
        self.stepBlink = False
        self.debug = False
        self.is_emotional = False
        self.emotion = "Neutral"

    def update_pos(self, pos) -> None:
        self.pos = [pos[0], pos[1]]
        self.posOeilG = [pos[0]-(self.largeur+2),pos[1]+self.hauteur_max/2]
        self.posOeilD = [pos[0]+(self.largeur/2),pos[1]+self.hauteur_max/2]

    def debug_pixels(self) -> None:
        pygame.draw.rect(screen, (255, 0, 0), (self.pos[0] * SIZE, self.pos[1] * SIZE, SIZE, SIZE))
        pygame.draw.rect(screen, (0, 255, 0), (self.posOeilG[0] * SIZE, self.posOeilG[1] * SIZE, SIZE, SIZE))
        pygame.draw.rect(screen, (0, 0, 255), (self.posOeilD[0] * SIZE, self.posOeilD[1] * SIZE, SIZE, SIZE))

    #Emotions: 
    #   -Neutre
    def neutral_eyes(self) -> None:
        pygame.draw.rect(screen, self.couleur, (self.posOeilG[0] * SIZE, self.posOeilG[1] * SIZE, self.largeur * SIZE, -self.hauteur * SIZE), border_radius=int(SIZE*1.5625))
        pygame.draw.rect(screen, self.couleur, (self.posOeilD[0] * SIZE, self.posOeilD[1] * SIZE, self.largeur * SIZE, -self.hauteur * SIZE), border_radius=int(SIZE*1.5625))

    def blink(self) -> None:
        if self.is_blinking == True:
            if self.stepBlink == True:
                self.hauteur += 0.9
                if self.hauteur >= self.hauteur_max:
                    self.hauteur = self.hauteur_max
                    self.is_blinking = False
                    self.stepBlink = False
            else:
                self.hauteur -= 0.9
                if self.hauteur <= 1:
                    self.stepBlink = True
            
        elif self.is_blinking == False:
            nbr = random.randint(0,1000)
            if nbr < 70:
                self.is_blinking = True

    def go_to(self, position) -> None: 
        if self.pos[0] < position[0]+1 and self.pos[0] > position[0]-1:
            pass
        elif self.pos[0] > position[0]:
            self.pos[0] -= 0.5
        elif self.pos[0] < position[0]:
            self.pos[0] += 0.5
        
        if self.pos[1] < position[1]+1 and self.pos[1] > position[1]-1:
            pass
        elif self.pos[1] > position[1]:
            self.pos[1] -= 0.5
        elif self.pos[1] < position[1]:
            self.pos[1] += 0.5


        self.update_pos(self.pos)

             

yeux = Yeux(8, 6, (255,100,0), [WIDTH/SIZE/2,HEIGHT/SIZE/2])


def draw():
    global SIZE
    screen.fill((0, 0, 0))
    
    yeux.neutral_eyes()

    pygame.display.flip()

def leave():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        # Libérer la capture de la webcam
        cap.release()
        exit()

def get_face_position():
    global SIZE, WIDTH, HEIGHT, WIDTHCAM, HEIGHTCAM
    # Lire une image à partir de la webcam
    ret, frame = cap.read()
    
    if ret:
        # Inverser l'image horizontalement pour créer un effet miroir
        frame = cv2.flip(frame, 1)
        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Détecter les visages dans l'image
        faces = detector(gray)
        
        # Mettre à jour la position des yeux en fonction du premier visage détecté
        if faces:
        
            # Dessiner un rectangle autour de chaque visage détecté
            for face in faces:
                x, y = face.left(), face.top()
                w, h = face.width(), face.height()   
                # Calculer les coordonnées du centre du rectangle
                center_x = x + w // 2
                center_y = y + h // 2
                yeux.go_to([(center_x*(WIDTH/WIDTHCAM)/SIZE), center_y*(HEIGHT/HEIGHTCAM)/SIZE])
    
         

def update():
    get_face_position()
    leave()
    
#Boucle principale
running = True
while running:
    update()
    draw()
    clock.tick(20)




