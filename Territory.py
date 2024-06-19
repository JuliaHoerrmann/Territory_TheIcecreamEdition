# Importieren der Pygame-Bibliothek

import pygame, sys, os
from pygame.locals import *
import numpy as np
from scipy import spatial
from shapely.geometry import Polygon, LineString, Point
from myspatial import myVoronoi




# initialisieren von pygame
pygame.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# genutzte Farbe
ORANGE  = ( 255, 140, 0)
ROT     = ( 255, 0, 0)
GRUEN   = ( 0, 255, 0)
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)
PINK = (255, 192, 203)
DARKPINK = (102,0,102)
BLUE = (137, 207, 240)
DARKBLUE = (0,0,102)


player1 = pygame.image.load(os.path.join("EIS_Player1.png"))
player1=pygame.transform.scale(player1, (20,20))
player2 = pygame.image.load(os.path.join("EIS_Player2.png"))
player2=pygame.transform.scale(player2, (20, 20))

# Fenster öffnen
screensize=[600,600]
window=Polygon([(0,0),(600,0),(600,600),(0,600)])
screen = pygame.display.set_mode(screensize)
Area=screensize[0]*screensize[1]
screen.fill((255, 255, 255))


# Titel für Fensterkopf
pygame.display.set_caption("Territory - the ice cream edition. Spieler 1, platziere die erste Eisdiele!")

# solange die Variable True ist, soll das Spiel laufen
spielaktiv = True
i=0
Fläche_Sp1=0
Fläche_Sp2=0
Stand_Sp1=0
Stand_Sp2=0



# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock()

# Schleife Hauptprogramm
while spielaktiv:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False
            print("Spieler hat Quit-Button angeklickt")
        elif event.type == pygame.KEYDOWN:
            print("Spieler hat Taste gedrückt")

            # Taste für Spieler 1
            if event.key == pygame.K_RIGHT:
                print("Spieler hat Pfeiltaste rechts gedrückt")
            elif event.key == pygame.K_LEFT:
                print("Spieler hat Pfeiltaste links gedrückt")
            elif event.key == pygame.K_UP:
                print("Spieler hat Pfeiltaste hoch gedrückt")
            elif event.key == pygame.K_DOWN:
                print("Spieler hat Pfeiltaste runter gedrückt")
            elif event.key == pygame.K_SPACE:
                print("Spieler hat Leertaste gedrückt")

            # Taste für Spieler 2
            elif event.key == pygame.K_w:
                print("Spieler hat Taste w gedrückt")
            elif event.key == pygame.K_a:
                print("Spieler hat Taste a gedrückt")
            elif event.key == pygame.K_s:
                print("Spieler hat Taste s gedrückt")
            elif event.key == pygame.K_d:
                print("Spieler hat Taste d gedrückt")

        elif event.type == pygame.MOUSEBUTTONDOWN:


            i=i+1
            
            if i%2==0:
                  pygame.display.set_caption("Spieler 1: "+str(Stand_Sp1)+", Spieler 2: "+str(Stand_Sp2)+". Spieler 1, platziere Eisdiele!") 
            else:
                  pygame.display.set_caption("Spieler 1: "+str(Stand_Sp1)+", Spieler 2: "+str(Stand_Sp2)+". Spieler 2, platziere Eisdiele!")

            print("Spieler hat Maus angeklickt")
            pos=pygame.mouse.get_pos()
            print(pos)

            if i%2==0:
                screen.blit(player2, pos)
            else:
                screen.blit(player1, pos)

            pygame.display.update()
            
            pos=np.array([pos])
            if i==1: 
                xy=pos
            else:
                xy = np.concatenate((xy,pos))
            print(xy)

            if (i>=4)&(i<=20):
                vornew=myVoronoi(xy,window)
                # draw all the new edges in black
              #  for indx_pair in vornew.ridge_vertices:
              #     start_pos = vornew.vertices[indx_pair[0]]
              #      end_pos = vornew.vertices[indx_pair[1]]
              #      pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos)
            
                screen.fill((255, 255, 255))
               
                for j in range(i):
                    pygame.display.flip()
                    region=vornew.regions[vornew.point_region[j]]          
                    if (j+1)%2==0:
                        if (len(region)>2)&(min(region)>-1):
                            verts=vornew.vertices[region]
                            pygame.draw.polygon(screen, BLUE,verts)
                            pygame.draw.polygon(screen, SCHWARZ,verts,1)

                            pg=Polygon(verts)
                            Fläche_Sp2=Fläche_Sp2+pg.area
                            print(pg.area)
                        pygame.draw.circle(screen,DARKBLUE,xy[j],3)
                        screen.blit(player2, xy[j])

                    else:
                        if (len(region)>2)&(min(region)>-1):
                            verts=vornew.vertices[region]
                            pygame.draw.polygon(screen, PINK,verts)
                            pygame.draw.polygon(screen, SCHWARZ,verts,1)
                            
                            pg=Polygon(verts)
                            Fläche_Sp1=Fläche_Sp1+pg.area
                        pygame.draw.circle(screen,DARKPINK,xy[j],3)
                        screen.blit(player1, xy[j])

                # Update des Spielstands
                Stand_Sp1=round(100*Fläche_Sp1/(max(1,Fläche_Sp1+Fläche_Sp2)))
                Stand_Sp2=round(100*Fläche_Sp2/max(1,(Fläche_Sp1+Fläche_Sp2)))

                
                Fläche_Sp1=0
                Fläche_Sp2=0

            elif i>20:

                    pygame.display.set_caption("Spieler 1: "+str(Stand_Sp1)+", Spieler 2: "+str(Stand_Sp2))
                    if Stand_Sp1>Stand_Sp2:
                        text1 = my_font.render('Gewinner: Spieler 1', False, (0, 0, 0))
                        text2 = my_font.render('Punktestand: '+str(Stand_Sp1)+str(" : ")+str(Stand_Sp2), False, (0, 0, 0))
                        screen.blit(text1, (round(screensize[0]/3),round(screensize[0]/3)))
                        screen.blit(text2, (round(screensize[0]/3),round(screensize[0]/3)+30))
                    elif Stand_Sp2>Stand_Sp1:
                        text1 = my_font.render('Gewinner: Spieler 2', False, (0, 0, 0))
                        text2 = my_font.render('Punktestand: '+str(Stand_Sp1)+' : '+str(Stand_Sp2), False, (0, 0, 0))
                        screen.blit(text1, (round(screensize[0]/3),round(screensize[0]/3)))
                        screen.blit(text2, (round(screensize[0]/3),round(screensize[0]/3)+30))
                    else:
                        text1 = my_font.render('Unentschieden', False, (0, 0, 0))
                        text2 = my_font.render('Punktestand: '+str(Stand_Sp1)+' : '+str(Stand_Sp2), False, (0, 0, 0))
                        screen.blit(text1, (round(screensize[0]/3),round(screensize[0]/3)))
                        screen.blit(text2, (round(screensize[0]/3),round(screensize[0]/3)+30))

    # Spiellogik hier integrieren

    # Spielfeld löschen
    #screen.fill(WEISS)

    # Spielfeld/figuren zeichnen

    # Fenster aktualisieren
    pygame.display.flip()

    # Refresh-Zeiten festlegen
    clock.tick(60)

pygame.quit()
