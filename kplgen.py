import sys
from PIL import Image
from zipfile import ZipFile

'''
Generates a .kpl file from the given image
'''
def kpl_generate(filepath):
    name = '.'.join(filepath.split('/')[-1].split('.')[:-1])
    img = Image.open(filepath)

    # Convert the image to RGB format (in case it's palette based)
    img = img.convert('RGB')

    # Generate the colorset.xml component of the .kpl file
    with open('res/colorset.xml', 'w', encoding = 'utf-8') as output:

        # Open the top-level XML tag
        output.write(f'<ColorSet name="{name}" rows="20" version="1.0" readonly="false" comment="" columns="16">\n')

        # Generate an entry for each RGB color in the input image
        recorded_colors = set()
        width, height = img.size
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))
                if (r, g, b) not in recorded_colors:
                    recorded_colors.add((r, g, b))
                    r /= 255
                    g /= 255
                    b /= 255

                    # Calculate this color entry's index, column, and row
                    i = len(recorded_colors) - 1
                    col = i % 20
                    row = int(i / 20)

                    # Write this color entry in colorset.xml
                    output.write(f' <ColorSetEntry id="{i}" name="Color {i}" bitdepth="U8" spot="false">\n')
                    output.write(f'  <RGB r="{r}" b="{b}" g="{g}" space="sRGB-elle-V2-srgbtrc.icc"/>\n')
                    output.write(f'  <Position column="{col}" row="{row}"/>\n')
                    output.write(f' </ColorSetEntry>\n')

        # Close the top-level XML tag
        output.write('</ColorSet>\n')

    # Write files in res to the .kpl file
    with ZipFile(f'{name}.kpl', 'w') as zf:
        for filepath in ['colorset.xml', 'mimetype', 'profiles.xml', 'sRGB-elle-V2-srgbtrc.icc']:
            with open(f'res/{filepath}', 'rb') as src:
                with zf.open(filepath, 'w') as f:
                    f.write(src.read())

if __name__ == '__main__':
    # User must provide a filepath
    if len(sys.argv) < 2:
        print('Usage: python3 kplgen.py path/to/image')
        sys.exit(1)

    # run our main function
    kpl_generate(sys.argv[1])