from typing import Literal, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def draw_beeswarm(
    data: pd.DataFrame,
    value_metric: str,
    group_by: str,
    orientation: Literal['horizontal'] = 'horizontal',
    ax_min: Optional[int] = 0,
    ax_max: Optional[int] = 100,
    averages: Optional[pd.DataFrame] = None,
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
        - averages: Averages to plot. Categories must match those in data
        - palette: The colour palette to use

    Returns
        None

    Notes
        - This automatically scales dot size until it fits the plot

    Future enhancements
        - Implement orientation='vertical'
    """

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
                    legend=False,
                    data=averages.sort_values(
                        value_metric
                    )
                )
                order = None
            else:
                ax = plt.gca()

                # Create order variable, ordering categories by lowest value
                order = data.sort_values(
                    [value_metric],
                    ascending=True
                )[group_by].unique()

            # Produce plot
            sns.swarmplot(
                x=value_metric,
                y=group_by,
                data=data,
                hue=group_by,
                palette=palette,
                size=dot_size,
                order=order,
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
