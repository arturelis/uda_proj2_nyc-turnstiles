    import pandas
    import numpy as np
    import matplotlib.pyplot as plt
    
    
    # only need this when working in udacity IDE
    pandas.options.mode.chained_assignment = None

    # Read csv file with dataset
    turnstile_df = pandas.read_csv(turnstile_weather)
    
    # Plot figure using matplotlib
    plt.figure(figsize=(10,5))
    bins=range(0,8000,100)    
    turnstile_weather_df['ENTRIESn_hourly'][turnstile_weather_df.rain==0].hist(bins=bins, label='No rain', color='yellow')
    turnstile_weather_df['ENTRIESn_hourly'][turnstile_weather_df.rain==1].hist(bins=bins, label='Rain', color='blue')
    plt.title('Histogramme of hourly entries to the NYC metro')
    plt.ylabel('Frequency')
    plt.xlabel('Hourly entries (values for ENTRIESn_hourly)')
    plt.legend()
    plt.show()
