from PIL import Image
import math
import os

# 1. PRINT A MATRIX
def print_matrix(matrix, name):
    print("\n" + name)
    print("-" * len(name))
    for i in range(3):
        print("[ " + f"{matrix[i][0]:8.3f} " + f"{matrix[i][1]:8.3f} " + f"{matrix[i][2]:8.3f} " + "]")

# 2. MATRIX MULTIPLICATION
def multiply_matrices(A, B):
    result = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] = result[i][j] + A[i][k] * B[k][j]
    return result

# 3. TRANSLATION MATRIX
def create_translation_matrix(tx, ty):
    
    matrix = [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]
    return matrix

# 4. ROTATION MATRIX
def create_rotation_matrix(angle):
    
    radians = math.radians(angle)
    cos_value = math.cos(radians)
    sin_value = math.sin(radians)
    matrix = [
        [cos_value, -sin_value, 0],
        [sin_value,  cos_value, 0],
        [0,          0,         1]
    ]
    return matrix

# 5. SCALING MATRIX
def create_scaling_matrix(sx, sy):
    
    matrix = [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]
    return matrix

# 6. SHEARING MATRIX
def create_shearing_matrix(shx, shy):
    matrix = [
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ]
    return matrix

# 7. TRANSFORM A POINT USING HOMOGENEOUS COORDINATES
def transform_point(x, y, matrix):
    
    new_x = (matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * 1)
    new_y = (matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * 1)
    new_w = (matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * 1)

    if new_w != 0:
        new_x = new_x / new_w
        new_y = new_y / new_w

    return new_x, new_y

# 8. FIND NEW IMAGE BOUNDARIES
def find_new_boundaries(image, matrix):
    
    width, height = image.size
    corners = [(0, 0), (width, 0), (0, height), (width, height)]
    transformed_corners = []

    for x, y in corners:
        new_x, new_y = transform_point(x, y, matrix)
        transformed_corners.append((new_x, new_y))

    x_values = []
    y_values = []
    for x, y in transformed_corners:
        x_values.append(x)
        y_values.append(y)

    min_x = min(0, min(x_values))
    max_x = max(width, max(x_values))
    min_y = min(0, min(y_values))
    max_y = max(height, max(y_values))

    new_width = int(math.ceil(max_x - min_x))
    new_height = int(math.ceil(max_y - min_y))

    return (new_width, new_height, min_x, min_y)

# 9. FIND INVERSE OF AN AFFINE MATRIX
def inverse_affine_matrix(matrix):
   
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[0][2]
    d = matrix[1][0]
    e = matrix[1][1]
    f = matrix[1][2]

    determinant = (a * e) - (b * d)
    if abs(determinant) < 0.0000001:
        return None

    inverse = [
        [e / determinant, -b / determinant, (b * f - e * c) / determinant],
        [-d / determinant, a / determinant, (d * c - a * f) / determinant],
        [0, 0, 1]
    ]
    return inverse

# 10. APPLY AFFINE TRANSFORMATION TO IMAGE
def apply_affine_transformation(image, matrix):
    
    (new_width, new_height, min_x, min_y) = find_new_boundaries(image, matrix)
    move_matrix = create_translation_matrix(-min_x, -min_y)
    final_matrix = multiply_matrices(move_matrix, matrix)
    inverse_matrix = inverse_affine_matrix(final_matrix)

    if inverse_matrix is None:
        print("Error: Transformation cannot be applied.")
        return None

    output_image = Image.new("RGB", (new_width, new_height), "white")
    old_width, old_height = image.size

    for y in range(new_height):
        for x in range(new_width):
            original_x, original_y = transform_point(x, y, inverse_matrix)
            original_x = int(round(original_x))
            original_y = int(round(original_y))

            if (0 <= original_x < old_width and 0 <= original_y < old_height):
                pixel = image.getpixel((original_x, original_y))
                output_image.putpixel((x, y), pixel)

    return output_image

# 11. GET A NUMBER FROM USER
def get_number(message, default_value=None):
    
    while True:
        if default_value is not None:
            user_input = input(message + " [Default: " + str(default_value) + "]: ")
            if user_input == "":
                return default_value
        else:
            user_input = input(message)
        
        try:
            value = float(user_input)
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

# 12. SAVE IMAGE
def save_image(image, folder, filename):
    
    path = os.path.join(folder, filename)
    image.save(path)
    print("Saved successfully:", path)

