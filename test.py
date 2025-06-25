import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from camera.camera import configure_projection_matrix, Camera
import math
from transformations import translation_matrix_4x4, rotation_matrix_4x4, scaling_matrix_4x4
import numpy as np

def init_opengl(width, height):
    # Configurações básicas da OpenGL
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)

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
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.004, 0.2, 0.3, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.004, 0.408, 0.627, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 32.0)

def bresenham_line(x1, y1, x2, y2):
    """
    Calcula os pontos de uma linha 2D usando o algoritmo de Bresenham
    e os retorna um a um (usando yield).
    """
    x1, y1, x2, y2 = int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        yield (x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# VERSÃO FINAL DA FUNÇÃO HEXAGON
def hexagon(radius, height, position, color, scale_factor=1.0, squash_factor=0.85, curve_angle_deg=60, curve_steps=15, draw_lines=True, line_color=(1,1,1), line_width=2.0):
    
    glPushMatrix()
    
    scale_mat = scaling_matrix_4x4(scale_factor, scale_factor, scale_factor)
    glMultMatrixf(scale_mat.T)
    translation_mat = translation_matrix_4x4(position[0], position[1], position[2])
    glMultMatrixf(translation_mat.T)
    
    r, g, b = color
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [r, g, b, 1.0])

    # --- LÓGICA DE VÉRTICES FINAL E CORRIGIDA (AGORA COM OS ÍNDICES CERTOS) ---
    num_segments = 6
    # Giro inicial de 30 graus para deixar o hexágono "em pé"
    angle_offset = math.pi / 6
    angles = [angle_offset + (2 * math.pi * i / num_segments) for i in range(num_segments)]

    # Parâmetros de ajuste
    squash_factor = 0.85
    # Índices CORRETOS dos cantos a serem curvados no escudo (topo esquerdo, inferior esquerdo, ambos da direita)
    curved_indices = {0, 2, 3, 5}
    curve_angle_deg = 60

    top_vertices = []
    bottom_vertices = []

    for i, angle in enumerate(angles):
        current_radius = radius
        # Achata os vértices de TOPO (índice 1) e BASE (índice 4)
        if i == 1 or i == 4:
            current_radius = radius * squash_factor

        if i in curved_indices:
            start = angle - math.radians(curve_angle_deg / 2)
            end = angle + math.radians(curve_angle_deg / 2)
            for t in np.linspace(start, end, curve_steps):
                x = current_radius * math.cos(t)
                y = current_radius * math.sin(t)
                top_vertices.append((x, y, height / 2.0))
                bottom_vertices.append((x, y, -height / 2.0))
        else: # Vértices retos
            x = current_radius * math.cos(angle)
            y = current_radius * math.sin(angle)
            top_vertices.append((x, y, height / 2.0))
            bottom_vertices.append((x, y, -height / 2.0))

    # --- DESENHO DAS FACES COM TRIANGLE_FAN ---
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, height / 2.0)
    for vertex in top_vertices:
        glVertex3f(*vertex)
    glVertex3f(*top_vertices[0])
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(0.0, 0.0, -height / 2.0)
    for vertex in reversed(bottom_vertices):
        glVertex3f(*vertex)
    glVertex3f(*bottom_vertices[0])
    glEnd()
    
    n = len(top_vertices)
    glBegin(GL_QUADS)
    for i in range(n):
        v1_top = top_vertices[i]
        v2_bottom = bottom_vertices[i]
        v3_bottom = bottom_vertices[(i + 1) % n]
        v4_top = top_vertices[(i + 1) % n]
        normal_angle = math.atan2(v1_top[1], v1_top[0])
        glNormal3f(math.cos(normal_angle), math.sin(normal_angle), 0.0)
        glVertex3f(*v1_top)
        glVertex3f(*v2_bottom)
        glVertex3f(*v3_bottom)
        glVertex3f(*v4_top)
    glEnd()

    # Linhas com Rasterização Bresenham
    if draw_lines:
        glDisable(GL_LIGHTING)
        line_indices = [0, 2, 4]
        # Ângulos originais (sem o offset) para as linhas ficarem no formato "Y" correto
        original_angles = [2 * math.pi * i / num_segments for i in range(num_segments)]
        z_line = height / 2.0 + 0.05  # Pra ficar um pouco acima do topo do hexágono
        glColor3f(*line_color)
        glPointSize(line_width)
        rasterization_scale = 100.0
        glBegin(GL_POINTS)
        for i in line_indices:
            x2 = radius * math.cos(original_angles[i])
            y2 = radius * math.sin(original_angles[i])
            x1, y1 = 0.0, 0.0
            points = bresenham_line(x1 * rasterization_scale, y1 * rasterization_scale, x2 * rasterization_scale, y2 * rasterization_scale)
            for px, py in points:
                glVertex3f(px / rasterization_scale, py / rasterization_scale, z_line)
        glEnd()
        glEnable(GL_LIGHTING)

    glPopMatrix()


