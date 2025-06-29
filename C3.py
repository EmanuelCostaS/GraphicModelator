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

    # --- Configuração de Iluminação ---
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
        # Retorna o ponto atual em vez de desenhá-lo
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


def hexagon(radius, height, num_segments, position, color, 
                        scale_factor=1.0, 
                        curve_angle_deg=10, 
                        bulge_factor=0.9,  
                        curve_steps=105, 
                        draw_lines=True, line_color=(1,1,1), line_width=2.0):
    """
    Draws a hexagon with specified corners 'bulged' outwards.

    Args:
        bulge_factor (float): Multiplier for the radius of the curved sections only.
                  e            Values > 1.0 make the curve bulge outwards.
    """
     
    glPushMatrix()
    
    # Apply transformations
    scale_mat = scaling_matrix_4x4(scale_factor, scale_factor, scale_factor)
    glMultMatrixf(scale_mat.T)
    translation_mat = translation_matrix_4x4(position[0], position[1], position[2])
    glMultMatrixf(translation_mat.T)
    
    # Set material color
    r, g, b = color
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [r, g, b, 1])

    object_color_rgba = [*color, 1.0]
    object_color_rgba = [c/3 for c in object_color_rgba]

    # 1. Define a propriedade EMISSIVA do material para a cor do objeto.
    glMaterialfv(GL_FRONT, GL_EMISSION, object_color_rgba)

    # --- Vertex Generation ---
    curved_indices = [1, 3, 5]
    angles = [2 * math.pi * i / num_segments for i in range(num_segments)]

    top_vertices = []
    bottom_vertices = []
    
    for i, angle in enumerate(angles):
        if i in curved_indices:
            # --- curved corner ---
            start = angle - math.radians(curve_angle_deg / 2)
            end = angle + math.radians(curve_angle_deg / 2)
            
            # Apply the bulge to the radius for this section only
            current_radius = radius * bulge_factor
            
            for t in np.linspace(start, end, curve_steps):
                x = current_radius * math.cos(t)
                y = current_radius * math.sin(t)
                top_vertices.append((x, y, height / 2.0))
                bottom_vertices.append((x, y, -height / 2.0))
        else:
            # --- sharp corner ---
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            top_vertices.append((x, y, height / 2.0))
            bottom_vertices.append((x, y, -height / 2.0))

    # --- Drawing Logic ---
    # Draw Top Face
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)
    for vertex in top_vertices:
        glVertex3f(*vertex)
    glEnd()

    # Draw Bottom Face
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, -1.0)
    for vertex in reversed(bottom_vertices):
        glVertex3f(*vertex)
    glEnd()
    
    # Draw Side Faces
    n = len(top_vertices)
    glBegin(GL_QUADS)
    for i in range(n):
        v1_top = top_vertices[i]; v2_bottom = bottom_vertices[i]
        v3_bottom = bottom_vertices[(i + 1) % n]; v4_top = top_vertices[(i + 1) % n]
         
        normal_angle = math.atan2(v1_top[1], v1_top[0])
        glNormal3f(math.cos(normal_angle), math.sin(normal_angle), 0.0)
        
        glVertex3f(*v1_top); glVertex3f(*v2_bottom); glVertex3f(*v3_bottom); glVertex3f(*v4_top)
    glEnd()

    # --- RASTERIZAÇÃO ---
    if draw_lines:
      
        glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.0, 0.0, 0.0, 1.0])

        line_indices = [0, 2, 4]
        z_line = height / 2.0 + 0.01
        valid_line_width = max(1.0, line_width)
        glPointSize(valid_line_width) 
        
        rasterization_scale = 80.0
        glBegin(GL_POINTS)
        for i in line_indices:
            current_angle = angles[i]
            x2 = radius * math.cos(current_angle)
            y2 = radius * math.sin(current_angle)
            points = bresenham_line(0, 0, x2 * rasterization_scale, y2 * rasterization_scale)
            for px, py in points:
                glVertex3f(px / rasterization_scale, py / rasterization_scale, z_line)
        glEnd()
  
    glPopMatrix()

# FUNÇÃO DRAW_SCENE ATUALIZADA E SIMPLIFICADA
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

    # --- Rotação geral da cena ---
    angle_in_radians = np.deg2rad(30)
    rotation_mat = rotation_matrix_4x4(angle_in_radians, 'z')
    glMultMatrixf(rotation_mat.T)

    # --- Fator de escala único para todos os objetos ---
    scale_factor = 0.9 

    # --- As chamadas de desenho com a largura da linha corrigida ---
    

    # Hexágono 1
    hexagon(1.5, 2, 6, [0, 0, 0], (1, 1, 1), scale_factor=scale_factor, line_color=(1,1,1), line_width=5.0)
    
    # Hexágono 2
    hexagon(2.7, 2, 6, [0, 0, -2], (0.004, 0.404, 0.62), scale_factor=scale_factor, line_color=(1,1,1), line_width=5.0)
    
    # Hexágono 3
    hexagon(3.9, 2, 6, [0, 0, -4], (1, 1, 1), scale_factor=scale_factor, line_color=(1,1,1), line_width=5.0)
    
    # Hexágono 4
    hexagon(6.9, 2, 6, [0, 0, -6], (0.553, 0.557, 0.573), scale_factor=scale_factor, line_color=(1,1,1), line_width=5.0)
    
    # Hexágono 5
    hexagon(8.1, 2, 6, [0, 0, -8], (1, 1, 1), scale_factor=scale_factor, line_color=(1,1,1), line_width=5.0)
    
    # Hexágono 6
    hexagon(15.8, 2, 6, [0, 0, -10], (0.004, 0.404, 0.62), scale_factor=scale_factor, line_color=(1,1,1), line_width=5.0)
    
    # Hexágono 7
    hexagon(17, 2, 6, [0, 0, -12], (1, 1, 1), scale_factor=scale_factor, line_color=(1,1,1), line_width=0)
    
    # Hexágono 8
    hexagon(17.6, 2, 6, [0, 0, -14], (0.2, 0.2, 0.2), scale_factor=scale_factor, line_color=(1,1,1), line_width=0)

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
    camera.camera_position[2] = 8 # Afasta a câmera para ver os objetos
    
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