import matplotlib.pyplot as plt
import matplotlib.patches as patches
import smallestenclosingcircle
import numpy as np


class bounding_circle() :
	def __init__(self, img) :
		self.img = img.copy()
		self.org = img[:,:]

	def __hide_object(self, i , j) :
		"""function to darken (black) the visited part of image, so that it is not counted again.

		Parameters
		----------
		i : int
			row index lying in the object (i.e. white)
		j : int
			column index lying in the object (i.e. white)

		Returns
		-------
		box_coor : list
			bounding box coordinates
		border_pt : list
			border pixel coordinates
		"""
		stack = [(i,j)]                                             								# stack for DFS traversal
		box_coor = [[img.shape[0] * img.shape[1] + 2 , img.shape[0] * img.shape[1] + 2] , [-1 , -1]]
		border_pt = set()

		possible_dir = [(1,0) , (-1,0) , (0,1) , (0,-1)]            								# possible direction are the

		while(len(stack) > 0) :
			u = stack.pop()
			self.img[u[0]][u[1]] = 0																# darkening it ( 1 --> 0 )

			box_coor[0][0] = min(box_coor[0][0] , u[0])
			box_coor[0][1] = min(box_coor[0][1] , u[1])
			box_coor[1][0] = max(box_coor[1][0] , u[0])
			box_coor[1][1] = max(box_coor[1][1] , u[1])

			border_flag = 0
			for directions in possible_dir :                        								# iterating in the possible directions
				if(self.img.shape[0] > u[0] + directions[0] >= 0 and self.img.shape[1] > u[1] + directions[1] >= 0 and self.img[u[0] + directions[0]][u[1] + directions[1]] == 1) :
					# if the index is valid and the pixel at that index is white
					# the we need to darken it
					stack.append((u[0] + directions[0],u[1] + directions[1]))
					border_flag += self.org[u[0] + directions[0]][u[1] + directions[1]]				# number of white neigbhours

			if(border_flag == 1) :																	# border point
				border_pt.add(u)

		return box_coor, border_pt

	def number_of_objects(self) -> int :
		"""function to find number of white objects in the black background image

		Returns
		-------
		objects_counter : int
			number of white objects in the image
		"""
		objects_counter = 0																			# starting object counter

		for i in range(self.img.shape[0]) :
			for j in range(self.img.shape[1]) :
				if(self.img[i][j] == 1) :															# white pixel of a object is found
					objects_counter += 1															# one more object is found
					self.__hide_object(i , j)														# need to hide all other white pixels of this object
		
		return objects_counter

	def get_box(self) :
		"""function to count number of objects and calculate bouding box coordinates

		Returns
		-------
		objects_counter : int
			objects_counter : number of objects
		obj_box_coor : list
			bounding box coordinats of detected objects
		"""
		objects_counter = 0																			# starting object counter
		obj_box_coor = []

		for i in range(self.img.shape[0]) :
			for j in range(self.img.shape[1]) :
				if(self.img[i][j] == 1) :															# white pixel of a object is found
					objects_counter += 1															# one more object is found
					box_coor , _ = self.__hide_object(i , j)										# need to hide all other white pixels of this object
					obj_box_coor.append(box_coor)													# adding the bounding box coordinates w.r.t object
		
		return objects_counter , obj_box_coor


	def get_circle(self , show_border_pts = False) :
		"""function to compute the tightest bounding circle for the image using the border points (i.e. key points)

		Returns
		-------
		objects_counter : int
			number of objects in the mentioned image
		border_pt_wrt_obj : list
			list of border points corresponding to the object
		"""
		objects_counter = 0																			# starting object counter
		border_pt_wrt_obj = []

		for i in range(self.img.shape[0]) :
			for j in range(self.img.shape[1]) :
				if(self.img[i][j] == 1) :															# white pixel of a object is found
					objects_counter += 1															# one more object is found
					_ , border_pt = self.__hide_object(i , j)										# need to hide all other white pixels of this object
					border_pt_wrt_obj.append(border_pt)												# adding the border pixels w.r.t object

		if(show_border_pts) :																		# to show the border pixels 
			for border_pt in border_pt_wrt_obj :														
				for u in border_pt :
					self.img[u[0]][u[1]] = 1														# higlighting key points in dark image
			plt.imshow(self.img , cmap='gray')														# showing image
		return objects_counter , border_pt_wrt_obj


