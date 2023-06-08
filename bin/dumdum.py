import hashlib
import colorsys
import random

def generate_hex_color(text):
    # Map words to corresponding colors
    color_map = {
        ''''mountain': '#008000',  # Green
        'ocean': '#0000FF',     # Blue
        'sunset': '#FF4500',    # Orange
        'forest': '#228B22',    # Forest green
        # Add more words and colors as desired'''
    }

    if text in color_map:
        # If the text is a word in the color map, return the corresponding color
        return color_map[text]
    else:
        # If the text is not a word in the color map, generate a hash-based hex color
        random.seed(text)  # Set the seed based on the input text
        random_hex = random.randint(0, 16777215)  # Generate a random number between 0 and 16777215 (0xFFFFFF in decimal)

        hex_color = '#' + format(random_hex, '06x')  # Format the random number as a six-character hex color code

        # Adjust hue based on input text
        hue_value = ord(text[0]) % 360  # Use ASCII value of the first character
        hue_color = colorsys.hls_to_rgb(hue_value / 360, 0.5, 1)
        rgb_color = tuple(int(c * 255) for c in hue_color)

        adjusted_hex_color = '#%02x%02x%02x' % rgb_color

        return hex_color


# Example usage
input_text = input("Enter a text: ")
hex_color = generate_hex_color(input_text)
print(hex_color)
