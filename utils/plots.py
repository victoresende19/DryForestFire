from pandas import DataFrame
import plotly.express as px


def line_plot(df: DataFrame, column_x: str, column_y: str, title: str, color: str):
    """
    Description
    -----------
    Cria um gráfico de lineplot.

    Parameters
    ----------
    df: DataFrame
        DataFrame do qual será utilizado para o gráfico.

    column_x: str
        Eixo X do gráfico.

    column_y: str
        Eixo Y do gráfico.

    title: str
        Título do gráfico.
    
    color: str
        Cor do gráfico.

    Returns
    -------
    Gráfico lineplot da biblioteca plotly.
    """

    fig = px.line(df, x=column_x, y=column_y,
                  line_shape='spline',
                  color_discrete_sequence=[color])
    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        title={
            'text': title,
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig
