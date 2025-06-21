

import numpy as np
from camera.perspectives import perspective_matrix_from_scratch, orthogonal_matrix_from_scratch
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame


def configure_projection_matrix(width, height, is_orthogonal=False):

    ## Configuração da Matriz de Projeção caso fossemos usar a função OpenGL 
    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()
    ## Exemplo de Projeção Perspectiva
    ## fovy: ângulo do campo de visão em Y
    ## aspect: proporção largura/altura
    ## zNear: distância do plano de corte próximo
    ## zFar: distância do plano de corte distante
    #gluPerspective(45, (width / height), 0.1, 100.0)
    ## Configuração da Matriz de Modelo/Visão
    #glMatrixMode(GL_MODELVIEW)
    #glLoadIdentity()

    # Parâmetros para a projeção
    fov_rad = np.radians(45.0)
    aspect_ratio = width / height
    near_plane = 0.1
    far_plane = 100.0

    # Parametros para a projeção ortogonal
    zoom_factor = 5.0 
    left = -zoom_factor * aspect_ratio
    right = zoom_factor * aspect_ratio
    bottom = -zoom_factor
    top = zoom_factor

    # Cria a matriz usando sua função
    my_projection_matrix = orthogonal_matrix_from_scratch(left, right, bottom, top, near_plane, far_plane) if is_orthogonal else perspective_matrix_from_scratch(
        fov_rad, aspect_ratio, near_plane, far_plane
    )

    glMatrixMode(GL_PROJECTION)
    # 2. Resete a matriz da câmera para um estado limpo (identidade).
    glLoadIdentity()

    glMultMatrixf(my_projection_matrix.T)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



class Camera:


    def __init__(self):
        self.camera_position = [0.0, 0.0, 5.0]
        self.camera_speed = 0.1


    def update(self):
        keys = pygame.key.get_pressed()

        # Frente / Trás
        if keys[pygame.K_w]:
            self.camera_position[2] -= self.camera_speed
        if keys[pygame.K_s]:
            self.camera_position[2] += self.camera_speed

        # Esquerda / Direita
        if keys[pygame.K_a]:
            self.camera_position[0] -= self.camera_speed
        if keys[pygame.K_d]:
            self.camera_position[0] += self.camera_speed
        
        # Cima / Baixo
        if keys[pygame.K_e]:
            self.camera_position[1] += self.camera_speed
        if keys[pygame.K_q]:
            self.camera_position[1] -= self.camera_speed