'''
This file handles rendering and file output.
'''
import struct
import random
def save_image(image, filename):
    with open(filename, 'wb') as file:
        file.write(struct.pack('B', 66))  # BMP magic number
        file.write(struct.pack('B', 77))
        file.write(struct.pack('I', 54 + 3 * len(image[0]) * len(image)))  # File size
        file.write(struct.pack('I', 0))  # Reserved
        file.write(struct.pack('I', 54))  # Offset to image data
        file.write(struct.pack('I', 40))  # Header size
        file.write(struct.pack('I', len(image[0])))  # Image width
        file.write(struct.pack('I', len(image)))  # Image height
        file.write(struct.pack('H', 1))  # Number of color planes
        file.write(struct.pack('H', 24))  # Bits per pixel
        file.write(struct.pack('I', 0))  # Compression method
        file.write(struct.pack('I', 0))  # Image size
        file.write(struct.pack('I', 0))  # Horizontal resolution
        file.write(struct.pack('I', 0))  # Vertical resolution
        file.write(struct.pack('I', 0))  # Number of colors in palette
        file.write(struct.pack('I', 0))  # Number of important colors
        for row in image:
            for pixel in row:
                file.write(struct.pack('B', int(pixel.b * 255)))  # Blue
                file.write(struct.pack('B', int(pixel.g * 255)))  # Green
                file.write(struct.pack('B', int(pixel.r * 255)))  # Red
def normalize(vector):
    length = math.sqrt(vector.x * vector.x + vector.y * vector.y + vector.z * vector.z)
    return Vector(vector.x / length, vector.y / length, vector.z / length)