def non_tightest_circle(img) :
	"""fucntion to find bounding box for the objects in the image and furthur use it to obtain the loosly bounding circle

	Parameters
	----------
	img : 2D numpy array
		image that will be processed
	"""
	bc = bounding_circle(img)																		# itialising the object
	n , l = bc.get_box()
	print('Number of objects detected = ' , n)
	# print(l)
	# l = [[[14, 740], [121, 834]], [[18, 62], [192, 244]], [[30, 378], [188, 555]], [[239, 58], [409, 209]], [[266, 388], [420, 567]], [[282, 653], [388, 933]], [[440, 401], [629, 535]], [[453, 40], [606, 264]], [[495, 674], [612, 914]]]	

	fig , ax = plt.subplots()																		# intialisng image window
	plt.imshow(img , cmap = 'gray')
	for box_coor in l :
		# computing the rectangular box over the objects
		rect = patches.Rectangle((box_coor[0][1],box_coor[0][0]),box_coor[1][1]-box_coor[0][1],box_coor[1][0]-box_coor[0][0],linewidth = 2,edgecolor='b',facecolor='none')
		x = box_coor[0][0] + box_coor[1][0] ; x /= 2 ;
		y = box_coor[0][1] + box_coor[1][1] ; y /= 2 ;
		r = ((box_coor[0][0] - x) ** 2 + (box_coor[0][1] - y) ** 2 ) ** 0.5
		# computing the circle over the objects
		circle = patches.Circle((y,x), r, linewidth = 2, edgecolor = 'r' , facecolor = 'none')
		ax.add_patch(rect)																			# Adding the rectangular patch to the Axes
		ax.add_patch(circle)																		# Adding the circle patch to the Axes

	plt.show()

def tightest_circle(img) :
	"""fucntion to find tigtest bounding circle

	Parameters
	----------
	img : 2D numpy array
		image that will be processed
	circle_arg : list
		contains argument of circle (i.e., x,y,r) for every detected object in image
	"""
	bc = bounding_circle(img)																		# itialising the object
	n , b_pt_obj = bc.get_circle()
	print('Number of objects detected = ' , n)
	circle_arg = []
	fig , ax = plt.subplots()																		# intialisng image window
	plt.imshow(img , cmap = 'gray')
	for b_pt in b_pt_obj :
		actual = smallestenclosingcircle.make_circle(b_pt)
		circle_arg.append(actual)
		circle = patches.Circle((actual[1],actual[0]), actual[2], linewidth = 2, edgecolor = 'r' , facecolor = 'none')
		ax.add_patch(circle)																		# Adding the circle patch to the Axes
		# ax.add_artist(plt.Circle((actual[1], actual[0]), actual[2] , edgecolor = 'r' , fill = False))

	plt.show()
	return circle_arg

def jaccard_similarity(img1 , img2) :
	"""function to compute the jaccard similarity among the two provided iamges

	Parameters
	----------
	img1 : 2D numpy array
		first image for comparision
	img2 : 2D numpy array
		second image for comparision

	Returns
	-------
	float
		jaccard score between two images
	"""
	# if black pixels outside circle are included
	# tmp = img1 + img2
	# common_count = (tmp != 1).sum()																	# number of common pixels
	# return common_count / (tmp.shape[0] * tmp.shape[1])												# jaccard score
	
	tmp = (img1 + img2) * img2																		# mutlitipication by mask, makes it sure that pixel inside mask are used, only
	common_count = (tmp > 1).sum()																	# number of common pixels
	return common_count / img2.sum()																# jaccard score


def create_mask(circle_args, img) :
	"""function to creat a mask over provided image based on the provided arguments of circle

	Parameters
	----------
	circle_args : list
		arguments of circle (i.e., x, y, r)
	img : 2D numpy
		image to be processed

	Returns
	-------
	img : 2D numpy array
		edited image i.e. masked image
	"""
	# iterating over image
	for i in range(img.shape[0]) :
		for j in range(img.shape[1]) :
			for circle_arg in circle_args :															# traversing over circles
				if(((circle_arg[0] - i) ** 2 + (circle_arg[1] - j) ** 2 ) ** 0.5 <= circle_arg[2]) :
					img[i][j] = 1																	# whitening the portion lying inside circle
					break

	return img


if __name__ == '__main__' :
	img = plt.imread('Project1.png')																# reading the image

	# creating patches based upon objects
	objects = []
	objects.append(img[:233 , :373])
	objects.append(img[:247 , 287:680])
	objects.append(img[:247 , 680:])
	objects.append(img[223:443 , :373])
	objects.append(img[233:433 , 287:630])
	objects.append(img[183:493 , 630:])
	objects.append(img[413: , :373])
	objects.append(img[423: , 287:650])
	objects.append(img[428: , 630:])

	objects = [img]																				# comment-out to compute over whole image

	for i in range(len(objects)) :																	# traversing over the objects
		circle_args = tightest_circle(objects[i])													# circle's arguments in patch according to objects
		mask = create_mask(circle_args , np.zeros(objects[i].shape, dtype = np.int))				# created a mask

		fig = plt.figure()
		plt.imshow(mask, cmap='gray')																# showing the mask
		plt.show()

		score = jaccard_similarity(objects[i] , mask)												# jacard score for the patch and image
		print('Jaccard score of object', i+1 , 'is' , score)