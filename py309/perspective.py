import matplotlib.pyplot as plt
import numpy as np


def rectify_image(img, corners, height=200, width=300):
    '''
    Rectifies an image removing camera perspective
    
    img:      3-dimensional numpy array representing an image
    
    corners:  List of pixel coordinates of vertices of the area of
              the image are which is to be rectified. Coordinates of pixels  
              are gives as a tuple of the form (pixel_column, pixel_row).
              Order of vertices on the list is [upper_left, upper_right, lower_left, lower_right]
    
    width:    The number of columns of the rectified image
    
    height:   The number of rows of the rectified image
    
    Returns a 3-dimensional numpy array representing the rectified image
    '''
    
    if img.dtype == 'uint8':
        img = img.astype(float)/255
    
    c_arr = np.array(corners, dtype=float)
    
    #calculate the coordinate change matrix from the object coordinates to the camera coordinates
    C = np.hstack((c_arr, np.array([1,1,1,1]).reshape(-1, 1))).T
    scale = np.linalg.solve(C[:, :3]*np.array([-1, 1, 1]), C[:, -1])
    #A is the matrix of  coordinates of corners of the object in the camera coordinate system
    A = C[:, :3]*scale   
    #B is the matrix of  coordinates of corners of the object in the object coordinate system
    B = np.array([[0, 0, 1], [height-1, 0, 1], [0, width-1, 1]]).T
    #BC is the coordinate change matrix
    BC = np.dot(A, np.linalg.inv(B))
    
    #for each pixel of the rectified image compute coordinates of 
    #the corresponding pixel in the original image
    indices = np.empty((width, height, 3))
    indices[:,:,0], indices[:,:,1] = np.meshgrid(np.arange(height), np.arange(width))
    indices[:,:,2] = 1
    straight_coords = indices.reshape(-1, 3).T
    img_coords = np.dot(BC, straight_coords)
    homog_coords = (img_coords/img_coords[2]).astype(int)
    
    #assign color values to pixels in the rectified image using the above pixel coordinate correspondence
    img_indices = np.ravel_multi_index([homog_coords[1], homog_coords[0]], img.shape[:2])
    pic = img.reshape(-1, 3).T[:, img_indices].T.reshape(width, height, 3)
    
    return pic



def rectify_whole_image(img, corners, height, width):
    '''
    Rectifies an the whole image, removing perspective defined by coordinates of  four pixels.
    
    img:      3-dimensional numpy array representing an image
    
    corners:  List of pixel coordinates of vertices of the area of
              the image are which is to be rectified. Coordinates of pixels  
              are gives as a tuple of the form (pixel_column, pixel_row).
              Order of vertices on the list is [upper_left, upper_right, lower_left, lower_right]
    
    height:     The number of columns of the rectified image
    
    width:     The number of rows of the rectified image
    
    Returns a 3-dimensional numpy array representing the rectified image
    '''
    
    if img.dtype == 'uint8':
        img = img.copy().astype(float)/255
    
    c_arr = np.array(corners, dtype=float)
    C = np.hstack((c_arr, np.array([1,1,1,1]).reshape(-1, 1))).T

    scale = np.linalg.solve(C[:, :3]*np.array([-1, 1, 1]), C[:, -1])
    A = C[:, :3]*scale
    B = np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]).T
    BC = np.dot(A, np.linalg.inv(B))
    CB = np.linalg.inv(BC)
    ir, ic = img.shape[0], img.shape[1]
    corner_pix = np.dot(CB, np.array([[0, 0, 1], [ic, 0, 1], [0, ir, 1], [ic, ir, 1]]).T)
    max_row = np.max(corner_pix[1]/corner_pix[2])
    min_row = np.min(corner_pix[1]/corner_pix[2])
    max_col = np.max(corner_pix[0]/corner_pix[2])
    min_col = np.min(corner_pix[0]/corner_pix[2])
    pic = np.zeros((width, height, 3))
    for i in range(width):
        for j in range(height):
            x = (max_row-min_row)*(i/width) + min_row
            y = (max_col-min_col)*(j/height) + min_col
            pix = np.dot(BC, np.array([y, x,1]))
            if 0 <= int(pix[1]/pix[2]) < ir and 0 <= int(pix[0]/pix[2]) < ic:
                pic[i, j] = img[int(pix[1]/pix[2]), int(pix[0]/pix[2])]
    return pic


def paste_image(background, img, corners):
    '''
    Pastes an image into a quadrilateral area of the backgound image defined by four vertices.
    
    background:  3-dimensional numpy array representing the background image
    
    img:         3-dimensional numpy array representing the image to be pasted
    
    corners:     List of pixel coordinates of vertices of the area of
                 the image are which is to be rectified. Coordinates of pixels  
                 are gives as a tuple of the form (pixel_column, pixel_row).
                 Order of vertices on the list is [upper_left, upper_right, lower_left, lower_right]
    
    Returns a 3-dimensional numpy array representing modified background image
    '''
    
    if img.dtype == 'uint8':
        img = img.astype(float)/255
    
    if background.dtype == 'uint8':
        background = background.astype(float)/255
    
    
    brows, bcols = background.shape[:2]
    irows, icols = img.shape[:2]
    c_arr = np.array(corners, dtype=float)
    
    #calculate the coordinate change matrix from the he camera coordinates to the object coordinates
    C = np.hstack((c_arr, np.array([1,1,1,1]).reshape(-1, 1))).T
    scale = np.linalg.solve(C[:, :3]*np.array([-1, 1, 1]), C[:, -1])
    A = C[:, :3]*scale
    B = np.array([[0, 0, 1], [icols-1, 0, 1], [0, irows-1, 1]]).T
    CB = np.dot(B, np.linalg.inv(A))
    
    
    #for each pixel of the background image compute coordinates of 
    #the corresponding pixel in the pasted image 
    indices = np.empty((brows, bcols, 3))
    indices[:,:,0], indices[:,:,1] = np.meshgrid(np.arange(bcols), np.arange(brows))
    indices[:,:,2] = 1
    background_coords = indices.reshape(-1, 3).T
    img_coords = np.dot(CB, background_coords)
    homog_coords = (img_coords/img_coords[2]).astype(int)
    
    # some of these coordinates in the pasted image computed above may be 
    # negative or exceed pasted image dimensions; they correspond to background image 
    # pixels that lay outside the area defined by vertices
    # below we select coordinates that are valid
    valid_homog_bool  = (0 <= homog_coords[0]) & (0 <= homog_coords[1]) & (homog_coords[0] < icols) & (homog_coords[1] < irows)
    valid_homog_coords = homog_coords[:, valid_homog_bool]
    
    #copy pixels from the pasted image to the background image
    img_indices = np.ravel_multi_index([valid_homog_coords[1], valid_homog_coords[0]], img.shape[:2])
    background_array = background.copy().reshape(-1, 3).T
    background_array[:, valid_homog_bool] =  img.reshape(-1, 3).T[:, img_indices]
    
    return background_array.T.reshape(brows, bcols, 3)