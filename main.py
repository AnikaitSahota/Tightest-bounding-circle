from PIL.Image import NONE
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import smallestenclosingcircle


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
		"""
		stack = [(i,j)]                                             # stack for DFS traversal
		box_coor = [[img.shape[0] * img.shape[1] + 2 , img.shape[0] * img.shape[1] + 2] , [-1 , -1]]
		border_pt = set()

		possible_dir = [(1,0) , (-1,0) , (0,1) , (0,-1)]            # possible direction are the

		while(len(stack) > 0) :
			u = stack.pop()
			self.img[u[0]][u[1]] = 0										# darkening it ( 1 --> 0 )

			box_coor[0][0] = min(box_coor[0][0] , u[0])
			box_coor[0][1] = min(box_coor[0][1] , u[1])
			box_coor[1][0] = max(box_coor[1][0] , u[0])
			box_coor[1][1] = max(box_coor[1][1] , u[1])

			border_flag = 0
			for directions in possible_dir :                        # iterating in the possible directions
				if(self.img.shape[0] > u[0] + directions[0] >= 0 and self.img.shape[1] > u[1] + directions[1] >= 0 and self.img[u[0] + directions[0]][u[1] + directions[1]] == 1) :
					# if the index is valid and the pixel at that index is white
					# the we need to darken it
					stack.append((u[0] + directions[0],u[1] + directions[1]))
					border_flag += self.org[u[0] + directions[0]][u[1] + directions[1]]		# number of white neigbhours

			if(border_flag == 1) :
				border_pt.add(u)

		return box_coor, border_pt

	def number_of_objects(self) -> int :
		"""function to find number of white objects in the black background image

		Returns
		-------
		int
			number of white objects in the image
		"""
		objects_counter = 0											# starting object counter

		for i in range(self.img.shape[0]) :
			for j in range(self.img.shape[1]) :
				if(self.img[i][j] == 1) :                				# white pixel of a object is found
					objects_counter += 1							# one more object is found
					self.__hide_object(i , j)						# need to hide all other white pixels of this object
		
		return objects_counter

	def get_box(self) :
		"""function to count number of objects and calculate bouding box coordinates

		Returns
		-------
		int
			objects_counter : number of objects
		list
			bounding box coordinats of detected objects
		"""
		objects_counter = 0											# starting object counter
		obj_box_coor = []

		for i in range(self.img.shape[0]) :
			for j in range(self.img.shape[1]) :
				if(self.img[i][j] == 1) :                				# white pixel of a object is found
					objects_counter += 1							# one more object is found
					box_coor , _ = self.__hide_object(i , j)						# need to hide all other white pixels of this object
					obj_box_coor.append(box_coor)
		
		return objects_counter , obj_box_coor

	# def get_tightest_circle(self , border_pt) :
	# 	for i in range()

	def get_circle(self) :
		objects_counter = 0											# starting object counter
		border_pt_wrt_obj = []

		for i in range(self.img.shape[0]) :
			for j in range(self.img.shape[1]) :
				if(self.img[i][j] == 1) :                				# white pixel of a object is found
					objects_counter += 1							# one more object is found
					_ , border_pt = self.__hide_object(i , j)						# need to hide all other white pixels of this object
					border_pt_wrt_obj.append(border_pt)

		# for border_pt in border_pt_wrt_obj :
		# 	for u in border_pt :
		# 		self.img[u[0]][u[1]] = 1
		# plt.imshow(self.img , cmap='gray')
		return objects_counter , border_pt_wrt_obj


def non_tightest(img) :
	bc = bounding_circle(img)
	n , l = bc.get_box()
	print('Number of objects detected = ' , n)
	# print(l)
	# l = [[[14, 740], [121, 834]], [[18, 62], [192, 244]], [[30, 378], [188, 555]], [[239, 58], [409, 209]], [[266, 388], [420, 567]], [[282, 653], [388, 933]], [[440, 401], [629, 535]], [[453, 40], [606, 264]], [[495, 674], [612, 914]]]	

	fig , ax = plt.subplots()
	plt.imshow(img , cmap = 'gray')
	for box_coor in l :
		rect = patches.Rectangle((box_coor[0][1],box_coor[0][0]),box_coor[1][1]-box_coor[0][1],box_coor[1][0]-box_coor[0][0],linewidth=2,edgecolor='b',facecolor='none')
		x = box_coor[0][0] + box_coor[1][0] ; x /= 2 ;
		y = box_coor[0][1] + box_coor[1][1] ; y /= 2 ;
		r = ((box_coor[0][0] - x) ** 2 + (box_coor[0][1] - y) ** 2 ) ** 0.5
		circle = patches.Circle((y,x), r, linewidth = 1, edgecolor = 'r' , facecolor = 'none')
		ax.add_patch(rect)																			# Adding the rectangular patch to the Axes
		ax.add_patch(circle)

	plt.show()

def tightest(img) :
	bc = bounding_circle(img)
	n , b_pt_obj = bc.get_circle()
	print('Number of objects detected = ' , n)
	circle_arg = []
	fig , ax = plt.subplots()
	plt.imshow(img , cmap = 'gray')
	for b_pt in b_pt_obj :
		actual = smallestenclosingcircle.make_circle(b_pt)
		circle_arg.append(actual)
		# circle = patches.Circle((actual[1],actual[0]), actual[2], linewidth = 1, edgecolor = 'r' , facecolor = 'none')
		# ax.add_patch(circle)
		ax.add_artist(plt.Circle((actual[1], actual[0]), actual[2] , edgecolor = 'r' , fill = False))

	plt.show()
	return circle_arg

def jacard_similarity(img1 , img2 = None) :
	if(img2 == None) :
		circle_arg_obj = tightest(img1)
	else :
		circle_arg_obj = tightest(img2)

	common_count = 0

	for i in range (img1.shape[0]) :
		for j in range (img1.shape[1]) :
			in_circle = False
			for circle_arg in circle_arg_obj :
				if(((circle_arg[0] - i)**2 + (circle_arg[1] - j)**2) ** 0.5 <= circle_arg[2]) :
					in_circle = True
					break
			if((in_circle and img1[i][j] == 1) or (in_circle == False and img1[i][j] == 0)) :
				common_count += 1
	
	return common_count / (img1.shape[0] * img1.shape[1])

if __name__ == '__main__' :
	img = plt.imread('Project1.png')
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

	for obj in objects :
		score = jacard_similarity(obj)
		print(score)


	# coor = tightest(obj6)
	# print(coor)
	# non_tightest(img)