import numpy as np
import math
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Settings
year = 2021
weeks = [1, 2, 3, 4, 5, 6]
days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
               'September', 'October', 'November', 'December']

#def generate_data(year, month, day, interval=365):
def generate_data(date, interval=365):
    idx = pd.date_range(date, periods=interval, freq='D')
    return pd.Series(range(len(idx)), index=idx)


def split_months(df, year):
    csv = pd.read_csv('D:\Arquivos de Programa\mpv\data_'+str(year)+'.csv', index_col=False)
    """
    Take a df, slice by year, and produce a list of months,
    where each month is a 2D array in the shape of the calendar
    :param df: dataframe or series
    :return: matrix for daily values and numerals
    """
    df = df[df.index.year == year]

    # Empty matrices
    a = np.empty((6, 7))
    a[:] = np.nan

    day_nums = {m:np.copy(a) for m in range(1,13)}  # matrix for day numbers
    day_vals = {m:np.copy(a) for m in range(1,13)}  # matrix for day values
    min_val = math.inf
    max_val = -math.inf
    # Logic to shape datetimes to matrices in calendar layout
    for d in df.iteritems():  # use iterrows if you have a DataFrame
        day = d[0].day
        month = d[0].month
        col = d[0].dayofweek
        if d[0].is_month_start:
            row = 0

        #----------------------------------------------------------
        #DATA GATHERING
        sum = 0
        filter = csv[csv['i_day'] == day]
        filter = filter[filter['i_month'] == month]
        for duration in filter['duration']:
            sum += duration

        sum = (sum/60.0)
        min_val = min(sum, min_val)
        max_val = max(sum, max_val)
        #----------------------------------------------------------
        day_nums[month][row, col] = day  # day number (0-31)
        day_vals[month][row, col] = sum # day value (the heatmap data)

        if col == 6:
            row += 1

    return day_nums, day_vals, min_val, max_val


def create_year_calendar(title, day_nums, day_vals, min_val, max_val, id):
    fig, ax = plt.subplots(3, 4, figsize=(16.85, 10.5))
    #.reversed()
    color_map =  plt.cm.get_cmap('summer').reversed()
    max_val = math.ceil(max_val/10)*10
    min_val = math.floor(min_val/10)*10

    im = None
    bg_color = '#3caea3'
    fr_color = '#10524c'
    for i, axs in enumerate(ax.flat):
        axs.set_facecolor(bg_color)
        im = axs.imshow(day_vals[i+1], cmap=color_map, vmin=min_val, vmax=max_val)  # heatmap
        axs.set_title(month_names[i])

        # Labels
        axs.set_xticks(np.arange(len(days)))
        axs.set_xticklabels(days, fontsize=10, fontweight='bold', color='#555555')
        axs.set_yticklabels([])

        # Tick marks
        axs.tick_params(axis=u'both', which=u'both', length=0)  # remove tick marks
        axs.xaxis.tick_top()

        # Modify tick locations for proper grid placement
        axs.set_xticks(np.arange(-.5, 6, 1), minor=True)
        axs.set_yticks(np.arange(-.5, 5, 1), minor=True)
        axs.grid(which='minor', color=fr_color, linestyle='-', linewidth=1.1)

        # Despine
        for edge in ['left', 'right', 'bottom', 'top']:
            axs.spines[edge].set_color(fr_color)
            axs.spines[edge].set_linewidth(2.1)

        # Annotate
        for w in range(len(weeks)):
            for d in range(len(days)):
                day_val = day_vals[i+1][w, d]
                day_num = day_nums[i+1][w, d]

                c = "#000000"
                if np.isnan(day_num):
                    c = bg_color

                val = '0'
                if day_val != 0:
                    val = format(day_val, '.1f')
                axs.text(d, w+0.2, val,
                         ha="center", va="center",
                         fontsize=9, color=c, alpha=1)

                # If day number is a valid calendar day, add an annotation
                if not np.isnan(day_num):
                    axs.text(d+0.45, w-0.31, f"{day_num:0.0f}",
                             ha="right", va="center",
                             fontsize=6, color="#000000", alpha=1)  # day

                    # Aesthetic background for calendar day number
                    patch_coords = ((d-0.1, w-0.5),
                                    (d+0.5, w-0.5),
                                    (d+0.5, w+0.1))
                    triangle = Polygon(patch_coords, fc='w', alpha=0.7)
                    axs.add_artist(triangle)

    # Final adjustments
    fig.suptitle(title, fontsize=25)
    cax = fig.add_axes([0.96, 0.1, 0.01, 0.7]) #subtitle
    fig.colorbar(im, cax=cax)
    fig.patch.set_facecolor(bg_color)
    plt.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.04)

    # Save to file
    plt.savefig('calendar_'+id+'.pdf')
    #plt.show()


df = generate_data(str(year)+'-01-01')
day_nums, day_vals, min_val, max_val = split_months(df, year)
create_year_calendar('Time spent (minutes)', day_nums, day_vals, min_val, max_val, str(year))