# 13. MAIN PROGRAM
def main():
    print("\n       DATA AUGMENTATION USING AFFINE TRANSFORMATION")
    print("\nThis program performs:")
    print("1. Translation")
    print("2. Rotation")
    print("3. Scaling")
    print("4. Shearing")
    print("5. Combined Transformation")
    print("\nNo NumPy or OpenCV is used.")
    print("Only Pillow is used for image handling.")

    # STEP 1: READ IMAGE
    print("\nSTEP 1: LOAD IMAGE")
    while True:
        filename = input("\nEnter image filename (example: input.jpg): ")
        try:
            image = Image.open(filename)
            image = image.convert("RGB")
            print("\nImage loaded successfully!")
            print("Original image size:", image.size)
            break
        except FileNotFoundError:
            print("\nError: Image file was not found.")
            print("Make sure the image is in the same folder as this Python program.")
        except Exception as error:
            print("\nCould not open the image.")
            print("Error:", error)

    # STEP 2: CREATE OUTPUT FOLDER
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print("\nAll generated images will be saved in:", output_folder)
    print("\nOpening original image...")
    image.show()

    # STEP 3: TRANSLATION
    print("\nSTEP 2: TRANSLATION")
    print("\nTranslation moves the image horizontally and/or vertically.")
    tx = get_number("Enter translation in X direction", 50)
    ty = get_number("Enter translation in Y direction", 30)
    translation = create_translation_matrix(tx, ty)
    print_matrix(translation, "Translation Matrix")
    translated_image = apply_affine_transformation(image, translation)
    if translated_image is not None:
        save_image(translated_image, output_folder, "translated.jpg")

    # STEP 4: ROTATION
    print("\nSTEP 3: ROTATION")
    print("\nPositive angle = counter-clockwise rotation.")
    print("Negative angle = clockwise rotation.")
    angle = get_number("Enter rotation angle in degrees", 30)
    rotation = create_rotation_matrix(angle)
    print_matrix(rotation, "Rotation Matrix")
    rotated_image = apply_affine_transformation(image, rotation)
    if rotated_image is not None:
        save_image(rotated_image, output_folder, "rotated.jpg")

    # STEP 5: SCALING
    print("\nSTEP 4: SCALING")
    print("\nFactor greater than 1 = enlargement.")
    print("Factor between 0 and 1 = reduction.")
    sx = get_number("Enter scaling factor in X direction", 1.5)
    sy = get_number("Enter scaling factor in Y direction", 1.2)
    if sx == 0 or sy == 0:
        print("\nScaling factor cannot be zero.")
        print("Using default values 1.5 and 1.2.")
        sx = 1.5
        sy = 1.2
    scaling = create_scaling_matrix(sx, sy)
    print_matrix(scaling, "Scaling Matrix")
    scaled_image = apply_affine_transformation(image, scaling)
    if scaled_image is not None:
        save_image(scaled_image, output_folder, "scaled.jpg")

    # STEP 6: SHEARING
    print("\nSTEP 5: SHEARING")
    print("\nshx controls horizontal shearing.")
    print("shy controls vertical shearing.")
    shx = get_number("Enter horizontal shearing factor", 0.3)
    shy = get_number("Enter vertical shearing factor", 0)
    shearing = create_shearing_matrix(shx, shy)
    print_matrix(shearing, "Shearing Matrix")
    sheared_image = apply_affine_transformation(image, shearing)
    if sheared_image is not None:
        save_image(sheared_image, output_folder, "sheared.jpg")

    # STEP 7: COMBINED TRANSFORMATION
    print("\nSTEP 6: COMBINED TRANSFORMATION")
    print("\nThis transformation combines:")
    print("Scaling -> Rotation -> Translation")
    print("\nThe final matrix is:")
    print("T x R x S")
    print("\nScaling is applied first,")
    print("then rotation,")
    print("then translation.")
    print("\nEnter combined transformation values:")
    combined_sx = get_number("Scaling X", 1.2)
    combined_sy = get_number("Scaling Y", 1.2)
    combined_angle = get_number("Rotation angle", 30)
    combined_tx = get_number("Translation X", 50)
    combined_ty = get_number("Translation Y", 20)

    combined_scaling = create_scaling_matrix(combined_sx, combined_sy)
    combined_rotation = create_rotation_matrix(combined_angle)
    combined_translation = create_translation_matrix(combined_tx, combined_ty)

    rotation_scaling = multiply_matrices(combined_rotation, combined_scaling)
    combined_matrix = multiply_matrices(combined_translation, rotation_scaling)

    print_matrix(combined_scaling, "Scaling Matrix")
    print_matrix(combined_rotation, "Rotation Matrix")
    print_matrix(combined_translation, "Translation Matrix")
    print_matrix(combined_matrix, "FINAL COMBINED MATRIX (T x R x S)")

    combined_image = apply_affine_transformation(image, combined_matrix)
    if combined_image is not None:
        save_image(combined_image, output_folder, "combined.jpg")

    # STEP 8: DISPLAY ALL RESULTS
    print("\nDISPLAYING RESULTS")
    print("\nOriginal image:")
    image.show()
    if translated_image is not None:
        print("Translated image:")
        translated_image.show()
    if rotated_image is not None:
        print("Rotated image:")
        rotated_image.show()
    if scaled_image is not None:
        print("Scaled image:")
        scaled_image.show()
    if sheared_image is not None:
        print("Sheared image:")
        sheared_image.show()
    if combined_image is not None:
        print("Combined transformation image:")
        combined_image.show()

    # FINAL OUTPUT
    print("\nGenerated images:")
    print("1. translated.jpg")
    print("2. rotated.jpg")
    print("3. scaled.jpg")
    print("4. sheared.jpg")
    print("5. combined.jpg")
    print("\nAll images have been saved inside the 'output' folder.")

# START PROGRAM
if __name__ == "__main__":
    main()