# FUNÇÃO DRAW_SCENE FINAL
def draw_scene(camera, is_perspective, width, height):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    configure_projection_matrix(width, height, not is_perspective)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # --- Camera transform ---
    rotation_camera_x = camera.camera_rotation[0]
    rotation_camera_y = camera.camera_rotation[1]
    rotation_camera = rotation_matrix_4x4(rotation_camera_x, 'x') * rotation_matrix_4x4(rotation_camera_y, 'y')
    glMultMatrixf(rotation_camera.T)
    camera_pos = camera.camera_position
    translation = translation_matrix_4x4(-camera_pos[0], -camera_pos[1], -camera_pos[2])
    glMultMatrixf(translation.T)

    # A ROTAÇÃO DA CENA FOI REMOVIDA DAQUI, POIS O HEXÁGONO AGORA SE ORIENTA SOZINHO

    # --- Fator de escala único para todos os objetos ---
    scale_factor = 0.9 

    # --- Parâmetros de ajuste para a forma do escudo ---
    squash = 0.85 # Fator de achatamento (0.8 a 1.0)
    curve = 60   # Ângulo da curva (45 a 75)

    # --- Chamadas de desenho ---
    hexagon(1.5, 2, [0, 0, 0], (1, 1, 1), scale_factor=scale_factor, squash_factor=squash, curve_angle_deg=curve, line_color=(1,1,1), line_width=20.0)
    hexagon(2.7, 2, [0, 0, -2], (0.004, 0.404, 0.62), scale_factor=scale_factor, squash_factor=squash, curve_angle_deg=curve, line_color=(1,1,1), line_width=20.0)
    hexagon(3.9, 2, [0, 0, -4], (1, 1, 1), scale_factor=scale_factor, squash_factor=squash, curve_angle_deg=curve, line_color=(1,1,1), line_width=20.0)
    hexagon(6.9, 2, [0, 0, -6], (0.553, 0.557, 0.573), scale_factor=scale_factor, squash_factor=squash, curve_angle_deg=curve, line_color=(1,1,1), line_width=20.0)
    hexagon(8.1, 2, [0, 0, -8], (1, 1, 1), scale_factor=scale_factor, squash_factor=squash, curve_angle_deg=curve, line_color=(1,1,1), line_width=20.0)
    hexagon(15.8, 2, [0, 0, -10], (0.004, 0.404, 0.62), scale_factor=scale_factor, squash_factor=squash, curve_angle_deg=curve, line_color=(1,1,1), line_width=20.0)
    hexagon(17, 2, [0, 0, -12], (1, 1, 1), scale_factor=scale_factor, squash_factor=squash, curve_angle_deg=curve, line_color=(1,1,1), line_width=20.0)
    hexagon(17.6, 2, [0, 0, -14], (0.2, 0.2, 0.2), scale_factor=scale_factor, squash_factor=squash, curve_angle_deg=curve, line_color=(1,1,1), line_width=20.0)

    pygame.display.flip()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("CG FURG - Vários Hexágonos")

    init_opengl(*display)
    
    running = True
    is_perspective = True
    camera = Camera()
    camera.camera_position[2] = 8 
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_perspective = not is_perspective
                    print(f"Modo de projeção: {'Perspectiva' if is_perspective else 'Ortogonal'}")
        
        camera.update()
        
        draw_scene(camera, is_perspective, display[0], display[1])
        
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()