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
imname = 'cathedral.jpg'

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

def align(ch1, ch2, scale_factor, best_dict, orig):
	if (scale_factor == 0) :
		d_list = list(best_dict.values())
		ssd_list = list(best_dict.keys())
		disp_vec = d_list[ssd_list.index(min(ssd_list))]
		
		ch1 = np.roll(orig, disp_vec[0], axis=0) 
		ch1 = np.roll(orig, disp_vec[1], axis=1)
		print(disp_vec)
		print(best_dict)
 		return ch1 

 	else:
		best_disp_vec = (0, 0)
		best_ssd = float("inf")
		shifted = ch1

		y = -15
		curr_x_place = ch1

		for x in range(-15, 16):
			curr_x_place = np.roll(ch1, x, axis=0)
			while y < 16:
				shifted = np.roll(curr_x_place, y, axis=1) #search over the window of displacememts using roll for each x,y
				curr_ssd = ssd(shifted, ch2)
				if curr_ssd < best_ssd:
					best_ssd = curr_ssd
					best_disp_vec = (x, y)
				y += 1
			y = -15

		best_dict.update({best_ssd: best_disp_vec})
		return align(rescale(ch1, 2), rescale(ch2, 2), scale_factor-1, best_dict, orig)
	
#To search over a window of possible displacements 
#score each one using some image matching metric
#and take the displacement with the best score.

g2 = rescale(g, .03125)
r2 = rescale(r, .03125)
b2 = rescale(b, .03125)

print(np.floor(g2.shape[0]).astype(np.int))

best_overall = {}
ag = align(g2, b2, 5, best_overall, g)

g2 = rescale(g, .03125)
r2 = rescale(r, .03125)
b2 = rescale(b, .03125)

best_overall = {}
ar = align(r2, b2, 5, best_overall, r)

#create a color image
# b = rescale(b, .03125)
# b = rescale(b, 2)
# b = rescale(b, 2)
# b = rescale(b, 2)
# b = rescale(b, 2)
# b = rescale(b, 2)
# agheight = np.floor(ag.shape[0]).astype(np.int)
# arheight = np.floor(ar.shape[0]).astype(np.int)
# bheight = np.floor(b.shape[0]).astype(np.int)
# print(agheight, arheight, bheight)

im_out = np.dstack([ar, ag, b])

# save the image
fname = './out_path/out_frame3.jpg'
skio.imsave(fname, im_out)

# display the image
skio.imshow(im_out)
skio.show()