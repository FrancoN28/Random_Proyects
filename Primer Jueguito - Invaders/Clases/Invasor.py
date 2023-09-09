import pygame
from random import randint
from Clases import Proyectil


class Invasor(pygame.sprite.Sprite):
	def __init__(self,posx,posy,distancia,imagenUno,imagenDos):
		pygame.sprite.Sprite.__init__(self)

		self.imagenA = pygame.image.load(imagenUno)
		self.imagenA.set_colorkey((0,0,0))#elimina el fondo 

		self.imagenB = pygame.image.load(imagenDos)
		self.imagenB.set_colorkey((0,0,0))#elimina el fondo 


		self.listaImagenes = [self.imagenA,self.imagenB]
		self.posImagen = 0 #este va a ser el index de la imagen con la q va a empezar el invasor
		self.tiempoCambio = 1

		self.imagenInvasor = self.listaImagenes[self.posImagen]
		self.rect = self.imagenInvasor.get_rect()
		
		self.velocidad = 3
		self.rect.top = posy
		self.rect.left = posx

		self.listaDisparo = []
		self.frecDisparo = 5

		self.derecha = True
		self.contador = 0 
		self.maxdescenso = self.rect.top + 40

		self.limiteDerecha = posx + distancia
		self.limiteIzquierda = posx - distancia
		self.conquista = False



	def comportamiento(self,tiempo):

		
		if self.conquista == False: #esto es para que una vez terminado el juego los bichos no se sigan moviendo
			self.__movimientos()
			self.__ataque()

			if self.tiempoCambio == tiempo:
				self.posImagen += 1
				self.tiempoCambio += 1

				if self.posImagen > len(self.listaImagenes)-1:
					self.posImagen = 0 #si la posImagen pasa la posicion uno debe volver a 0 osea a la primer imagen

	def dibujar(self,superficie):
		self.imagenInvasor = self.listaImagenes[self.posImagen]
		superficie.blit(self.imagenInvasor, self.rect)

	def __ataque(self): 
		if (randint(0,300) < self.frecDisparo): 
			self.__disparo()

	def __disparo(self):
		
		x = self.rect.center[0] 
		y = self.rect.center[1] + 40
		miProyectil = Proyectil.Proyectil(x,y,'Imagenes/disparob.jpg',False)
		self.listaDisparo.append(miProyectil)

	def __movimientos(self):
		if self.contador < 3 :
			self.__movimientoLateral()
		else:
			self.__descenso()

	def __movimientoLateral(self):
		if self.derecha == True:
			self.rect.left += self.velocidad
			if self.rect.left >= self.limiteDerecha:
				self.derecha = False

				self.contador += 1
		else:
			self.rect.left -= self.velocidad
			if self.rect.left <= self.limiteIzquierda:
				self.derecha = True

	def __descenso(self):
		if self.maxdescenso == self.rect.top:
			self.contador = 0 #vuelve a moverse lateralmente
			self.maxdescenso = self.rect.top +40
		else:
			self.rect.top += 1 
