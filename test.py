import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from camera.camera import configure_projection_matrix, Camera
import math


def init_opengl(width, height):
    """Configurações básicas da OpenGL"""
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    
    # A configuração da projeção é agora feita em draw_scene
    # configure_projection_matrix(width, height, False) 

    # --- Configuração de Iluminação (Modelo de Phong) ---
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    light_position = [0.0, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    # --- Propriedades do Material do Objeto ---
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.004, 0.408, 0.627]) # Material um pouco esverdeado
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.004, 0.408, 0.627])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

def hexagon(radius, height, num_segments):
    top_vertices = []
    bottom_vertices = []
    for i in range(num_segments):
        # Ângulo para cada vértice
        angle = 2 * math.pi * i / num_segments
        # Coordenadas x e y baseadas no ângulo e raio
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        # Adiciona o vértice do topo e da base à lista
        top_vertices.append((x, y, height / 2.0))
        bottom_vertices.append((x, y, -height / 2.0))

        # Desenha a face do topo
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)  # Normal aponta para cima no eixo Z
    for vertex in top_vertices:
        glVertex3f(*vertex) # O '*' desempacota a tupla (x,y,z) nos argumentos da função
    glEnd()

    # Desenha a face da base
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, -1.0) # Normal aponta para baixo no eixo Z
    # Desenha em ordem inversa para manter a face virada para fora
    for vertex in reversed(bottom_vertices):
        glVertex3f(*vertex)
    glEnd()

    # Desenha as faces laterais
    glBegin(GL_QUADS)
    for i in range(num_segments):
        # Vértices do quad da lateral atual
        v1_top = top_vertices[i]
        v2_bottom = bottom_vertices[i]
        # O operador '%' garante que o índice volte a 0 após o último vértice
        v3_bottom = bottom_vertices[(i + 1) % num_segments]
        v4_top = top_vertices[(i + 1) % num_segments]

        # Calcula a normal para a face lateral.
        # A normal é perpendicular à face e aponta para fora do centro.
        # Para um hexágono regular, o ângulo da normal é o ângulo médio entre os dois vértices.
        normal_angle = 2 * math.pi * (i + 0.5) / num_segments
        normal_x = math.cos(normal_angle)
        normal_y = math.sin(normal_angle)
        glNormal3f(normal_x, normal_y, 0.0)

        # Desenha o quad da lateral usando os 4 vértices
        glVertex3f(*v1_top)
        glVertex3f(*v2_bottom)
        glVertex3f(*v3_bottom)
        glVertex3f(*v4_top)
    glEnd()

def draw_object():
    """Desenha um prisma hexagonal 3D no lugar do cubo."""
    
    # Mantém a rotação do objeto original para melhor visualização
    glRotatef(pygame.time.get_ticks() * 0.05, 0.5, 1, 0.2)

    # --- Desenho de um Prisma Hexagonal ---
    radius = 1.0  # Distância do centro a um vértice
    height = 0.2  # Altura total do prisma
    num_segments = 6 # Número de lados (hexágono)

    hexagon(radius, height, num_segments)


def draw_scene(camera_pos, is_perspective, width, height):
    """
    Desenha os objetos na cena, aplicando a transformação da câmera primeiro.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    configure_projection_matrix(width, height, not is_perspective) # Configura a matriz de projeção

    # --- Aplicação da Câmera (Matriz de Visão) ---
    # Usamos os valores da posição da câmera, mas INVERTIDOS.
    # Para mover a câmera para +X, movemos o mundo para -X.
    glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])

    # --- Desenho dos Objetos (Matriz de Modelo) ---
    # Todas as transformações de objetos vêm DEPOIS da câmera.

    # Salva o estado atual da matriz (depois da transformação da câmera)
    glPushMatrix()
    draw_object()
    glPopMatrix()

    pygame.display.flip()   

def main():
    pygame.init() # Inicializa o Pygame
    display = (800, 600) # Dimensões da janela
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL) # Cria a janela com suporte a OpenGL
    pygame.display.set_caption("CG FURG - Ambiente OpenGL") # Título da janela

    init_opengl(*display) # Inicializa as configurações da OpenGL

   
    running = True

    is_perspective = True
    camera = Camera()
 

    while running:

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Se o usuário clicar para fechar a janela
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # Se a tecla P for pressionada
                    is_perspective = not is_perspective # Inverte o modo
                    print(f"Modo de projeção: {'Perspectiva' if is_perspective else 'Ortogonal'}")
        

        camera.update() 

        draw_scene(camera.camera_position, is_perspective, display[0], display[1]) ### MODIFICADO ###
 
        pygame.time.wait(10) # Pequena pausa para reduzir o uso da CPU

    pygame.quit() # Encerra o Pygame

if __name__ == "__main__":
    main()