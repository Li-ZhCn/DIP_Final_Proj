import skimage
import matplotlib.pyplot as plt
from skimage.filters import butterworth

img_path = 'img/lena.bmp'
img = skimage.io.imread(img_path)

noise = skimage.util.random_noise(img, mode='gaussian', var=0.01)
noise_mode = ['gaussian', 'localvar', 'poisson', 'salt', "pepper", 's&p', 'speckle']

plt.figure(figsize=(8, 8))
plt.subplot(4, 4, 1)
plt.title('Original Image')
skimage.io.imshow(img)
plt.axis('off')

for i, mode in enumerate(noise_mode):
    plt.subplot(4, 4, i+2)
    plt.title('{}'.format(mode))
    plt.axis('off')
    noise = skimage.util.random_noise(img, mode=mode)
    skimage.io.imshow(noise)

    plt.subplot(4, 4, i + 10)
    plt.title('{}+LPF'.format(mode))
    plt.axis('off')
    low_pass = butterworth(noise, 0.05, False, 1, channel_axis=-1)
    skimage.io.imshow(low_pass)


plt.tight_layout()
plt.show()