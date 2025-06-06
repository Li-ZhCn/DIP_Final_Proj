import skimage
from skimage import io
from skimage.feature import canny
from skimage.transform import probabilistic_hough_line
import matplotlib.pyplot as plt

img_path = 'img/bank.bmp'
img = skimage.io.imread(img_path)

plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.axis('off')
io.imshow(img)

plt.subplot(1, 2, 2)
plt.title('Probabilistic Hough')
plt.axis('off')
edges = canny(img, 2, 1, 25)
lines = probabilistic_hough_line(edges, threshold=10, line_length=10,
                                 line_gap=3)

plt.imshow(edges * 0)
for line in lines:
    p0, p1 = line
    plt.plot((p0[0], p1[0]), (p0[1], p1[1]))

plt.tight_layout()
plt.show()