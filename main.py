import matplotlib.pyplot as plt
import matplotlib.patches as patches
# import 


class bounding_circle() :
	def __init__(self, img) :
		self.img = img.copy()

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

		possible_dir = [(-1,0) , (1,0) , (0,1) , (0,-1)]            # possible direction are the

		while(len(stack) > 0) :
			u = stack.pop()
			self.img[u[0]][u[1]] = 0										# darkening it ( 1 --> 0 )

			box_coor[0][0] = min(box_coor[0][0] , u[0])
			box_coor[0][1] = min(box_coor[0][1] , u[1])
			box_coor[1][0] = max(box_coor[1][0] , u[0])
			box_coor[1][1] = max(box_coor[1][1] , u[1])

			for directions in possible_dir :                        # iterating in the possible directions
				if(self.img.shape[0] > u[0] + directions[0] >= 0 and self.img.shape[1] > u[1] + directions[1] >= 0 and self.img[u[0] + directions[0]][u[1] + directions[1]] == 1) :
					# if the index is valid and the pixel at that index is white
					# the we need to darken it
					stack.append((u[0] + directions[0],u[1] + directions[1]))

		return box_coor

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
					box_coor = self.__hide_object(i , j)						# need to hide all other white pixels of this object
					obj_box_coor.append(box_coor)
		
		return objects_counter , obj_box_coor


if __name__ == '__main__' :
	img = plt.imread('Project1.png')

	# bc = bounding_circle(img)
	# a = bc.number_of_objects()
	# n , l = bc.get_box()
	# print(n)
	# print(l)

	l = [[[14, 740], [121, 834]], [[18, 62], [192, 244]], [[30, 378], [188, 555]], [[239, 58], [409, 209]], [[266, 388], [420, 567]], [[282, 653], [388, 933]], [[440, 401], [629, 535]], [[453, 40], [606, 264]], [[495, 674], [612, 914]]]
	

	fig , ax = plt.subplots()
	plt.imshow(img , cmap = 'gray')
	for box_coor in l :
		rect = patches.Rectangle((box_coor[0][1],box_coor[0][0]),box_coor[1][1]-box_coor[0][1],box_coor[1][0]-box_coor[0][0],linewidth=3,edgecolor='r',facecolor='none')
		x = box_coor[0][0] + box_coor[1][0] ; x /= 2 ;
		y = box_coor[0][1] + box_coor[1][1] ; y /= 2 ;
		r = ((box_coor[0][0] - x) ** 2 + (box_coor[0][1] - y) ** 2 ) ** 0.5
		circle = patches.Circle((y,x), r, linewidth = 3, edgecolor = 'b' , facecolor = 'none')
		ax.add_patch(rect)																			# Adding the rectangular patch to the Axes
		ax.add_patch(circle)

	plt.show()
