    #### Calculate how busy individual turnstile units are in the NYC metro (average daily entries & exits)
    #### Plot a histogramme using matplotlib and ggplot


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
    
    # Calculate total entries plus exits, add this to the Dataframe
    turnstile_df['entries_exits'] = turnstile_df['ENTRIESn_hourly'] + turnstile_df['EXITSn_hourly']

    # Determine how many days there are in the dataset
    days_in_dataset = len(turnstile_df['date'].unique())

    # Determine average daily entries+exits of each unit.
    avg_daily_entries_per_unit = turnstile_df.groupby('UNIT', as_index=False).\
        agg({'entries_exits':[np.sum, lambda x: np.sum(x) / days_in_dataset]})

    # Display list of top frequented turnstile units
    #avg_daily_entries_per_unit.sort([('entries_exits', 'sum')], ascending=False, inplace=True)   
    #print avg_daily_entries_per_unit.head()
    
    ## Display histogramme of the average daily entry/exit numbers per turnstile
    # Matplotlip
    plt.figure(figsize=(10,8))
    plt.hist(avg_daily_entries_per_unit['entries_exits']['<lambda>'], color='g', bins=range(0,210000, 10000))    
    plt.xticks(range(0, 200001, 10000), rotation=45, ha='right')
    plt.xlabel('Daily entries and exits per unit')    
    plt.ylabel('Number of units')
    #plt.yticks(range(0,251,50))
    plt.title('How busy are individual turnstile units in the NYC metro?')
    plt.show() 
    
    # ggplot
    gg = ggplot(avg_daily_entries_per_unit['entries_exits'], aes(x='<lambda>')) \
        + geom_histogram(stat='bin', binwidth=10000) \
        + scale_x_continuous(breaks=range(0,200001, 10000)) \
        + theme(axis_text_x = element_text(angle = 45)) \
        + ggtitle('How busy are individual turnstile units in the NYC metro?') \
        + xlab('Daily entries and exits per unit') \
        + ylab('Number of units')
        
    print gg
