import numpy as np
from sound_classification import GenreFeatureData

# def parse_predictors(path):
	# with open(path) as f:
		# value = f.readline().split()[1]
	# return np.array([float(value)]).reshape(-1, 1)
	
def parse_predictors(path):
	gen = GenreFeatureData()
	res = gen.load_new_data([path])
	print(res.shape)
	return res