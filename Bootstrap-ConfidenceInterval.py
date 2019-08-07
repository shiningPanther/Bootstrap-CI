'''
In this script, we calculate the 95% confidence interval of the 95% quantile for a given pdf using the empircal bootstrap method.
We sample N = 2000 points out of this function.
For the sampling we leverage class inheritance and rely on the build-in methods of the st.rv_continuous class.
Another approach for the sampling would be to use rejection sampling.
'''


import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt


class custom_pdf(st.rv_continuous):
	'''
	In this class we define the custom pdf and inherit all the methods from st.rv_continuous.
	Change the method _pdf to define a different pdf.
	'''
	def _pdf(self,x):
		return 1/24*x**4*np.exp(-x)


def createSample(N):
	'''
	Creates a sample with N points from the continuous variable defined by the custom pdf.
	Also prints the 95% quantile of the pdf and of the sample.
	'''

	# Create an instance of this class
	custom_cv = custom_pdf(a=0, name='custom_pdf')

	print('95% quantile calculated from pdf: {}'.format(custom_cv.ppf(0.95)))
	# Create a random sample of size N from the cv
	sample = custom_cv.rvs(size=N)
	sample_percentile = np.percentile(sample,95)
	print('95% quantile obtained from random sample: {}'.format(sample_percentile))
	return sample, sample_percentile

def plotCI(sample,CI):
	# Plot the pdf
	custom_cv = custom_pdf(a=0, name='custom_pdf')
	fig, ax = plt.subplots(1, 1)
	x = np.linspace(custom_cv.ppf(0.001),custom_cv.ppf(0.999),100)
	plt.plot(x, custom_cv.pdf(x),'r-', lw=3, alpha=0.6)

	# Plot the sample
	plt.hist(sample,bins=100,density=True)

	# Plot CI
	ax.hlines(y=-0.005, xmin=CI[0], xmax=CI[1], linewidth=3, color='g')
	plt.show()

	# Calculate mean, variance, skewness and curtosis.
	#mean, var, skew, kurt = custom_cv.stats(moments='mvsk')
	#print('Mean: {}; Var: {}'.format(mean, var))

def bootstrap(nboot, sample, sample_percentile):
	'''
	Implementatiom of the empirical bootstrap method
	'''
	delta_array = [] # Difference in the 95% percentile from the resampled data compared to the empirical sample
	for i in range(nboot):
		resample=np.random.choice(sample,size=len(sample),replace=True) # Resample the empirical sample
		resample_percentile = np.percentile(resample,95) # Create the 95% quantile of this new sample_percentile
		delta = resample_percentile - sample_percentile # Calculate the difference of the 95% quantile between the resampled and empirical data
		delta_array.append(delta)
	return delta_array


N = 2000 # Number of points of the sample
sample, sample_percentile = createSample(N)

nboot = 100000 # Number of simulations for the bootstrap
delta_array = bootstrap(nboot, sample, sample_percentile)
delta_percentile = np.percentile(delta_array, [97.5, 2.5]) # The bootstrap 95% confidence interval is given by the 97.5% and 2.5% quantile of the deltas
conf_interval = sample_percentile - delta_percentile
print('95% confidence interval obtained from bootstrap: {}'.format(conf_interval))
plotCI(sample,conf_interval)



