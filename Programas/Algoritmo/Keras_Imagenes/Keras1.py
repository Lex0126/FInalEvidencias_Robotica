from keras.src.utils import load_img
largo, alto = 320, 320 #tamaño segun los pixeles de tu imagen [cuadrada]

file = 'vertin.png'  #nombre de la imagen usada

img = load_img(file, target_size=(largo, alto),
               color_mode = "grayscale"
)

print(img.size)
print(img.mode)

import matplotlib.pyplot as plt
plt.imshow (img, cmap = "gray")
plt.imshow(img)
plt.xticks([])
plt.yticks([])
plt.show()