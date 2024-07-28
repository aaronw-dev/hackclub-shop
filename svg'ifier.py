import xml.etree.ElementTree as ET
import os

glyphs = eval(open("glyphs", "r").read())
sizes = [16, 32, 64, 128, 512, 1024]

for size in sizes:
    for key in glyphs.keys():
        value = glyphs[key]
        valuexml = ET.XML(value)
        ET.indent(valuexml)
        svgproperties = {
            "fill-rule": "evenodd",
            "cliprule": "evenodd",
            "stroke-linejoin": "round",
            "stroke-miterlimit": "1.414",
            "xmlns": "http://www.w3.org/2000/svg",
            "aria-label": "bolt-docs",
            "viewBox": "0 0 32 32",
            "preserveAspectRatio": "xMidYMid meet",
            "fill": "currentColor",
            "width": "48",
            "height": "48"
        }
        attributes = " ".join(
            f'{key} = "{svgproperties[key]}"' for key in svgproperties)
        finalstring = ET.tostring(valuexml, encoding='unicode')
        finalstring = f'<svg {attributes}> \n' + finalstring
        finalstring += '\n</svg>'
        with open(f"icons/svg/{key}.svg", "w") as file:
            file.write(finalstring)
            file.close()
            if not os.path.exists(f"icons/png/{size}"):
                os.mkdir(f"icons/png/{size}")
            os.system(
                f"magick convert -background none -size {size}x{size} icons/svg/{key}.svg icons/png/{size}/{key}.png"
            )
            print(f"Rendered icons/png/{size}/{key}.png")
