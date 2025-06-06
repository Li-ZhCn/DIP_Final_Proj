import skimage
from skimage import io, morphology, measure, color
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

img_path = 'img/rice.bmp'
img = skimage.io.imread(img_path)

plt.figure(figsize=(6, 6))

plt.subplot(2, 2, 1)
plt.title('Original Image')
plt.axis('off')
io.imshow(img)

se = morphology.disk(20)
opening = morphology.opening(img, se)
white_tophat = img - opening

thresh = threshold_otsu(white_tophat)
bi = white_tophat > thresh

labels = measure.label(bi, connectivity=2)
labels = morphology.remove_small_objects(labels, min_size=10, connectivity=1)
colored_region = color.label2rgb(labels)

plt.subplot(2, 2, 2)
plt.title('Histogram')
plt.hist(white_tophat.ravel(), bins=256)
plt.axvline(thresh, color='r')

plt.subplot(2, 2, 3)
plt.title('Colored Region')
plt.axis('off')
io.imshow(colored_region)

ax = plt.subplot(2, 2, 4)
plt.title('Marked Region')
plt.axis('off')
io.imshow(img)
for region in measure.regionprops(labels):
    minr, minc, maxr, maxc = region.bbox
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=1)
    ax.add_patch(rect)
    ax.scatter(region.centroid[1], region.centroid[0])
    print(region.centroid)
    # ax.plot(region.centroid)


stat = measure.regionprops_table(labels, properties=('label', 'bbox', 'centroid', 'perimeter', 'eccentricity'), separator=',')
stat = pd.DataFrame(stat)
stat.to_csv('stat.csv', sep=',')

plt.tight_layout()
plt.show()
