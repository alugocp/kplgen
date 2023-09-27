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
        for i, pair in enumerate(img.getcolors()):
            _, color = pair
            r, g, b = color
            r /= 255
            g /= 255
            b /= 255
            x = i % 20
            y = int(i / 20)
            output.write(f' <ColorSetEntry id="{i}" name="Color {i}" bitdepth="U8" spot="false">\n')
            output.write(f'  <RGB r="{r}" b="{b}" g="{g}" space="sRGB-elle-V2-srgbtrc.icc"/>\n')
            output.write(f'  <Position column="{x}" row="{y}"/>\n')
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