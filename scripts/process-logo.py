from PIL import Image

src = r"C:\Users\16704\AppData\Local\Temp\2e61e736-571e-48d5-8ae8-a01164cfcd69.78290f0daa.png"
dst = "store-assets/icon.png"

im = Image.open(src)
print("source size:", im.size, "mode:", im.mode)

if im.mode != "RGBA":
    im = im.convert("RGBA")

pixels = im.load()
for y in range(im.height):
    for x in range(im.width):
        r, g, b, a = pixels[x, y]
        # 去除纯白/近白背景
        if r > 245 and g > 245 and b > 245:
            pixels[x, y] = (r, g, b, 0)

# 缩放为 128x128
icon = im.resize((128, 128), Image.LANCZOS)
icon.save(dst)
print("saved", dst, "size:", icon.size, "mode:", icon.mode)
