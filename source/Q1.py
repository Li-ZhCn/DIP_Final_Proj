from skimage import io
import matplotlib.pyplot as plt

img_path = 'img/lena.bmp'
img = io.imread(img_path)

# convert the greyscale to certain value
def convert_greyscale_to(img, greyscale):
    interval = 256 // greyscale
    delta_grey = 255 // (greyscale - 1)
    rows, cols = img.shape
    for i in range(rows):
        for j in range(cols):
            img[i][j] = (img[i][j] // interval) * delta_grey

    return img


plt.figure(figsize=(8, 4))

# draw the oiginal image
plt.subplot(2, 4, 1)
plt.title('Original Image')
plt.axis('off')
io.imshow(img)

for i, value in enumerate([128, 64, 32, 16, 8, 4, 2]):
    plt.subplot(2, 4, i+2)
    plt.title('{}'.format(value))
    plt.axis('off')
    out = convert_greyscale_to(img, value)
    io.imshow(out)

plt.tight_layout()
plt.show()