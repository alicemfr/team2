
from plotnine import *
import matplotlib.pyplot as plt
import seaborn as sns

# import pandas as pd
# df = pd.read_csv('~/OneDrive - University of Exeter/Documents/Projects/Hackathon_2023/probe1_test.csv')


def age_scatter(df, plot_sex, non_linear):
    
    # extract info
    df['Beta_percent'] = df['Value'] * 100  # corresponding DNAm values for probe. Multiplied by 100 for %
    
    # plot
    plt.figure()
    if plot_sex:
        sns.lmplot(data = df, x = 'Age', y='Beta_percent', hue = 'Sex', scatter = True, lowess = non_linear)
    else:
        sns.lmplot(data = df, x = 'Age', y='Beta_percent', scatter = True, lowess = non_linear, scatter_kws={'color': 'black'}, line_kws={'color': 'black'})
        
    plt.ylim(0, 100)
    plt.xlim(5, 25)
    plt.xlabel("Age (PCW)", fontsize = 15)
    plt.ylabel("DNA methylation (%)", fontsize = 15)

    plt.show()
    
    
    
        
