
import pandas
import scipy
#import scipy.stats
import numpy as np
#import ggplot
import matplotlib.pyplot as plt
#plt.style.use('ggplot')
import statsmodels.api as sm
#from sklearn.linear_model import SGDRegressor


file_input=r'turnstile_data_master_with_weather.csv'

file_input_parsed = pandas.read_csv(file_input)

values, predictions_OLS, r2 = predictions_OLS(file_input_parsed)

#print predictions_OLS

residuals = values - predictions_OLS

plot_residuals_hist(residuals)

shapiro_wilk(residuals)

anderson(residuals)

probability_plot(residuals)

plot_residuals_against_predicted_values(predictions_OLS, residuals)

plot_observed_against_predicted_values(values, predictions_OLS)




def predictions_OLS(dataframe):

    # Check for week-ends
    dataframe['date'] = pandas.to_datetime(dataframe['DATEn'])
    dataframe['week-end'] = dataframe['date'].apply(lambda x: 1 if x.weekday() >= 5 else 0)
    
    features = dataframe[['week-end', 'rain', 'Hour']]
        
    # Deactivate during testing - requires a lot of memory resources
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit', sparse=True)
    features = features.join(dummy_units)
    
    # Values
    values_df = dataframe['ENTRIESn_hourly']

    # Perform linear regression
    intercept, params, r2 = linear_regression_OLS(features, values_df)
    
    # Calculate predicted values based on LR returns
    predictions = intercept + np.dot(features, params)
    
    #print 'OLS: ', r2    
    
    return values_df, predictions, r2




def linear_regression_OLS(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    """
       
    features = sm.add_constant(features)
    lr_model = sm.OLS(values, features)
    results = lr_model.fit()   
      
    intercept = results.params[0]
    params = results.params[1:]
    r2 = results.rsquared
    
    print results.summary()
    #print results.params
    
    return intercept, params, r2




def plot_residuals_hist(residuals):

    bins = range(-19999,40001,250)
    xticks = range(-20000,40001,5000)
    
    plt.figure(figsize=(10,5))
    #residuals.hist(bins=bins, weights=np.zeros_like(residuals) + 1. / residuals.size)
    plt.hist(residuals, bins=bins, weights=np.zeros_like(residuals) + 1. / residuals.size)
    plt.xlabel('Size range of residual (observed - estimated value)')
    plt.xticks(xticks, rotation=45)
    plt.ylabel('Relative frequency')
    plt.title('Difference between observed and predicted hourly subway entries')
    plt.show()
    
    return plt




def shapiro_wilk(values):
    
    W, p = scipy.stats.shapiro(values)
    
    print 'Shapiro-Wilk: '
    print 'W: ', W
    print 'p: ', p
    print ' '
    
    return W, p




def anderson(values):
    
    A2, crit_values, sign_level = scipy.stats.anderson(values, dist='norm')
  
    print 'Anderson-Darling: '
    print 'A2: ', A2
    print 'Critical values: ', crit_values
    print 'Significance level: ', sign_level
    print ' '
    
    return A2, crit_values, sign_level




def probability_plot(values):
    
    # SciPy probability plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    scipy.stats.probplot(values, plot=ax, fit=False) 
    plt.show()
    
    # Statsmodels probability plot
    probplot = sm.ProbPlot(values)
    probplot.probplot()
    plt.show()
    
    # Statsmodels Q-Q plot
    probplot = sm.ProbPlot(values)
    probplot.qqplot()
    plt.show()

    # Statsmodels P-P plot
    probplot = sm.ProbPlot(values)
    probplot.ppplot()
    plt.show()
   
    
    return True




def plot_residuals_against_predicted_values(predictions, residuals):
    
    # This allows us to detect if there is constant variance
    # or whether residuals are non-constant for certain predictions
    
    fig = plt.figure(figsize=(10,8))
    plt.scatter(predictions, residuals)
    plt.xlabel('Fitted values')
    plt.ylabel('Absolute residuals')
    plt.title('Plotting residuals against estimated values')
    plt.show()    
    
    return True 




def plot_observed_against_predicted_values(values, predictions):
    
    # This allows us to detect if there is constant variance
    # or whether residuals are non-constant for certain predictions
    
    fig = plt.figure(figsize=(10,8))
    plt.scatter(values, predictions)
    plt.xlabel('Observed values')
    plt.ylabel('Fitted values')
    plt.title('Plotting estimated against observed values')
    plt.show()    
    
    return True 

