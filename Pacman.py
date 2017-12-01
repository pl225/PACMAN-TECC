#Alunos: Julia Rodrigues, Matheus Abreu e Victor Diniz. 
#! /usr/bin/env python
import pygame
import time
import random
import math
from pygame.locals import *
from sys import exit

# CORES

# Pacman
PACMAN = (255, 255, 0)

# Fantasmas
CLYDE = (255, 127, 000)
BLINK   = (255, 0, 0)
PINK = (255, 062, 150)
INKY  = (000, 191, 255)

# Cenario
PILL = (240,230,140)
BLACK = (0, 0, 0)
PACPILL = (218, 165, 32) 
WALL = (067, 170, 067)
GHOSTGREEN = (0, 255, 0)
FOOD = (107, 142, 035)


class Mapa():
    def __init__ (self, gradeX, gradeY):
        self.limite_horizontal = gradeX
        self.limite_vertical = gradeY
            
            
    def criaObj(self, matriz):
        pacman = []
        ghosts = []
        specialPills = []
        pills = []
        walls = []
        k = 1
        for i in range(0, 12):
            for j in range(0, 12):
                if(matriz[j][i] == 0):
                    pills.append((64 * i, 32 * j))
                if(matriz[j][i] == 1):
                    walls.append((64 * i, 32 * j))
                if(matriz[j][i] == 2):
                    pacman.append((64 * i, 32 * j, 0, 0))
                if(matriz[j][i] == 3 or matriz[j][i] == 4 or matriz[j][i] == 5 or matriz[j][i] == 6):
                    ghosts.append((64 * i, 32 * j, k, 0))
                    k += 1
                if(matriz[j][i] == 10):
                    specialPills.append((64 * i, 32 * j))
        
        return (pacman, pills, specialPills, walls, ghosts)

    def renderizaObj(self, pacman, pills, specialPills, walls, ghosts, screen):
        #pills
        for i in range(0, len(pills)):
            (P_x, P_y) = pills[i]
            pygame.draw.circle(screen, FOOD, (P_x + 32, P_y + 16), 5, 0)
        #pills de forca
        for i in range(0, len(specialPills)):
            (P_x, P_y) = specialPills[i]
            pygame.draw.circle(screen, PILL, (P_x + 32, P_y + 16), 10, 0)
        #pacman            
        (pacmanX, pacmanY, estado, _) = pacman[0]
        if(estado == 0):
            pygame.draw.circle(screen, PACMAN, (pacmanX + 32, pacmanY + 16), 10, 0)
        else:
            pygame.draw.circle(screen, PACPILL, (pacmanX + 32, pacmanY + 16), 10, 0)
        #fantasma
        for i in range(0, len(ghosts)):
            (G_x, G_y, nF, estadoF) = ghosts[i]
            if(nF == 1 and estado == 0):
                pygame.draw.circle(screen, CLYDE,(G_x + 32, G_y + 16), 10, 0)
            elif(nF == 2 and estado == 0):
                pygame.draw.circle(screen, BLINK,(G_x + 32, G_y + 16), 10, 0)
            elif(nF == 3 and estado == 0):
                pygame.draw.circle(screen, PINK,(G_x + 32, G_y + 16), 10, 0)
            elif(nF == 4 and estado == 0):
                 pygame.draw.circle(screen, INKY,(G_x + 32, G_y + 16), 10, 0)
            else:
                pygame.draw.circle(screen, GHOSTGREEN,(G_x + 32, G_y + 16), 10, 0)
        #walls
        for i in range(0, len(walls)):
            (P_x, P_y) = walls[i]
            pygame.draw.rect(screen, WALL, (P_x, P_y, 64, 32), 0)
            
        pygame.draw.line(screen, WALL, (0, 384), (768, 384), 3)
        pygame.display.update() #atualiza a tela

    def movimentoPossivel(self, movimento, walls):
        for i in range(0, len(walls)):
            if(self.colisao(movimento,  walls[i])):
               return 0
        (movimento_horizontal, movimento_vertical) = movimento
        if(movimento_horizontal < 0 or movimento_horizontal >= self.limite_horizontal or movimento_vertical < 0 or movimento_vertical >= self.limite_vertical):
            return 0
        else: 
            return 1  

    def colisao(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        
        if(x1 == x2 and y1 == y2):
            return 1 # Colidiu!!!
        else: 
            return 0 # Nao colidiu!!!     

    def catchPacman(self, pacman, ghosts, vidas):
        (P_x, P_y, estado, _) = pacman[0]
        reset = 0
        for i in range(0, len(ghosts)):
            (G_x, G_y, _, _) = ghosts[i]
            if(self.colisao((P_x, P_y), (G_x, G_y)) == 1 and estado == 0):
                vidas -= 1
                reset = 1
                return (vidas, reset)
        return (vidas, reset)

    def catchGhost(self, pacman, ghosts, score, pontuacao_ghosts):
        (P_x, P_y, estado, tempo) = pacman[0]
        if(pontuacao_ghosts > 4):
            pontuacao_ghosts = 1
        elif(tempo == 0):
            pontuacao_ghosts = 1
        reset = 0
        for i in range(0, len(ghosts)):
            (G_x, G_y, nF, _) = ghosts[i]
            if(self.colisao((P_x, P_y), (G_x, G_y)) == 1 and estado == 1):
                score += pow(200, pontuacao_ghosts)
                pontuacao_ghosts += 1
                if(nF == 1):
                    ghosts[0] = (320, 160, 1, 0)
                elif(nF == 2):
                    ghosts[1] = (384, 160, 2, 0)
                elif(nF == 3):
                    ghosts[2] = (320, 192, 3, 0)
                elif(nF == 4):
                    ghosts[3] = (384, 192, 4, 0)
                return (score, pontuacao_ghosts, ghosts)
        return (score, pontuacao_ghosts, ghosts)                


    def pillsResult(self, pacman, pills, specialPills, score):
        (P_x, P_y, _, _) = pacman[0]
        for i in range(0, len(pills)):
            if(self.colisao((P_x, P_y), pills[i])):
                score += 10
                (posX, posY) = pills[i]
                pills.remove((posX, posY))
                break
        for i in range(0, len(specialPills)):
            if(self.colisao((P_x, P_y), specialPills[i])):
                score += 50
                (posX, posY) = specialPills[i]
                specialPills.remove((posX, posY))
                pacman[0] = (P_x, P_y, 1, 8)
                break
        return score

    
    def moveGhosts(self, fantasma, pacman, mX, mY, walls):
        i = 0
        movInv = 0
        (P_x, P_y, estadoP, _) = pacman[0]
        while(i < len(fantasma)):            
            (G_x, G_y, nF, estado) = fantasma[i]
            dist = ManhattanDistance(P_x, G_x, P_y, G_y)
            if(dist < 180 and estadoP == 0): #predador
                dist = 1000
                l = G_x - mX
                r = G_x + mX
                u = G_y - mY
                d = G_y + mY
                caca = ManhattanDistance(P_x, l, P_y, G_y)
                if(caca < dist and self.movimentoPossivel((l, G_y), walls) == 1):
                    dist = caca
                    fX = l
                    fY = G_y
                caca = ManhattanDistance(P_x, r, P_y, G_y) 
                if(caca < dist and self.movimentoPossivel((r, G_y), walls) == 1):
                    dist = caca
                    fX = r
                    fY = G_y
                caca = ManhattanDistance(P_x, G_x, P_y, d)
                if(caca < dist and self.movimentoPossivel((G_x, d), walls) == 1):
                    dist = caca
                    fX = G_x
                    fY = d
                caca = ManhattanDistance(P_x, G_x, P_y, u)
                if(caca < dist and self.movimentoPossivel((G_x, u), walls) == 1):
                    dist = caca
                    fX = G_x
                    fY = u
                fantasma[i] = (fX, fY, nF, estado)
                i += 1
            elif(dist < 180 and estadoP == 1): #presa
                dist = 0
                l = G_x - mX
                r = G_x + mX
                u = G_y - mY
                d = G_y + mY
                caca = ManhattanDistance(P_x, l, P_y, G_y)
                if(caca > dist and self.movimentoPossivel((l, G_y), walls) == 1):
                    dist = caca
                    fX = l
                    fY = G_y
                caca = ManhattanDistance(P_x, r, P_y, G_y) 
                if(caca > dist and self.movimentoPossivel((r, G_y), walls) == 1):
                    dist = caca
                    fX = r
                    fY = G_y
                caca = ManhattanDistance(P_x, G_x, P_y, d)
                if(caca > dist and self.movimentoPossivel((G_x, d), walls) == 1):
                    dist = caca
                    fX = G_x
                    fY = d
                caca = ManhattanDistance(P_x, G_x, P_y, u)
                if(caca > dist and self.movimentoPossivel((G_x, u), walls) == 1):
                    dist = caca
                    fX = G_x
                    fY = u
                fantasma[i] = (fX, fY, nF, estado)
                i += 1
            else:
                direction = random.randint(0,3)
                if(direction == 0):
                    G_x -= mX
                elif(direction == 1):
                    G_x += mX
                elif(direction == 2):
                    G_y -= mY
                elif(direction == 3):
                    G_y += mY
                if(self.movimentoPossivel((G_x, G_y), walls) == 1):
                    for j in range(0, len(fantasma)):
                        (verX, verY, _, _) = fantasma[j]
                        #if(G_x == verX and G_y == verY):
                        #    movInv = 1
                    if(movInv == 0):
                        fantasma[i] = (G_x, G_y, nF, estado)
                        i += 1
                    else:
                        movInv = 0

    def gameOver(self, vidas, pills, specialPills):
        if(vidas <= 0):
            print("POXA, VOCE PERDEU! :( \n")
            end = 1
        elif(len(pills) == 0 and len(specialPills) == 0):
            print("UHUL! VOCE VENCEU! :D \n")
            end = 1
        else:
            end = 0
        return end
                 

def ManhattanDistance(posX1, posX2, posY1, posY2):
    resultado = math.fabs(posX1 - posX2) + math.fabs(posY1 - posY2)
    return resultado
    
def playGame():
    pygame.init() 
    pygame.mixer.init() 
    pygame.font.init()

    DimensaoX = 768 
    DimensaoY = 440 
    screen = pygame.display.set_mode((DimensaoX, DimensaoY), 0, 32) 

    pygame.display.set_caption('PACMAN - PERDIDO NO BOSQUE') 
    pygame.mixer.music.load('Tema.ogg') 

    clock = pygame.time.Clock() 
    background_filename = 'Mapa.png'
    background = pygame.image.load(background_filename).convert()
    
    pygame.mixer.music.play(-1, 0.0) 
    pygame.mixer.music.set_volume(0.4)
   
                 
    framerate = 5
    vida = 3
    pontuacao = 0
    pontuacao_ghosts = 1
    
    move_horizontal = 64
    move_vertical = 32
    
    matriz = [[10,0,0,0,0,0,0,0,0,0,0,10],
              [0,1,0,1,1,0,0,1,1,0,1,0],
              [0,1,0,0,0,0,0,0,0,0,1,0],
              [0,1,1,1,0,1,1,0,1,1,1,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],
              [0,1,0,1,0,3,4,0,1,0,1,0],
              [1,0,0,0,1,5,6,1,0,0,0,1],
              [0,1,1,0,1,1,1,1,0,1,1,0],
              [0,0,1,0,0,0,0,0,0,1,0,0],
              [0,0,0,1,0,0,0,0,1,0,0,0],
              [0,1,0,0,0,1,1,0,0,0,1,0],
              [10,0,0,0,0,2,0,0,0,0,0,10]]
    
    mapa = Mapa(DimensaoX, 384)
    reset = 0
    (pacman, pills, specialPills, walls, ghosts) = mapa.criaObj(matriz)
    
    while True: 

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                pygame.mixer.music.stop()
                exit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                (pacmanX, pacmanY, estado, tempo) = pacman[0]
                pacmanX -= move_horizontal
                if(mapa.movimentoPossivel((pacmanX, pacmanY), walls)):
                    pacman = []
                    pacman.append((pacmanX, pacmanY, estado, tempo))
            elif event.key == K_RIGHT:
                (pacmanX, pacmanY, estado, tempo) = pacman[0]
                pacmanX += move_horizontal
                if(mapa.movimentoPossivel((pacmanX, pacmanY), walls)):
                    pacman = []
                    pacman.append((pacmanX, pacmanY, estado, tempo))
            elif event.key == K_UP:
                (pacmanX, pacmanY, estado, tempo) = pacman[0]
                pacmanY -= move_vertical
                if(mapa.movimentoPossivel((pacmanX, pacmanY), walls)):
                    pacman = []
                    pacman.append((pacmanX, pacmanY, estado, tempo))
            elif event.key == K_DOWN:
                (pacmanX, pacmanY, estado, tempo) = pacman[0]
                pacmanY += move_vertical
                if(mapa.movimentoPossivel((pacmanX, pacmanY), walls)):
                    pacman = []
                    pacman.append((pacmanX, pacmanY, estado, tempo))

       
        (pacmanX, pacmanY, estado, tempo) = pacman[0]
        if(tempo > 0):
            tempo -= 1  # Decrementa o tempo da pilula especial
        else:
            estado = 0
        pacman = []
        pacman.append((pacmanX, pacmanY, estado, tempo))
        (vida, reset) = mapa.catchPacman(pacman, ghosts, vida)
        (pontuacao, pontuacao_ghosts, ghosts) = mapa.catchGhost(pacman, ghosts, pontuacao, pontuacao_ghosts)
            
        pontuacao = mapa.pillsResult(pacman, pills, specialPills, pontuacao) #calcula pontuacao
        mapa.moveGhosts(ghosts, pacman, move_horizontal, move_vertical, walls)
        (vida, reset) = mapa.catchPacman(pacman, ghosts, vida)
        (pontuacao, pontuacao_ghosts, ghosts) = mapa.catchGhost(pacman, ghosts, pontuacao, pontuacao_ghosts)
        
        if(reset == 1):
            pacman[0] = (384, 352, 0, 0)
            ghosts[0] = (320, 160, 1, 0)
            ghosts[1] = (384, 160, 2, 0)
            ghosts[2] = (320, 192, 3, 0)
            ghosts[3] = (384, 192, 4, 0)
            reset = 0

 
        screen.blit(background, (0, 0))
        mapa.renderizaObj(pacman, pills, specialPills, walls, ghosts, screen)
        
        # SCORE
        fontScore = pygame.font.SysFont("ARIAL BLACK", 20)
        textsurface = fontScore.render("SCORE:", False, (255, 255, 0))
        screen.blit(textsurface,(5,395))
        pygame.draw.rect(screen, BLACK, (55, 395, 80, 50), 0)
        fontScore = pygame.font.SysFont("ARIAL BLACK", 20)
        textsurface = fontScore.render(str(pontuacao), False, (255, 0, 0))
        screen.blit(textsurface,(60,395))

        # LIFE
        fontVidas = pygame.font.SysFont("ARIAL BLACK", 20)
        textsurface = fontVidas.render("LIFE:", False, (255, 255, 0))
        screen.blit(textsurface,(5,415))
        pygame.draw.rect(screen, BLACK, (50, 415, 80, 50), 0)
        fontVidas = pygame.font.SysFont("ARIAL BLACK", 20)
        textsurface = fontVidas.render(str(vida), False, (255, 0, 0))
        screen.blit(textsurface,(60,415))

        pygame.display.update() 
        end = mapa.gameOver(vida, pills, specialPills)
        
        if(end == 1):
            print("A sua pontuacao foi: ")
            print(pontuacao)
            pygame.display.quit()
            pygame.mixer.music.stop()
            exit()
            
        time_passed = clock.tick(framerate) 


if __name__ == "__main__":
    playGame()
