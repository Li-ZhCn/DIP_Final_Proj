import skimage
from skimage import morphology, io
import matplotlib.pyplot as plt

img_path = 'img/rice.bmp'
img = skimage.io.imread(img_path)

plt.figure(figsize=(9, 3))

plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.axis('off')
io.imshow(img)

se = morphology.disk(20)
opening = morphology.opening(img, se)
white_tophat = img - opening

plt.subplot(1, 3, 2)
plt.title('Opening')
plt.axis('off')
io.imshow(opening)

plt.subplot(1, 3, 3)
plt.title('Wight Tophat')
plt.axis('off')
io.imshow(white_tophat)

plt.tight_layout()
plt.show()

