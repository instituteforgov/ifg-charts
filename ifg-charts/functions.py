from typing import Literal, Optional, Union

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
import seaborn as sns


def draw_beeswarm(
    data: pd.DataFrame,
    value_metric: str,
    group_by: str,
    orientation: Literal['horizontal'] = 'horizontal',
    ax_min: Optional[int] = 0,
    ax_max: Optional[int] = 100,
    order: Union[list | Literal['avg', 'min', 'max']] = 'avg',
    averages: Optional[pd.DataFrame] = None,
    average_label: Optional[str] = None,
    palette: pd.DataFrame = None,
):
    """
    Draw a beeswarm plot of the data.

    Parameters
        - data: The data to plot
        - value_metric: The metric to plot
        - group_by: The column to group by
        - orientation: The orientation of the plot
        - ax_min: The minimum value of the value axis
        - ax_max: The maximum value of the value axis
        - order: The order of the categories. If 'avg', order by average value,
        if 'min', order by minimum value, if 'max', order by maximum value
        - averages: Averages to plot. Categories must match those in data
        - average_label: The label for the average line in the legend
        - palette: The colour palette to use

    Returns
        None

    Notes
        - This automatically scales dot size until it fits the plot

    Future enhancements
        - Implement orientation='vertical'
    """

    # Raise arg errors
    if order == 'avg':
        if averages is None:
            raise ValueError("Averages must be provided to order by average")

    if averages is not None:
        if average_label is None:
            raise ValueError("Average legend label must be provided if averages are provided")

    # Handle ordering
    if order == 'avg':
        categories = averages.groupby(
            group_by
        )[value_metric].min().sort_values().index

    elif order == 'min':
        categories = data.groupby(
            group_by
        )[value_metric].min().sort_values().index

    elif order == 'max':
        categories = data.groupby(
            group_by
        )[value_metric].max().sort_values().index

    elif isinstance(order, list):
        categories = order

    # Create a copy of the data
    # NB: This fends off issues with ordering if the function is called
    # multiple times on the same data
    data = data.copy()
    if averages is not None:
        averages = averages.copy()

    # Turn data, averages categories into categorical
    data[group_by] = pd.Categorical(
        data[group_by],
        ordered=True,
        categories=categories
    )

    if averages is not None:
        averages[group_by] = pd.Categorical(
            averages[group_by],
            ordered=True,
            categories=categories
        )

    # Produce chart
    dot_size = 10

    while dot_size > 0:
        try:

            # Set axis min and max
            if orientation == 'horizontal':
                plt.xlim(ax_min, ax_max)

            # Add vertical gridlines
            if orientation == 'horizontal':
                plt.grid(axis='x')

            # Remove axis tick marks
            plt.tick_params(
                axis='both',
                which='both',
                bottom=False,
                left=False,
            )

            # Remove border
            plt.box(False)

            # Draw averagess
            if averages is not None:
                ax = sns.scatterplot(
                    x=value_metric,
                    y=group_by,
                    marker='|',
                    linewidth=2,
                    color='#333F48',
                    s=250,
                    zorder=4,
                    data=averages
                )

                # Add manual legend item
                # NB: This is necessary because we only have a single category
                # of average, meaning it will not appear in the legend
                legend_line = mlines.Line2D(
                    [], [],
                    color='#333F48',
                    label=average_label,
                    linestyle='-',
                    linewidth=2,
                )
                ax.legend(handles=[legend_line])

            else:
                ax = plt.gca()

            # Produce plot
            sns.swarmplot(
                x=value_metric,
                y=group_by,
                data=data,
                hue=group_by,
                palette=palette,
                size=dot_size,
                order=categories,
                ax=ax
            )

            # Set axis label
            # NB: This needs to be after creation of the plot,
            # otherwise default labels are added
            plt.xlabel('')
            plt.ylabel('')

        except UserWarning:
            dot_size -= 0.5
            plt.clf()
            pass

        else:
            print(f"Dot size: {dot_size}")
            break

    return
