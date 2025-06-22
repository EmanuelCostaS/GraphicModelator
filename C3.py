import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from camera.camera import configure_projection_matrix, Camera
import math
from transformations import translation_matrix_4x4, rotation_matrix_4x4

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
    # Define um material azul para o objeto
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.004, 0.2, 0.3, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.004, 0.408, 0.627, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 32.0)

def hexagon(radius, height, num_segments, position, color):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    
    # Set color
    r, g, b = color
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [r, g, b, 1.0])

    top_vertices = []
    bottom_vertices = []
    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        top_vertices.append((x, y, height / 2.0))
        bottom_vertices.append((x, y, -height / 2.0))

    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)
    for vertex in top_vertices:
        glVertex3f(*vertex)
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, -1.0)
    for vertex in reversed(bottom_vertices):
        glVertex3f(*vertex)
    glEnd()

    glBegin(GL_QUADS)
    for i in range(num_segments):
        v1_top = top_vertices[i]
        v2_bottom = bottom_vertices[i]
        v3_bottom = bottom_vertices[(i + 1) % num_segments]
        v4_top = top_vertices[(i + 1) % num_segments]
        normal_angle = 2 * math.pi * (i + 0.5) / num_segments
        normal_x = math.cos(normal_angle)
        normal_y = math.sin(normal_angle)
        glNormal3f(normal_x, normal_y, 0.0)
        glVertex3f(*v1_top)
        glVertex3f(*v2_bottom)
        glVertex3f(*v3_bottom)
        glVertex3f(*v4_top)
    glEnd()

    glPopMatrix()

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

    glRotatef(30, 0, 0, 1)
    hexagon(1.5, 2, 6, [0, 0, 0], (1, 1, 1))     
    hexagon(2.7, 2, 6, [0, 0, -2], (0.004, 0.404, 0.62)) 
    hexagon(3.9, 2, 6, [0, 0, -4], (1, 1, 1))   
    hexagon(6.9, 2, 6, [0, 0, -6], (0.553, 0.557, 0.573))
    hexagon(8.1, 2, 6, [0, 0, -8], (1, 1, 1))     
    hexagon(15.8, 2, 6, [0, 0, -10], (0.004, 0.404, 0.62)) 
    hexagon(17, 2, 6, [0, 0, -12], (1, 1, 1))   
    hexagon(17.6, 2, 6, [0, 0, -14], (0.553, 0.557, 0.573))  

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
        
        # CHANGE 3: The call to draw_scene is simple again.
        draw_scene(camera, is_perspective, display[0], display[1])
        
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()