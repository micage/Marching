import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img0 = mpimg.imread('assets/noise1/noise1_0.png')
img1 = mpimg.imread('assets/noise1/noise1_1.png')
cfg0 = mpimg.imread('assets/config1/config1_0.png')
cfg1 = mpimg.imread('assets/config1/config1_1.png')

f, ax = plt.subplots(2,2)
f.set_size_inches(12, 12)
ax[0][0].imshow(img0, cmap='terrain')
ax[0][1].imshow(cfg0)
ax[1][0].imshow(img1, cmap='terrain')
ax[1][1].imshow(cfg1)
plt.show()