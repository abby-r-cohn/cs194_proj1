# CS194-26 (CS294-26): Project 1 starter Python code

# these are just some suggested libraries
# instead of scikit-image you could use matplotlib and opencv to read, write, and display images

import numpy as np
import skimage as sk
import skimage.io as skio
from skimage.transform import rescale
from skimage.util import crop
import math

# name of the input file
imname = 'self_portrait.tif'

# read in the image
im = skio.imread(imname)

# convert to double (might want to do this later on to save memory)    
im = sk.img_as_float(im)
    
# compute the height of each part (just 1/3 of total)
height = np.floor(im.shape[0] / 3.0).astype(np.int)

# separate color channels
b = im[:height]
g = im[height: 2*height]
r = im[2*height: 3*height]

# align the images
# functions that might be useful for aligning the images include:
# np.roll, np.sum, sk.transform.rescale (for multiscale)

#add recursive calls that will downscale image (use sk.rescale) for image pyramid			

def ssd(ch1, ch2):
	sd = np.sum(np.sum((ch1 - ch2) ** 2))
	#return SSD. the lower the error, the more similar
	return sd

def align(ch1, ch2, scale_factor, prev_best):

	ch1_scale = rescale(ch1, .5 ** scale_factor)
	ch2_scale = rescale(ch2, .5 ** scale_factor)

	if (scale_factor == 0):

		best_disp_vec = (0, 0)
		best_ssd = float("inf")
		shifted = ch1_scale

		y = -15 + prev_best[1]*2
		curr_x_place = ch1

		for x in range(-15 + prev_best[0]*2, 16 + prev_best[0]*2):
			curr_x_place = np.roll(ch1_scale, x, axis=0)
			while y < 16 + prev_best[1]*2:
				shifted = np.roll(curr_x_place, y, axis=1) #search over the window of displacememts using roll for each x,y
				curr_ssd = ssd(shifted, ch2_scale)
				if curr_ssd < best_ssd:
					best_ssd = curr_ssd
					best_disp_vec = (x, y)
				y += 1
			y = -15 + prev_best[1]*2
		
		ch1 = np.roll(ch1, best_disp_vec[0], axis=0) 
		ch1 = np.roll(ch1, best_disp_vec[1], axis=1)
		print(best_disp_vec)
		
 		return ch1
 		
 	else:
		best_disp_vec = (0, 0)
		best_ssd = float("inf")
		shifted = ch1_scale

		y = -15 + prev_best[1]*2
		curr_x_place = ch1

		for x in range(-15 + prev_best[0]*2, 16 + prev_best[0]*2):
			curr_x_place = np.roll(ch1_scale, x, axis=0)
			while y < 16 + prev_best[1]*2:
				shifted = np.roll(curr_x_place, y, axis=1) #search over the window of displacememts using roll for each x,y
				curr_ssd = ssd(shifted, ch2_scale)
				if curr_ssd < best_ssd:
					best_ssd = curr_ssd
					best_disp_vec = (x, y)
				y += 1
			y = -15 + prev_best[1]*2

		prev_best = best_disp_vec

		return align(ch1, ch2, scale_factor-1, prev_best)
	
#To search over a window of possible displacements 
#score each one using some image matching metric
#and take the displacement with the best score.

best_ssd = float("inf")
ag = align(g, b, 1, (0,0))

best_ssd = float("inf")
ar = align(r, b, 1, (0,0))

im_out = np.dstack([ar, ag, b])

# save the image
fname = './out_path/self_portrait.jpg'
skio.imsave(fname, im_out)

# display the image
skio.imshow(im_out)
skio.show()

