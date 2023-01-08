import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Key metrics are:
# Unemployment rate, profitability of the companies, and cash levels of society and market. Possibly price levels too...
# These should all be indexed to a starting value of 1.0 and compared on a line chart
class Plot:
    def __init__(self):
        self.dt_now = datetime.now()
        self.dt_string = self.dt_now.strftime("%m%d_%M_%S")

    def plot(self):
        # profit
        summary_F_df = pd.read_csv("data/Farm1_full_log.csv")
        summary_F_df['Farm Profit'] = summary_F_df['Profit']/summary_F_df['Profit'][0]
        summary_F_df = summary_F_df['Farm Profit']
        summary_B_df = pd.read_csv("data/Builder1_full_log.csv")
        summary_B_df['Builder Profit'] = summary_B_df['Profit']/summary_B_df['Profit'][0]
        summary_B_df = summary_B_df['Builder Profit']
        summary_R_df = pd.read_csv("data/ResourceCo1_full_log.csv")
        summary_R_df['Resources Profit'] = summary_R_df['Profit']/summary_R_df['Profit'][0]
        summary_R_df = summary_R_df['Resources Profit']

        marketprices_df = pd.read_csv("data/MarketCo1_full_log.csv")
        marketprices_df['Food - rel price'] = marketprices_df['Price - food']/marketprices_df['Price - food'][0]
        marketprice_F_df = marketprices_df['Food - rel price']
        marketprices_df['Housing - rel price'] = marketprices_df['Price - housing']/marketprices_df['Price - housing'][0]
        marketprice_B_df = marketprices_df['Housing - rel price']
        marketprices_df['Resources - rel price'] = marketprices_df['Price - resources']/marketprices_df['Price - resources'][0]
        marketprice_R_df = marketprices_df['Resources - rel price']

        # unemp_df = pd.read_csv("data/society_unemployment_full_log.csv")

        fig, ax1 = plt.subplots(2)
        fig.suptitle('Key Economic Metrics')
        color = 'tab:red'
        color2 = 'tab:orange'
        color3 = 'tab:green'
        ax1[0].set_xlabel('Period')
        ax1[0].set_ylabel('Profit - standardised', color=color)
        ax1[0].plot(summary_F_df.index+1, summary_F_df, color=color, label='Farm Profit')
        ax1[0].plot(summary_F_df.index+1, summary_B_df, color=color2, label='Builder Profit')
        ax1[0].plot(summary_F_df.index+1, summary_R_df, color=color3, label='ResourceCo Profit')
        ax1[1].set_xlabel('Period')
        ax1[1].set_ylabel('Market Price - standardised', color=color)
        ax1[1].plot(summary_F_df.index + 1, marketprice_F_df, color=color, label='Farm unit price')
        ax1[1].plot(summary_F_df.index + 1, marketprice_B_df, color=color2, label='Builder unit price')
        ax1[1].plot(summary_F_df.index + 1, marketprice_R_df, color=color3, label='ResourceCo unit price')
        ax1[0].tick_params(axis='y', labelcolor=color)
        ax1[0].set_xlabel('Time Period')  # Add an x-label to the axes.
        ax1[0].grid(True, linestyle = "-.")
        ax1[1].tick_params(axis='y', labelcolor=color)
        ax1[1].set_xlabel('Time Period')  # Add an x-label to the axes.
        ax1[1].grid(True, linestyle="-.")
        # ax2[0] = ax1[0].twinx()  # instantiate a second axes that shares the same x-axis
        #
        # color = 'tab:blue'
        # ax2[0].set_ylabel('Unemployment rate', color=color)  # we already handled the x-label with ax1
        # ax2[0].plot(summary_F_df.index+1, unemp_df, color=color, label='Unemployment rate')
        # ax2[0].tick_params(axis='y', labelcolor=color)
        ax1[0].legend()  # Add a legend.
        ax1[1].legend()  # Add a legend.
        # ax2.legend()  # Add a legend.
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        fig.savefig(f"data/metrics/key_metrics_{self.dt_string}.png")
        plt.show()

# plot=Plot()
# plot.plot()