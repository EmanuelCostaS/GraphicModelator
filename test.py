import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

def init_opengl(width, height):
    # Configurações básicas da OpenGL
    glClearColor(0.0, 0.0, 0.0, 0.0) # Cor de fundo preta
    glClearDepth(1.0) # Valor padrão do z-buffer
    glEnable(GL_DEPTH_TEST) # Habilita o teste de profundidade (Z-buffer para visibilidade)
    glDepthFunc(GL_LESS) # Testa se o novo pixel está mais próximo que o anterior
    glShadeModel(GL_SMOOTH) # Habilita o sombreamento suave (Gouraud por padrão na OpenGL fixa)

    # Configuração da Matriz de Projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Exemplo de Projeção Perspectiva
    # fovy: ângulo do campo de visão em Y
    # aspect: proporção largura/altura
    # zNear: distância do plano de corte próximo
    # zFar: distância do plano de corte distante
    gluPerspective(45, (width / height), 0.1, 100.0)

    # Configuração da Matriz de Modelo/Visão
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa o buffer de cor e profundidade
    glLoadIdentity() # Reseta a matriz de modelo/visão para a identidade
    glTranslatef(0.0, 0.0, -5.0) # Move a câmera para trás para o objeto ser visível

    glRotatef(pygame.time.get_ticks() * 0.1, 1, 1, 0)

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

    pygame.display.flip() # Atualiza a tela (mostra o que foi desenhado)

def main():
    pygame.init() # Inicializa o Pygame
    display = (800, 600) # Dimensões da janela
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL) # Cria a janela com suporte a OpenGL
    pygame.display.set_caption("CG FURG - Ambiente OpenGL") # Título da janela

    init_opengl(*display) # Inicializa as configurações da OpenGL

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Se o usuário clicar para fechar a janela
                running = False

        draw_object() # Desenha o objeto
        pygame.time.wait(10) # Pequena pausa para reduzir o uso da CPU

    pygame.quit() # Encerra o Pygame

if __name__ == "__main__":
    main()