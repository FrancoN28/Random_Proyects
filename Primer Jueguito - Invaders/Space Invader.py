import pygame,sys
from pygame.locals import *
from random import randint
from Clases import Nave
from Clases import Invasor

#variables globales
ancho = 900
alto = 500
listaEnemigo =[]

def detenerTodo():
	for enemigo in listaEnemigo:
		for disparo in enemigo.listaDisparo:
			enemigo.listaDisparo.remove(disparo)

		enemigo.conquista = True
		
def cargarEnemigos():
	posx = 113
	for x in range(4):
		enemigo = Invasor.Invasor(posx,100,40, 'Imagenes/MarcianoA.jpg','Imagenes/MarcianoB.jpg')
		listaEnemigo.append(enemigo)	
		posx += 200

	posx = 100
	for x in range(4):
		enemigo = Invasor.Invasor(posx,0,40, 'Imagenes/Marciano2A.jpg','Imagenes/Marciano2B.jpg')
		listaEnemigo.append(enemigo)	
		posx += 200

	posx = 100
	for x in range(4):
		enemigo = Invasor.Invasor(posx,-100,40, 'Imagenes/Marciano2B.jpg','Imagenes/Marciano3B.jpg')
		listaEnemigo.append(enemigo)	
		posx += 200

def SpaceInvader(): #FUNCION DEL JUEGO
	pygame.init()
	ventana = pygame.display.set_mode((ancho,alto))
	pygame.display.set_caption('Space Invader')

	ImagenFondo = pygame.image.load('Imagenes/Fondo.jpg')

	#pygame.mixer.music.load('Sonidos/Intro.mp3') #hay q tener el archivo
	#pygame.mixer.music.play(3)#el numero indica la cantidad de veces q se repetira la musica

	jugador = Nave.naveEspacial(ancho,alto)
	move_left = False
	move_right = False
	cargarEnemigos() #creamos un enemigo

	miFuente = pygame.font.SysFont('arial',60)
	TextoFinal = miFuente.render('Fin del Juego',0,(120,100,40))

	enJuego = True

	reloj = pygame.time.Clock()

	while True:

		reloj.tick(30) #establece cuantos frames se ejecutan por segundo

		ventana.blit(ImagenFondo, (0,0))#dibujamos el fondo

		tiempo = pygame.time.get_ticks()//1000

		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				sys.exit()

			if enJuego == True: 
				if evento.type == pygame.KEYDOWN:
					if evento.key == K_LEFT:#movimiento izq
						move_left = True
					elif evento.key == K_RIGHT:#movimiento der
						move_right = True

					elif evento.key == K_s: #disparar
						x,y = jugador.rect.center#la posicion del disparo va a depender de la pos del jugador
						jugador.disparar(x,y)

				elif evento.type == pygame.KEYUP:
					if evento.key == K_LEFT:
						move_left = False
					elif evento.key == K_RIGHT:
						move_right = False

		if move_left == True:#aplicar movimiento
			jugador.rect.left -= jugador.velocidad
			jugador.movimiento() #corregimos que no se salga del marco
		if move_right == True:
			jugador.rect.right += jugador.velocidad
			jugador.movimiento()

		if len(jugador.listaDisparo) > 0:
			for x in jugador.listaDisparo:
				x.dibujar(ventana)
				x.trayectoria()
				if x.rect.top < 0:
					jugador.listaDisparo.remove(x)
				else:
					for enemigo in listaEnemigo:
						if x.rect.colliderect(enemigo.rect):#si disparo jugador choca enemigo
							listaEnemigo.remove(enemigo)
							jugador.listaDisparo.remove(x)


		if len(listaEnemigo) > 0:
			for enemigo in listaEnemigo:
				enemigo.comportamiento(tiempo)

				if enemigo.rect.colliderect(jugador.rect):#si enemigo choca jugador
					enJuego = False
					jugador.destruccion()
					detenerTodo()

				for x in enemigo.listaDisparo:
					x.dibujar(ventana)
					x.trayectoria()
					if x.rect.top > 900:
						enemigo.listaDisparo.remove(x)
					else:
						for disparo in jugador.listaDisparo:
							if x.rect.colliderect(disparo.rect):#si ambos disparos chocan
								jugador.listaDisparo.remove(disparo)
								enemigo.listaDisparo.remove(x)

					if x.rect.colliderect(jugador.rect): #si disparo enemigo chocha jugador
						enJuego = False
						jugador.destruccion()
						detenerTodo()

				enemigo.dibujar(ventana) #lo escribo al final para que el enemigo aparezca arriba del disparo
		else: enJuego = False


		jugador.dibujar(ventana)#en esa superficie
 
		if enJuego == False:
			#pygame.mixer.music.fadeout(3000)#en 3 segundos la musica se atenua y desaparece
			ventana.blit(TextoFinal,(275,200))

		pygame.display.update()

SpaceInvader()






