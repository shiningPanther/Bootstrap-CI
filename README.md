#### Overview
A script written in Python to calculate the 95% confidence interval of a quantile of a sample (here the 95% quantile) using the empirical bootstrap method.
The pdf can be customly designed, in this script it is a Gamma distribution.

#### Sampling from the pdf
Here, we employ class leverage and use the built-in methods of scipy.stats to sample from the pdf.
Another possibility would be to use rejection sampling, which I am planning to implement in the future.

#### Example
![Example](/CI1.png)
PDF in red, sampled distribution in blue, and the 95% confidence interval of the 95% quantile in green.
