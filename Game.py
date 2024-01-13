import pygame
import random
import math
from pygame import mixer

#! Inicializo PyGame
pygame.init() 

#! Establezco el tamaño de la pantalla
pantalla = pygame.display.set_mode((800, 600)) 

#! Titulo, icono y fondos
pygame.display.set_caption("Submarinos y pulpos")
icono = pygame.image.load("images/submarino.png")
pygame.display.set_icon(icono) #? Defino el icono del titulo
fondo = pygame.image.load("images/Fondo-mar.jpg")

#! Agregar sonido
mixer.music.load("assets/MusicaFondo.mp3")
mixer.music.set_volume(0.3) #? numero del 0 al 1 para indicar el volumen
mixer.music.play(-1) #? -1 para que suene infinito

#! Variables Jugador - Submarino
submarino_img = pygame.image.load("images/submarino64px.png") #? Guardo el icono en una variable
submarino_x = 10
submarino_y = 268
submarino_y_cambio = 0

#! Variables Enemigo - Pulpo
enemigo_img = []
enemigo_x = []
enemigo_y = []
enemigo_y_cambio = []
enemigo_x_cambio = []
cantidad_enemigos = 7

#? Loop para asignar enemigos
for enemigo in range(cantidad_enemigos):
    enemigo_img.append(pygame.image.load("images/pulpo.png"))
    enemigo_x.append(random.randint(500, 736))
    enemigo_y.append(random.randint(0, 536))
    enemigo_y_cambio.append(0.27)
    enemigo_x_cambio.append(-50)

#! Variables de la Bala
bala_img = pygame.image.load("images/torpedo.png")
bala_x = submarino_x + 64 # Le doy el valor actual del submarino mas el tamaño del mismo
bala_y = 0
bala_y_cambio = 0
bala_x_cambio = 1.7
bala_visible = False

#! Varibles del Puntaje
puntaje = 0
fuente = pygame.font.Font("assets/orange juice 2.0.ttf", 32)
puntaje_x = 10
puntaje_y = 10

#! Variables Game Over
fuente_grande = pygame.font.Font("assets/orange juice 2.0.ttf", 64)
game_over = False

def texto_final():
    mi_fuente_final = fuente_grande.render("GAME OVER", True, (255, 0, 0))
    pantalla.blit(mi_fuente_final, (230, 200))

#! Variables Start Game
def texto_inicial():
    mi_fuente_iniciar = fuente_grande.render("PRESS ENTER TO START", True, (240, 240, 0))
    pantalla.blit(mi_fuente_iniciar, (110, 200))

#! Funcion para mostrar Puntaje
def mostrar_puntaje(x, y):
    tabla = fuente.render(f"Puntaje: {puntaje}", True, (0, 0, 255))
    pantalla.blit(tabla, (x, y))

#! Funcion del Jugador - Submarino
def submarino(x, y): #? Defino la posicion del jugador
    pantalla.blit(submarino_img, (x, y))

#! Funcion del Enemigo - Pulpo
def enemigo(x, y, i): #? Defino la posicion de los enemigos
    pantalla.blit(enemigo_img[i], (x, y))

#! Funcion disparar bala
def disparar_bala(x, y): #? Defino la posicion de la bala
    global bala_visible
    bala_visible = True
    pantalla.blit(bala_img, (x, y))

#! Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False

#! Loop del menu
menu_abierto = True

#! Loop del juego
se_ejecuta = False




