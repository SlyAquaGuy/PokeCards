import os
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import binary_fill_holes

# Generation 1 Types & HEX Colors
GEN1_TYPE_COLORS = {
    "NOR":   "#A8A878",
    "FRE":   "#F08030",
    "WTR":   "#6890F0",
    "GRS":   "#78C850",
    "ELE":   "#F8D030",
    "ICE":   "#98D8D8",
    "FIG":   "#C03028",
    "PSN":   "#A040A0",
    "GRD":   "#E0C068",
    "FLY":   "#A890F0",
    "PSY":   "#F85888",
    "BUG":   "#A8B820",
    "RCK":   "#B8A038",
    "GST":   "#705898",
    "DRG":   "#7038F8"
}

def hex_to_rgb(hex_str):
    """Converts HEX string to normalized float RGB tuple (0.0 to 1.0) for Matplotlib."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def hex_to_rgb_array(hex_str):
    """Converts HEX string to float RGBA numpy array [0.0, 1.0]"""
    hex_str = hex_str.lstrip('#')
    return np.array([int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)] + [1.0], dtype=np.float32)

def get_darkened_type_color(type_code, factor=0.45):
    """Fetches type color and darkens it by multiplying RGB channels."""
    hex_val = GEN1_TYPE_COLORS.get(type_code, "#000000")
    rgb = hex_to_rgb_array(hex_val)
    rgb[:3] = rgb[:3] * factor  # Reduce brightness while preserving hue
    return rgb

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
            ratio = (((width-x) / (width - 1)) + y / (height - 1)) / 2.0
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

    # Digits 0-9
    font['0'] = parse_char(["###", "# #", "###"])
    font['1'] = parse_char(["## ", " # ", "###"])
    font['2'] = parse_char(["## ", " # ", " ##"])
    font['3'] = parse_char(["###", " ##", "  #"])
    font['4'] = parse_char(["# #", "###", "  #"])
    font['5'] = parse_char([" ##", " # ", "## "])
    font['6'] = parse_char(["#  ", "###", "###"])
    font['7'] = parse_char(["###", "  #", "  #"])
    font['8'] = parse_char(["## ", "###", " ##"])
    font['9'] = parse_char(["###", "###", "  #"])

    # Uppercase & Lowercase A-Z / a-z (Matching the provided font image)
    font['A'] = font['a'] = parse_char([" # ", "###", "# #"])
    font['B'] = font['b'] = parse_char(["## ", "###", "###"])
    font['C'] = font['c'] = parse_char(["###", "#  ", "###"])
    font['D'] = font['d'] = parse_char(["## ", "# #", "## "])
    font['E'] = font['e'] = parse_char(["###", "## ", "###"])
    font['F'] = font['f'] = parse_char(["###", "## ", "#  "])
    font['G'] = font['g'] = parse_char(["###", "# #", "## "])
    font['H'] = font['h'] = parse_char(["# #", "###", "# #"])
    font['I'] = font['i'] = parse_char(["###", " # ", "###"])
    font['J'] = font['j'] = parse_char(["  #", "  #", "## "])
    font['K'] = font['k'] = parse_char(["# #", "## ", "# #"])
    font['L'] = font['l'] = parse_char(["#  ", "#  ", "###"])
    font['M'] = font['m'] = parse_char(["###", "###", "# #"])
    font['N'] = font['n'] = parse_char(["## ", "# #", "# #"])
    font['O'] = font['o'] = parse_char(["###", "# #", "###"])
    font['P'] = font['p'] = parse_char(["##", "##", "# "])
    font['Q'] = font['q'] = parse_char([" # ", "# #", " ##"])
    font['R'] = font['r'] = parse_char(["## ", "## ", "# #"])
    font['S'] = font['s'] = parse_char([" ##", " # ", "## "])
    font['T'] = font['t'] = parse_char(["###", " # ", " # "])
    font['U'] = font['u'] = parse_char(["# #", "# #", "###"])
    font['V'] = font['v'] = parse_char(["# #", "# #", " # "])
    font['W'] = font['w'] = parse_char(["# #", "###", "###"])
    font['X'] = font['x'] = parse_char(["# #", " # ", "# #"])
    font['Y'] = font['y'] = parse_char(["# #", " # ", " # "])
    font['Z'] = font['z'] = parse_char(["## ", " # ", " ##"])
    font[':'] = font[':'] = parse_char(["#", " ", "#"])

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
def get_dominant_color(sprite):
    '''Extracts the most frequent color, ignoring transparent, black, and white.'''
    pixels = sprite[sprite[:, :, 3] > 0.5]
    if len(pixels) == 0:
        return np.array([0., 0., 0., 1.])
        
    rgb_sums = pixels[:, :3].sum(axis=1)
    valid_mask = (rgb_sums > 0.6) & (rgb_sums < 2.7)
    valid_pixels = pixels[valid_mask]
    
    if len(valid_pixels) == 0:
        valid_pixels = pixels
        
    # Bin colors to group subtle shade differences
    binned = np.round(valid_pixels[:, :3] * 10) / 10.0
    unique_colors, counts = np.unique(binned, axis=0, return_counts=True)
    most_common = unique_colors[np.argmax(counts)]
    
    return np.array([most_common[0], most_common[1], most_common[2], 1.0])

def paste_sprite(bg, sprite, x_offset, y_offset):
    '''Safely blends a sprite onto a background given coordinate offsets.'''
    h_bg, w_bg = bg.shape[:2]
    h_s, w_s = sprite.shape[:2]
    
    y1, y2 = max(0, y_offset), min(h_bg, y_offset + h_s)
    x1, x2 = max(0, x_offset), min(w_bg, x_offset + w_s)
    
    y1_s, y2_s = max(0, -y_offset), max(0, -y_offset) + (y2 - y1)
    x1_s, x2_s = max(0, -x_offset), max(0, -x_offset) + (x2 - x1)
    
    if y1 < y2 and x1 < x2:
        bg_slice = bg[y1:y2, x1:x2]
        s_slice = sprite[y1_s:y2_s, x1_s:x2_s]
        alpha_s = s_slice[:, :, 3:4]
        
        bg[y1:y2, x1:x2, :3] = s_slice[:, :, :3] * alpha_s + bg_slice[:, :, :3] * (1 - alpha_s)

def get_text_width(text, font):
    '''Calculates the pixel width of a string including 1px gaps.'''
    w = 0
    for char in text:
        if char == ' ': w += 1 + 1
        elif char in font: w += font[char].shape[1] + 1
        else: w += 3 + 1
    return w - 1 if w > 0 else 0

def draw_text(canvas, text, x, y, font, color=np.array([0.0, 0.0, 0.0, 1.0])):
    '''Renders text directly onto the canvas numpy array.'''
    curr_x = x
    for char in text:
        if char == ' ':
            curr_x += 1
            continue
        if char in font:
            glyph = font[char]
            gh, gw = glyph.shape
            for gy in range(gh):
                for gx in range(gw):
                    cy, cx = y + gy, curr_x + gx
                    if 0 <= cy < canvas.shape[0] and 0 <= cx < canvas.shape[1]:
                        if glyph[gy, gx] == 1:
                            canvas[cy, cx] = color
            curr_x += gw + 1

def generate_pokemon_cards(json_path="pokemon_gen1.json", sprites_dir="./sprites", templates_dir="./templates", output_dir="./cards"):
    '''Main pipeline to generate all Pokemon cards.'''
    os.makedirs(output_dir, exist_ok=True)
    font = create_font_library()

    # White RGBA color for stats (CP/HP)
    WHITE_COLOR = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
    
    with open(json_path, 'r') as f:
        pokemon_data = json.load(f)
    
    type_order = list(GEN1_TYPE_COLORS.keys())
    
    for pkmn in pokemon_data:
        # 1. Fetch Types & Background Gradient Template
        # Ensure dual-types are sorted matching the generator's exact filename logic
        sorted_types = sorted(pkmn['types'], key=lambda t: type_order.index(t))
        template_name = "_".join(sorted_types) + ".png"
        template_path = os.path.join(templates_dir, template_name)
        
        if not os.path.exists(template_path):
            print(f"Missing template: {template_path}")
            continue
            
        card = plt.imread(template_path).copy()
        
        # 2. Load Sprite 
        sprite_filename = f"{pkmn['id']:03d}.png"
        sprite_path = os.path.join(sprites_dir, sprite_filename)
        
        if not os.path.exists(sprite_path):
            print(f"Missing sprite: {sprite_path}")
            continue
            
        sprite = loadcard(sprite_path)
        
        # 3. Create Border from Dominant Color
        #border_color = get_dominant_color(sprite)
        border_color = np.array([0.3, 0.3, 0.3, 1.0], dtype=np.float32)  # grey
        card[0, :] = border_color
        card[-1, :] = border_color
        card[:, 0] = border_color
        card[:, -1] = border_color
        
        # 4. Paste Sprite Centered
        paste_sprite(card, sprite, x_offset=-2, y_offset=0)
        
        # 5. Add Top Text (Types)
        top_text = " ".join(pkmn['types'])
        start_x = 2

        curr_x = start_x
        for t in pkmn['types']:
            dark_color = get_darkened_type_color(t, factor=0.85)
            draw_text(card, t, curr_x, 2, font, color=dark_color)
            curr_x += get_text_width(t, font) + 2  # Advance past word and 1px-spaced space character
        
        # 6. Add Bottom Text (CP and HP)
        bottom_text = f"CP:{pkmn['cp']} HP:{pkmn['hp']}"
        tw_b = get_text_width(bottom_text, font)
        start_x_b = 1
        # y=27 places text exactly 1px above the y=31 bottom border 
        # (27 + 3px font height = 30; gap at 30)
        draw_text(card, bottom_text, start_x_b, 27, font, color=WHITE_COLOR)
        
        # 7. Save File
        out_path = os.path.join(output_dir, f"{pkmn['id']}.png")
        plt.imsave(out_path, card)
        
    print(f"Finished generating cards in {output_dir}")

if __name__ == "__main__":
    generate_pokemon_cards()
