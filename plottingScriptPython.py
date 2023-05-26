
from plotnine import *

# import pandas as pd
# df = pd.read_csv('~/OneDrive - University of Exeter/Documents/Projects/Hackathon_2023/probe1_test.csv')
# plot_sex = False

def get_range(x) :
    
    return (max(x) - min(x))

def age_scatter(df, plot_sex, non_linear):
    
    # extract info
    df['Beta_percent'] = df['Value'] * 100  # corresponding DNAm values for probe. Multiplied by 100 for %
    
    if get_range(df["Value"]) > 0.6 :
        
        SPAN = 0.4
        
    elif (get_range(df["Value"]) < 0.6)  & (get_range(df["Value"]) > 0.4):
        
        SPAN = 0.85
        
    else :
        
        SPAN = 1.0
    
    
    p = (ggplot(df, aes(x="Age", y="Beta_percent"))
		+ geom_point(size=3)
        + xlab("Age (PCW)")
		+ ylab("DNA methylation (%)")
		+ ylim(0,100)
		+ theme(axis_text=element_text(size=19), axis_title=element_text(size=20))
        + theme_minimal()
		) 
    
    if plot_sex :
        p = p + aes(color = "Sex")
        
        if non_linear :
            p = p + geom_smooth(method='loess', se=False, size=1, span = SPAN)
            
        else: 
            p = p + stat_smooth(method = "lm", formula = "y ~ x", se = True)
            
    else:
        
        if non_linear :
            p = p + geom_smooth(method='loess', se=False, size=1, span = SPAN)
            
        else: 
            p = p + stat_smooth(method = "lm", formula = "y ~ x", se = True)
    
    p.save('plot_fig.png')
        
    # return p

