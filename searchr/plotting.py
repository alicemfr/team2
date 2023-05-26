from plotnine import *

# import pandas as pd
# df = pd.read_csv('~/OneDrive - University of Exeter/Documents/Projects/Hackathon_2023/probe1_test.csv')
# plot_sex = False


def age_scatter(df, plot_sex):
    # extract info
    df["Beta_percent"] = (
        df["Value"] * 100
    )  # corresponding DNAm values for probe. Multiplied by 100 for %

    if plot_sex:
        p = (
            ggplot(df, aes(x="Age", y="Beta_percent"))
            + aes(color="Sex")
            + geom_point(size=3)
            + xlab("Age (PCW)")
            + ylab("DNA methylation (%)")
            + ylim(0, 100)
            + stat_smooth(method="lm", formula="y ~ x", se=True)
            + theme_minimal()
            + theme(axis_text=element_text(size=19), axis_title=element_text(size=20))
        )

    else:
        p = (
            ggplot(df, aes(x="Age", y="Beta_percent"))
            + geom_point(size=3)
            + xlab("Age (PCW)")
            + ylab("DNA methylation (%)")
            + ylim(0, 100)
            + stat_smooth(method="lm", formula="y ~ x", se=True)
            + theme_minimal()
            + theme(axis_text=element_text(size=19), axis_title=element_text(size=20))
        )

    return p
