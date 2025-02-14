from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance
from math import sqrt, ceil

WIDTH = 84
HEIGHT = 100
NW_CELLS = 6
NH_CELLS = 10
LINE = "+============================+"

# 25P = 1H = 10K

class ImageProcessor:
    def __init__(self, url):
        self.xPixelsBefore = None
        self.image_numerized=None
        self.yPixelsBefore = None
        self.nCol = None
        self.nRow = None
        self.nColPxl = None
        self.nRowPxl = None
        self.xPixels = None
        self.yPixels = None

        try:
            image = Image.open(url)
            try:
                bg = Image.new("RGB", image.size, (255, 255, 255))
                bg.paste(image, image)
                self.image = bg
            except:
                self.image = image.convert('RGB')
        except:
            print("URL is not valid, cannot import this")

    def resize_image(self):
        resized_image = self.image.resize((self.xPixelsBefore,self.yPixelsBefore))
        self.image = Image.new("RGB", (self.xPixels, self.yPixels), (255,255,255))
        self.image.paste(resized_image, ((self.xPixels-self.xPixelsBefore)//2,(self.yPixels-self.yPixelsBefore)//2))

    def get_image_soluce(self):
        new_img = Image.new('RGB', self.image.size, (255, 255, 255))

        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                pixel = self.image.getpixel((x, y))
                if pixel < 127:
                    new_img.putpixel((x, y), (0, 0, 0))
        return new_img

    def process_image_numerized(self):
        enhancer = ImageEnhance.Contrast(self.image)
        contrasted = enhancer.enhance(10.0)
        self.image = ImageOps.grayscale(contrasted)
        N = 20
        new_img = Image.new('RGB', (self.image.size[0] * N, self.image.size[1] * N + 3), (255, 255, 255))
        font = ImageFont.truetype("C:\Windows\Fonts\Verdanab.ttf", 17)
        draw = ImageDraw.Draw(new_img)

        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                pixel = self.image.getpixel((x, y))
                if pixel < 127:
                    draw.text((x * N, y * N), "0", (0, 0, 0), font=font)
                else:
                    draw.text((x * N, y * N), "1", (0, 0, 0), font=font)
        self.image_numerized = new_img

    def get_cropped_image(self):
        draw = ImageDraw.Draw(self.image_numerized)
        for i in range(1, self.nCol):
            draw.line([(i * self.nColPxl - 2, 0), (i * self.nColPxl - 2, self.image_numerized.size[1] - 1)], fill="black", width=2)
        for i in range(1, self.nRow):
            draw.line([(0, i * self.nRowPxl + 2), (self.image_numerized.size[0] - 1, i * self.nRowPxl + 2)], fill="black", width=2)
        return self.image_numerized

    def process_image_dim(self, nbCells, nbPixels):
        ratio = self.image.size[0] / self.image.size[1]
        cols_approx = sqrt(nbCells) * ratio
        k = sqrt(nbPixels/self.image.size[0]*self.image.size[1])
        self.xPixelsBefore = round(self.image.size[0]*k)
        self.yPixelsBefore = round(self.image.size[1]*k)
        self.nCol = round(cols_approx)
        self.nRow = round(nbCells / self.nCol)
        self.nColPxl = ceil(self.image.size[0] / self.nCol)
        self.nRowPxl = ceil(self.image.size[1] / self.nRow)
        self.xPixels = self.image.size[0] - (self.nColPxl * self.nCol)
        self.yPixels = self.image.size[1] - (self.nRowPxl * self.nRow)

# Charger l'image
imgProcess = ImageProcessor("panda.png")
print("Image loaded")
imgProcess.process_image_dim(60,8400)
print("Dims calculated")
print(imgProcess.xPixelsBefore)
print(imgProcess.yPixelsBefore)
imgProcess.resize_image()
print("Resize Image")
imgProcess.process_image_numerized()
print("Image wit numbers generated")
imgProcess.get_cropped_image().save("numerized.png")
print("Bite")
imgProcess.get_image_soluce().save("soluce.png")