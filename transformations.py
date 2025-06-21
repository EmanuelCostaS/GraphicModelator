


import numpy as np

def scaling_matrix_4x4(sx, sy, sz):
    """
    Generates a 4x4 homogeneous scaling matrix.

    Args:
        sx (float): The scaling factor along the x-axis.
        sy (float): The scaling factor along the y-axis.
        sz (float): The scaling factor along the z-axis.

    Returns:
        numpy.matrix: The 4x4 homogeneous scaling matrix.
    """
    # A scaling matrix has the scaling factors on the main diagonal
    return np.matrix([
        [sx, 0,  0,  0],
        [0,  sy, 0,  0],
        [0,  0,  sz, 0],
        [0,  0,  0,  1]
    ])


def translation_matrix_4x4(tx, ty, tz):
    """
    Generates a 4x4 homogeneous translation matrix.

    Args:
        tx (float): The translation distance along the x-axis.
        ty (float): The translation distance along the y-axis.
        tz (float): The translation distance along the z-axis.

    Returns:
        numpy.matrix: The 4x4 homogeneous translation matrix.
    """
    return np.matrix([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])


def rotation_matrix_4x4(angle, axis="x"):
    """
    Generates a 4x4 homogeneous rotation matrix for a given angle and axis.

    Args:
        angle (float): The angle of rotation in radians.
        axis (str): The axis of rotation ('x', 'y', or 'z').

    Returns:
        numpy.matrix: The 4x4 homogeneous rotation matrix.
    """
    c = np.cos(angle)
    s = np.sin(angle)

    if axis.lower() == "x":
        return np.matrix([
            [1, 0,  0, 0],
            [0, c, -s, 0],
            [0, s,  c, 0],
            [0, 0,  0, 1]
        ])
    elif axis.lower() == "y":
        return np.matrix([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])
    elif axis.lower() == "z":
        return np.matrix([
            [c, -s, 0, 0],
            [s,  c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1]
        ])
    else:
        print("Invalid axis specified. Please use 'x', 'y', or 'z'.")
        return None


def create_transform_matrix(translation, rotation, scale):
    """
    Generates a combined 4x4 homogeneous transformation matrix (model matrix).

    The final transformation is calculated in the order: Translate * Rotate * Scale.
    This means the scaling is applied first, then the rotation, and finally the translation.

    Args:
        translation (tuple): A tuple of (tx, ty, tz) for translation.
        rotation (tuple): A tuple of (angle_rad, axis_str) for rotation.
                          Example: (np.pi / 2, 'y')
        scale (tuple): A tuple of (sx, sy, sz) for scaling.

    Returns:
        numpy.matrix: The combined 4x4 transformation matrix.
    """
    # 1. Unpack the parameters
    tx, ty, tz = translation
    angle, axis = rotation
    sx, sy, sz = scale

    # 2. Create the individual transformation matrices
    trans_matrix = translation_matrix_4x4(tx, ty, tz)
    rot_matrix = rotation_matrix_4x4(angle, axis)
    scale_matrix = scaling_matrix_4x4(sx, sy, sz)

    # 3. Combine the matrices by multiplying them in the correct order.
    # The operations are applied from right to left (Scale, then Rotate, then Translate)
    # This is the standard order for a model matrix.
    model_matrix = trans_matrix * rot_matrix * scale_matrix

    return model_matrix

 


