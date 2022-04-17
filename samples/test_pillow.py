from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# colormap values: hot, terrain, summer, autumn, gray

im = Image.open("assets/noise1/noise1_2.png")
# print(im.format, im.size, im.mode) # prints: PNG (32, 32) L # L for luminance

# Get the color map by name:
colormap = plt.get_cmap('terrain')

# opens image with shell "open"
im = im.resize((1<<8,1<<8), resample=Image.Resampling.LANCZOS)
# im = im.convert("P", palette=Image.ADAPTIVE, colors=256)
# im = im.remap_palette([c for oc, c in clrs])


cm_hot = mpl.cm.get_cmap('terrain')
im = np.array(im)
im = cm_hot(im)
im = np.uint8(im * 255)
im = Image.fromarray(im)

im.show()
