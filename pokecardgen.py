import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import binary_fill_holes

# Generation 1 Types & HEX Colors
GEN1_TYPE_COLORS = {
    "NORMAL":   "#A8A878",
    "FIRE":     "#F08030",
    "WATER":    "#6890F0",
    "GRASS":    "#78C850",
    "ELECTRIC": "#F8D030",
    "ICE":      "#98D8D8",
    "FIGHTING": "#C03028",
    "POISON":   "#A040A0",
    "GROUND":   "#E0C068",
    "FLYING":   "#A890F0",
    "PSYCHIC":  "#F85888",
    "BUG":      "#A8B820",
    "ROCK":     "#B8A038",
    "GHOST":    "#705898",
    "DRAGON":   "#7038F8"
}

def hex_to_rgb(hex_str):
    """Converts HEX string to normalized float RGB tuple (0.0 to 1.0) for Matplotlib."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def loadcard(filename):
    '''
    Load card sprite using plt.imread and clear only exterior white pixels 
    using flood-fill/hole-filling to preserve internal whites (e.g. eyes).
    '''
    img = plt.imread(filename)
    
    # Ensure float32 representation in range [0, 1] with RGBA
    if img.dtype == np.uint8:
        img = img.astype(np.float32) / 255.0
    
    if img.shape[2] == 3:
        # Append alpha channel if RGB
        alpha = np.ones((img.shape[0], img.shape[1], 1), dtype=np.float32)
        img = np.concatenate([img, alpha], axis=-1)
        
    data = img.copy()
    
    # Identify white/near-white pixels (RGB >= 0.94 (~240/255))
    white_mask = (data[:, :, 0] >= 0.94) & (data[:, :, 1] >= 0.94) & (data[:, :, 2] >= 0.94)
    
    # Non-white pixels mark the sprite's interior structure
    non_white = ~white_mask
    
    # binary_fill_holes fills enclosed regions (like eyes/body interior).
    # The inverted mask isolating outer connected background stays False.
    filled_structure = binary_fill_holes(non_white)
    
    # Outer white background pixels are white AND not part of the filled structure
    background_mask = white_mask & (~filled_structure)
    
    # Set background alpha to 0
    data[background_mask, 3] = 0.0
    
    return data

def create_gradient_template(color1_rgb, color2_rgb=None, width=28, height=32):
    '''
    Generates a 28x32 RGBA float array containing a diagonal color gradient.
    '''
    arr = np.ones((height, width, 4), dtype=np.float32)
    
    if color2_rgb is None:
        arr[:, :, :3] = color1_rgb
        return arr

    for y in range(height):
        for x in range(width):
            ratio = (x / (width - 1) + y / (height - 1)) / 2.0
            r = color1_rgb[0] * (1 - ratio) + color2_rgb[0] * ratio
            g = color1_rgb[1] * (1 - ratio) + color2_rgb[1] * ratio
            b = color1_rgb[2] * (1 - ratio) + color2_rgb[2] * ratio
            arr[y, x, :3] = [r, g, b]
            
    return arr

def cardtypegenerator(output_dir="./templates"):
    '''
    Generate type templates saved via plt.imsave for all Gen 1 combinations.
    '''
    os.makedirs(output_dir, exist_ok=True)
    types = list(GEN1_TYPE_COLORS.keys())
    generated_templates = {}

    for i, type1 in enumerate(types):
        # 1. Single-Type Templates
        rgb1 = hex_to_rgb(GEN1_TYPE_COLORS[type1])
        single_arr = create_gradient_template(rgb1)
        
        filepath = os.path.join(output_dir, f"{type1}.png")
        plt.imsave(filepath, single_arr)
        generated_templates[type1] = single_arr

        # 2. Dual-Type Templates
        for type2 in types[i+1:]:
            rgb2 = hex_to_rgb(GEN1_TYPE_COLORS[type2])
            dual_arr = create_gradient_template(rgb1, rgb2)
            
            dual_filepath = os.path.join(output_dir, f"{type1}_{type2}.png")
            plt.imsave(dual_filepath, dual_arr)
            generated_templates[f"{type1}_{type2}"] = dual_arr

    return generated_templates
import numpy as np
import matplotlib.pyplot as plt

def create_font_library():
    """
    Creates a dictionary mapping characters (a-z, 0-9) to 2D numpy arrays.
    1 represents a drawn black pixel, 0 represents background.
    Font grid height is fixed at 3 pixels; width is 3 (or 2 for narrow characters).
    """
    font = {}
    
    # helper to convert string grid to binary numpy array
    def parse_char(lines):
        return np.array([[1 if c == '#' else 0 for c in line] for line in lines], dtype=np.uint8)

    # Numbers 0-9 (Height 3)
    font['0'] = parse_char(["###", "# #", "###"])
    font['1'] = parse_char([" #", " #", " #"])  # 2x3
    font['2'] = parse_char(["###", "  #", "###"])
    font['3'] = parse_char(["###", " ##", "###"])
    font['4'] = parse_char(["# #", "###", "  #"])
    font['5'] = parse_char(["###", "## ", "###"])
    font['6'] = parse_char(["#  ", "###", "###"])
    font['7'] = parse_char(["###", "  #", "  #"])
    font['8'] = parse_char(["###", "###", "###"])
    font['9'] = parse_char(["###", "###", "  #"])

    # Letters a-z (Height 3, mixed 3x3 and 2x3)
    font['a'] = parse_char(["## ", "###", "# #"])
    font['b'] = parse_char(["#  ", "###", "###"])  # 2x3
    font['c'] = parse_char(["###", "#  ", "###"])
    font['d'] = parse_char(["  #", " ##", " ##"])  # 2x3
    font['e'] = parse_char(["###", "## ", "###"])
    font['f'] = parse_char([" ##", " # ", " # "])
    font['g'] = parse_char(["###", "# #", " ##"])
    font['h'] = parse_char(["# #", "###", "# #"])
    font['i'] = parse_char(["#", "#", "#"])        # 1x3
    font['j'] = parse_char(["  #", "  #", "## "])
    font['k'] = parse_char(["# #", "## ", "# #"])
    font['l'] = parse_char(["# ", "# ", "##"])    # 2x3
    font['m'] = parse_char(["###", "###", "# #"])
    font['n'] = parse_char(["## ", "# #", "# #"])
    font['o'] = parse_char(["###", "# #", "###"])
    font['p'] = parse_char(["## ", "## ", "#  "])  # 2x3
    font['q'] = parse_char([" ##", " ##", "  #"])  # 2x3
    font['r'] = parse_char(["## ", "#  ", "#  "])  # 2x3
    font['s'] = parse_char([" ##", " # ", "## "])
    font['t'] = parse_char(["###", " # ", " # "])
    font['u'] = parse_char(["# #", "# #", "###"])
    font['v'] = parse_char(["# #", "# #", " # "])
    font['w'] = parse_char(["# #", "###", "###"])
    font['x'] = parse_char(["# #", " # ", "# #"])
    font['y'] = parse_char(["# #", "###", "  #"])
    font['z'] = parse_char(["###", " # ", "###"])

    return font

def draw_text_test(filename="font_test.png"):
    '''
    Generates a test PNG with numbers 0-9 and letters a-z rendered
    in black on a white background with 1px spacing.
    '''
    font = create_font_library()
    
    # Test lines to render
    line1 = "0123456789"
    line2 = "abcdefghijklm"
    line3 = "nopqrstuvwxyz"
    lines = [line1, line2, line3]
    
    spacing = 1  # 1 pixel gap between characters and lines
    char_height = 3
    
    # Calculate required image width and height
    max_width = 0
    for line in lines:
        width = sum(font[ch].shape[1] + spacing for ch in line if ch in font)
        if width > max_width:
            max_width = width
            
    total_height = len(lines) * char_height + (len(lines) + 1) * spacing
    total_width = max_width + spacing

    # Initialize canvas with white background (RGB float 1.0)
    canvas = np.ones((total_height, total_width, 3), dtype=np.float32)

    # Render characters line by line
    y_offset = spacing
    for line in lines:
        x_offset = spacing
        for ch in line:
            if ch in font:
                glyph = font[ch]
                gh, gw = glyph.shape
                
                # Draw black pixels where glyph matrix is 1
                for gy in range(gh):
                    for gx in range(gw):
                        if glyph[gy, gx] == 1:
                            canvas[y_offset + gy, x_offset + gx] = [0.0, 0.0, 0.0]
                            
                x_offset += gw + spacing
        y_offset += char_height + spacing
    # plot image
    plt.imshow(canvas)
    plt.show()

    # Save output image
    plt.imsave(filename, canvas)
    print(f"Font test image saved to '{filename}' ({total_width}x{total_height} px).")

if __name__ == "__main__":
    draw_text_test()