while menu_abierto:
    #! Background de la pantalla
    pantalla.fill((0, 0, 240))
    texto_inicial()
        #! Iterar eventos
    for evento in pygame.event.get():

        #! Cerrar Juego
        if evento.type == pygame.QUIT: 
            se_ejecuta = False
            menu_abierto = False
        
        #! Presionar Teclas
        if evento.type == pygame.KEYDOWN: #? Verifico si alguna tecla fue presionada
            if evento.key == pygame.K_RETURN :
                print("Me ejecute")
                menu_abierto = False
                se_ejecuta = True

        while se_ejecuta:
            
            #! Background de la pantalla
            pantalla.blit(fondo, (0, 0))

            #! Iterar eventos
            for evento in pygame.event.get():

                #! Cerrar Juego
                if evento.type == pygame.QUIT: #? Si ocurre este evento cierro la pantalla
                    se_ejecuta = False
                
                #! Presionar Teclas
                if evento.type == pygame.KEYDOWN: #? Verifico si alguna tecla fue presionada
                    if evento.key == pygame.K_UP:
                        submarino_y_cambio = -0.1 # Produce movimiento hacia arriba
                    if evento.key == pygame.K_DOWN:
                        submarino_y_cambio = 0.1  # Produce movimiento hacia abajo
                    if evento.key == pygame.K_LEFT:
                        print("flecha izquierda")
                    if evento.key == pygame.K_RIGHT:
                        print("flecha derecha")
                    if evento.key == pygame.K_SPACE:
                        if not bala_visible: #? Evito cambiar la direccion de la bala si ya es visible
                            bala_y = submarino_y # Accedo al valor de submarino_y para que la bala tenga el valor inicial del submarino pero despues sea independiente a ese valor
                            disparar_bala(bala_x, bala_y)
                            sonido_disparo = mixer.Sound("assets/disparo.mp3")
                            sonido_disparo.play()

                #! Soltar flechas
                if evento.type == pygame.KEYUP: #? Verifico si el usuario suelta una tecla
                    if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN or evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                        submarino_y_cambio = 0 # Para el movimiento en y

            #! Actualizar ubicacion submarino
            submarino_y += submarino_y_cambio

            #! Mantener submarino en pantalla
            if submarino_y <= 0: #? Evito que el submarino exceda el limite superior
                submarino_y = 0

            elif submarino_y >= 536: #? Evito que el submarino exceda el limite inferior
                submarino_y = 536

            #! Actualizar ubicacion enemigo
            for indice in range(cantidad_enemigos): #? Parea poder acceder al enemigo indicado por su indice
                if enemigo_x[indice] < 74:
                    for p in range(cantidad_enemigos):
                        enemigo_x[p] = 2000
                    game_over = True
                    #texto_final()
                    break #? Final del JUEGO
                enemigo_y[indice] += enemigo_y_cambio[indice]

            #! Mantener enemigo en pantalla
                if enemigo_y[indice] <= 0: #? Evito que el submarino exceda el limite superior
                    enemigo_y_cambio[indice] = 0.27
                    enemigo_x[indice] += enemigo_x_cambio[indice]

                elif enemigo_y[indice] >= 536: #? Evito que el submarino exceda el limite inferior
                    enemigo_y_cambio[indice] = -0.27
                    enemigo_x[indice] += enemigo_x_cambio[indice]

                #! colision
                colision = hay_colision(enemigo_x[indice], enemigo_y[indice], bala_x, bala_y)
                if colision:
                    sonido_colision = mixer.Sound("assets/Golpe.mp3")
                    sonido_colision.play()
                    bala_x = submarino_x +64
                    bala_visible = False
                    puntaje += 10
                    enemigo_x[indice] = random.randint(500, 736)
                    enemigo_y[indice] = random.randint(0, 536)

                #! Llamada a la funcion del enemigo 
                enemigo(enemigo_x[indice], enemigo_y[indice], indice)

            #! Movimiento Bala
            if bala_x >= 864:
                bala_x = 74
                bala_visible = False 

            elif bala_visible:
                disparar_bala(bala_x, bala_y)
                bala_x += bala_x_cambio


            submarino(submarino_x, submarino_y)
            mostrar_puntaje(puntaje_x, puntaje_y )
            if game_over:
                texto_final()

            pygame.display.update()
            
    pygame.display.update()
                









