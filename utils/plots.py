from pandas import DataFrame
import plotly.express as px


def line_plot(df: DataFrame, column_x: str, column_y: str, title: str, color_chart: str):
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
    
    color_chart: str
        Cor do gráfico.

    Returns
    -------
    Gráfico lineplot da biblioteca plotly.
    """

    fig = px.line(df, x=column_x, y=column_y,
                  line_shape='spline',
                  color_discrete_sequence=[color_chart])
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


def bar_plot(df: DataFrame, column_x: str, column_y: str, title: str, color_column: str, color_chart:str):
    """
    Description
    -----------
    Cria um gráfico de barplot.

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

    color_column: str
        Cor do gráfico de acordo com uma coluna.

    color_chart: str
        Cor das barras.

    Returns
    -------
    Gráfico barplot da biblioteca plotly.
    """

    fig = px.bar(df, x=column_x, y=column_y,
                 text_auto=True,
                 color=color_column,
                 color_continuous_scale=color_chart)
    fig.update_traces(textfont_size=12, textangle=0, 
                      marker_line_color='black',
                      marker_line_width=1.5,
                      textposition="outside", cliponaxis=False)
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
