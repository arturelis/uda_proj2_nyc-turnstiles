    #### Calculate the average number of entries per day of the week 
    #### and plot as bar chart using matplotlib and ggplot


    import pandas
    from ggplot import *
    import numpy as np
    import matplotlib.pyplot as plt
    
    
    # only need this when working in udacity IDE
    pandas.options.mode.chained_assignment = None

    # Read csv file with dataset
    turnstile_df = pandas.read_csv(turnstile_weather)
  
    # Add day of the week to the dataframe
    turnstile_df['date'] = pandas.to_datetime(turnstile_df['DATEn'])
    turnstile_df['weekday'] = turnstile_df['date'].apply(lambda x: x.weekday())
    
    # Set an array of weekday labels    
    weekday_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Get total entries per date
    daily_entries_intermediate = turnstile_df.groupby('date', as_index=False).agg({'ENTRIESn_hourly':[np.sum]})

    # Build a dataframe of daily entries to use farther on
    daily_entries = pandas.DataFrame()
    daily_entries['date'] = daily_entries_intermediate.date
    daily_entries['entries'] = daily_entries_intermediate['ENTRIESn_hourly']
    daily_entries['weekday'] = daily_entries_intermediate['date'].apply(lambda x: x.weekday())

    # Build a dataframe of average entries per day of the week
    weekday_entries = daily_entries.groupby('weekday', as_index=False).agg(np.mean)
    weekday_entries.columns = ['weekday', 'entries_avg']
    #print weekday_entries
    
    # Plot bar chart using matplotlib    
    plt.figure(figsize=(10,8))
    weekday_entries['entries_avg'].plot(kind='bar', color='r')
    plt.title('Entries to the NYC metro per day of week, May 2011')
    plt.xticks(range(0, 7), weekday_labels)
    plt.xlabel('Day of the week')    
    plt.ylabel('Average entries')
    plt.yticks()
    plt.show()
    
    # Plot bar chart using ggplot        
    gg = ggplot(weekday_entries, aes(x='weekday', y='entries_avg')) \
        + geom_bar(stat='bar') \
        + scale_x_continuous(breaks=range(0,7), labels=weekday_labels) \
        + scale_y_continuous(labels='comma') \
        + ggtitle('Entries to the NYC metro per day of week, May 2011') \
        + xlab('Day of the week') \
        + ylab('Average entries')
    
    print gg
