    #### Take a look at NYC metro ridership during different precipitation levels
    #### by visualising average hourly entries for individual turnstiles per precipitation level

    import pandas
    from ggplot import *
    import numpy as np
    
    
    # only need this when working in udacity IDE
    pandas.options.mode.chained_assignment = None

    # Read csv file with dataset
    turnstile_df = pandas.read_csv(turnstile_weather)
  
    # Add day of the week to the dataframe
    turnstile_df['date'] = pandas.to_datetime(turnstile_df['DATEn'])
    turnstile_df['weekday'] = turnstile_df['date'].apply(lambda x: x.weekday())

    # Group dataset by unit and precipitation level (sequence makes no difference)
    # Select only Mon-Fri to exclude systematically lower ridership on week-end
    entries_precipitation = turnstile_df.loc[turnstile_df['weekday']<5].groupby(['UNIT', 'precipi'], as_index=False).\
        agg({'ENTRIESn_hourly': [np.mean]})    
               
    # Build the dataframe to plot: unit, precipitation level, avg hourly entries
    entries_and_precipitation_df = pandas.DataFrame(\
        {'unit': entries_precipitation['UNIT'],\
        'precipi': entries_precipitation['precipi'],\
        'entries_hourly_avg': entries_precipitation['ENTRIESn_hourly']['mean']})        
        
    # Filter the dataset to use only turnstiles with a minimum level of average hourly entries,
    # i.e. at least x hourly entries on average
    units_threshold = entries_and_precipitation_df.groupby('unit', as_index=False).mean()
    units_threshold = units_threshold.loc[units_threshold['entries_hourly_avg'] > 1500] 

    # Keep only the labels of the units for subsequent filtering
    units_filtered = units_threshold['unit']
    
    # Filter the actual dataset
    entries_and_precipitation_df = entries_and_precipitation_df[entries_and_precipitation_df['unit'].isin(units_filtered)]
    
    # Check that the length corresponds to number of filtered turnstiles * number of precipitation levels
    #print len(entries_and_precipitation_df)    
        
    # Build a grand average per precipitation level to plot on the graph
    entries_precipitation_avg = entries_and_precipitation_df.groupby('precipi', as_index=False).mean()
    entries_precipitation_avg['unit'] = 'Average across units'  
    
    # Plot entries per precipitation level for individual units 
    # plus grand average 
    gg = ggplot(entries_and_precipitation_df, aes(x='precipi', y='entries_hourly_avg', color='unit'))\
        + geom_line() \
        + geom_line(aes(x='precipi', y='entries_hourly_avg'), data=entries_precipitation_avg, color='red', size=10) \
        + xlab('Precipitation level') \
        + ylab('Average hourly entries of ' + str(len(units_filtered)) + ' individual turnstile units') \
        + scale_y_continuous(labels='comma') \
        + ggtitle('Hourly metro entries during different precipitation levels (Mon-Fri)')

    print gg
