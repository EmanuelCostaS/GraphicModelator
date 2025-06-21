

import numpy as np

def perspective_matrix_from_scratch(fov_rad, aspect, near, far):
    # Inicializa uma matriz 4x4 com zeros.
    # Usamos np.array para facilitar o envio para o OpenGL depois.
    P = np.zeros((4, 4), dtype=np.float32)

    # Pré-calcula o tangente do meio do FOV
    tan_half_fov = np.tan(fov_rad / 2.0)

    # Preenche os elementos da matriz de acordo com a fórmula

    # Escala X
    P[0, 0] = 1.0 / (aspect * tan_half_fov)

    # Escala Y
    P[1, 1] = 1.0 / tan_half_fov

    # Mapeia Z para o intervalo [-1, 1]
    P[2, 2] = -(far + near) / (far - near)

    # Termo de translação para o mapeamento de Z
    P[2, 3] = -(2.0 * far * near) / (far - near)

    # Define o componente W para a divisão de perspectiva
    P[3, 2] = -1.0

    return np.matrix(P)


def orthogonal_matrix_from_scratch(left, right, bottom, top, near, far):
    """Cria uma matriz de projeção ortogonal 4x4 "do zero"."""
    O = np.zeros((4, 4), dtype=np.float32)
    O[0, 0] = 2.0 / (right - left)
    O[1, 1] = 2.0 / (top - bottom)
    O[2, 2] = -2.0 / (far - near)
    O[0, 3] = -(right + left) / (right - left)
    O[1, 3] = -(top + bottom) / (top - bottom)
    O[2, 3] = -(far + near) / (far - near)
    O[3, 3] = 1.0
    return np.matrix(O)

# --- Exemplo de Uso ---

if __name__ == "__main__":
    # Parâmetros típicos para uma cena
    largura_tela = 800
    altura_tela = 600
    razao_aspecto = largura_tela / altura_tela
    campo_visao_graus = 45.0
    plano_proximo = 0.1
    plano_distante = 100.0

    # Converte o campo de visão para radianos
    campo_visao_rad = np.radians(campo_visao_graus)

    # Cria a matriz de projeção
    projection_matrix = perspective_matrix_from_scratch(
        campo_visao_rad,
        razao_aspecto,
        plano_proximo,
        plano_distante
    )

    print("Matriz de Projeção Perspectiva gerada:\n")
    print(projection_matrix)
 

'''
#version 330 core
layout (location = 0) in vec3 aPos;

// Matrizes recebidas do seu código Python
uniform mat4 model;      // Transforma do espaço do objeto para o espaço do mundo
uniform mat4 view;       // Transforma do espaço do mundo para o espaço da câmera
uniform mat4 projection; // Transforma do espaço da câmera para o espaço de projeção (NDC)

void main()
{
// A ordem de multiplicação é crucial: Projeção * Câmera * Modelo
gl_Position = projection * view * model * vec4(aPos, 1.0);
}
'''