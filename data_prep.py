import cv2
import numpy as np
def load_img(image_dir, target_size):
	data = cv2.imread(image_dir) 
	data = cv2.bitwise_not(data)
	data = np.asarray(cv2.resize(data, target_size))
	data = data.reshape(1,-1)
	return data

def img_to_array(img):
	train_x_flatten = img.reshape(img.shape[0], -1).T   # The "-1" makes reshape flatten the remaining dimensions
	train_x = train_x_flatten/255.
	return train_x

def load_model(file_name):
	print(file_name)
	parameters = np.load(file_name, allow_pickle=True)
	parameters = parameters.reshape(1,-1)
	return parameters[0][0]

def linear_forward(A, W, b):
    Z = np.dot(W,A) + b
    cache = (A, W, b)    
    return Z, cache

def sigmoid(Z):
    A = 1/(1+np.exp(-Z))
    cache = Z
    
    return A, cache

def relu(Z):
    A = np.maximum(0,Z)
    
    assert(A.shape == Z.shape)
    
    cache = Z 
    return A, cache

def linear_activation_forward(A_prev, W, b, activation):
    
    if activation == "sigmoid":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = sigmoid(Z)    
    elif activation == "relu":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = relu(Z)
    cache = (linear_cache, activation_cache)

    return A, cache

def L_model_forward(X, parameters):
    caches = []
    A = X
    L = len(parameters) // 2                  # number of layers in the neural network
    for l in range(1, L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev, parameters["W" + str(l)], parameters["b" + str(l)], "relu")
        caches.append(cache)
    AL, cache = linear_activation_forward(A, parameters["W" + str(L)], parameters["b" + str(L)], "sigmoid")
    caches.append(cache)          
    return AL, caches

	
def predict_image(image, parameters):
    m = image.shape[1]
    p = np.zeros((1,m))
    
    # Forward propagation
    probas, caches = L_model_forward(image, parameters)

    # convert probas to 0/1 predictions
    for i in range(0, probas.shape[1]):
        if probas[0,i] > 0.5:
            p[0,i] = 1
        else:
            p[0,i] = 0

    return np.squeeze(p)