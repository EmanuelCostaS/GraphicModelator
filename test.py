import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from camera.camera import configure_projection_matrix, Camera
import math


def init_opengl(width, height):
    # Configurações básicas da OpenGL
    glClearColor(0.0, 0.0, 0.0, 0.0) # Cor de fundo preta
    glClearDepth(1.0) # Valor padrão do z-buffer
    glEnable(GL_DEPTH_TEST) # Habilita o teste de profundidade (Z-buffer para visibilidade)
    glDepthFunc(GL_LESS) # Testa se o novo pixel está mais próximo que o anterior
    glShadeModel(GL_SMOOTH) # Habilita o sombreamento suave

    # A configuração da projeção será feita em draw_scene
    # configure_projection_matrix(width, height, False)

    # --- Configuração de Iluminação (Modelo de Phong) ---
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Posição da Luz 0
    light_position = [0.0, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    # --- Propriedades do Material do Objeto ---
    # Define um material azul para o objeto
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.004, 0.2, 0.3, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.004, 0.408, 0.627, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 32.0)


### FUNÇÃO CORRIGIDA ###
def draw_object():
    """Desenha um prisma hexagonal 3D."""
    
    # Aplica uma rotação ao objeto para que ele gire na tela
    glRotatef(pygame.time.get_ticks() * 0.05, 0.5, 1, 0.2)

    # --- Parâmetros do Prisma Hexagonal ---
    radius = 1.2  # Distância do centro a um vértice
    height = 1.0  # Altura total do prisma
    num_segments = 6 # Número de lados (6 para um hexágono)

    # --- Cálculo dos Vértices ---
    top_vertices = []
    bottom_vertices = []
    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        top_vertices.append((x, y, height / 2.0))
        bottom_vertices.append((x, y, -height / 2.0))

    # --- Desenho da Face do Topo ---
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)  # Normal aponta para cima
    for vertex in top_vertices:
        glVertex3f(*vertex)
    glEnd()

    # --- Desenho da Face da Base ---
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, -1.0) # Normal aponta para baixo
    for vertex in reversed(bottom_vertices): # Ordem inversa para a face apontar para fora
        glVertex3f(*vertex)
    glEnd()

    # --- Desenho das Faces Laterais ---
    glBegin(GL_QUADS)
    for i in range(num_segments):
        v1_top = top_vertices[i]
        v2_bottom = bottom_vertices[i]
        v3_bottom = bottom_vertices[(i + 1) % num_segments]
        v4_top = top_vertices[(i + 1) % num_segments]

        # Calcula a normal para a face lateral (aponta para fora do centro)
        normal_angle = 2 * math.pi * (i + 0.5) / num_segments
        normal_x = math.cos(normal_angle)
        normal_y = math.sin(normal_angle)
        glNormal3f(normal_x, normal_y, 0.0)

        # Desenha o retângulo (quad) da lateral
        glVertex3f(*v1_top)
        glVertex3f(*v2_bottom)
        glVertex3f(*v3_bottom)
        glVertex3f(*v4_top)
    glEnd()


### MODIFICADO E CORRIGIDO ###
def draw_scene(camera_pos, is_perspective, width, height):
    """
    Desenha os objetos na cena, aplicando a transformação da câmera primeiro.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Configura a matriz de projeção (perspectiva ou ortogonal)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    configure_projection_matrix(width, height, is_perspective)

    # Configura a matriz de visão/modelo
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # --- Aplicação da Câmera (Matriz de Visão) ---
    # Move o mundo na direção oposta à da câmera.
    # Revertido para glTranslatef para garantir que o código funcione sem o arquivo transformations.py
    glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])

    # --- Desenho dos Objetos (Matriz de Modelo) ---
    # Salva o estado atual da matriz (depois da transformação da câmera)
    glPushMatrix()
    draw_object()
    glPopMatrix()

    pygame.display.flip()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("CG FURG - Hexágono")

    init_opengl(*display)
    
    running = True
    is_perspective = True
    camera = Camera()
    camera.camera_position[2] = 5 # Afasta a câmera para ver o objeto
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_perspective = not is_perspective
                    print(f"Modo de projeção: {'Perspectiva' if is_perspective else 'Ortogonal'}")
        
        camera.update()
        draw_scene(camera.camera_position, is_perspective, display[0], display[1])
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()