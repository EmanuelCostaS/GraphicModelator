import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from camera.camera import configure_projection_matrix, Camera

from transformations import scaling_matrix_4x4, translation_matrix_4x4, rotation_matrix_4x4

def init_opengl(width, height):
    # Configurações básicas da OpenGL
    glClearColor(0.0, 0.0, 0.0, 0.0) # Cor de fundo preta
    glClearDepth(1.0) # Valor padrão do z-buffer
    glEnable(GL_DEPTH_TEST) # Habilita o teste de profundidade (Z-buffer para visibilidade)
    glDepthFunc(GL_LESS) # Testa se o novo pixel está mais próximo que o anterior
    glShadeModel(GL_SMOOTH) # Habilita o sombreamento suave (Gouraud por padrão na OpenGL fixa)

    configure_projection_matrix(width, height, False) # Configura a matriz de projeção


    # 4. Aplique sua matriz. A transposição (.T) é vital para alinhar o formato
    #    do NumPy com o formato interno do OpenGL.


    # --- Configuração de Iluminação (Modelo de Phong) ---
    glEnable(GL_LIGHTING) # Habilita o sistema de iluminação
    glEnable(GL_LIGHT0) # Ativa a primeira fonte de luz (LIGHT0)

    # Posição da Luz 0 (luz direcional no exemplo, w=0)
    # Se w=0, a luz é direcional (raios paralelos). Se w=1, é pontual.
    light_position = [0.0, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # Cores da Luz 0
    light_ambient = [0.2, 0.2, 0.2, 1.0] # Componente ambiente (luz geral)
    light_diffuse = [0.8, 0.8, 0.8, 1.0] # Componente difusa (direção da luz)
    light_specular = [1.0, 1.0, 1.0, 1.0] # Componente especular (brilho)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    # --- Propriedades do Material do Objeto ---
    # As cores do material interagem com as cores da luz para determinar a cor final do objeto.
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0) # Nível de brilho especular (0-128)


def draw_object():
    

    #glRotatef(pygame.time.get_ticks() * 0.1, 1, 1, 0)
    rotation_matrix = rotation_matrix_4x4(1, 'y')
    rotation_matrix = rotation_matrix*rotation_matrix_4x4(1, 'z')
    #rotation_matrix = rotation_matrix_4x4(1, 'x')
    rotation_matrix = rotation_matrix * rotation_matrix_4x4(pygame.time.get_ticks() * 0.001, 'x')
    glMultMatrixf(rotation_matrix.T) # Multiplica a matriz atual 

    # --- Exemplo de Aplicação de Transformações com glMultMatrix() ---
    # Para usar suas próprias matrizes de translação, rotação e escala
    # (25% e 20% do trabalho)
    # Crie uma matriz 4x4 em um array NumPy ou lista de 16 elementos (float32)
    # Exemplo de matriz de rotação em torno do eixo Y:
    # rotation_matrix_y = [
    #    cos_angle, 0, sin_angle, 0,
    #    0, 1, 0, 0,
    #    -sin_angle, 0, cos_angle, 0,
    #    0, 0, 0, 1
    # ]
    # glMultMatrixf(rotation_matrix_y) # Multiplica a matriz atual pela sua matriz

    # Desenha um cubo simples
    glBegin(GL_QUADS) # Inicia o desenho de quads (faces de 4 vértices)
    # Frente
    glNormal3f(0.0, 0.0, 1.0) # Normal da superfície (aponta para fora) - importante para iluminação
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)

    # Trás
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    # Topo
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)

    # Base
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    # Direita
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    # Esquerda
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glEnd() # Finaliza o desenho de quads 


### MODIFICADO ###
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
     
    translation = translation_matrix_4x4(-camera_pos[0], -camera_pos[1], -camera_pos[2])
    glMultMatrixf(translation.T) # Multiplica a matriz atual pela matriz de translação 

    #glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])

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