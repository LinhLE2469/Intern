from __future__ import annotations
from pathlib import Path
from re import X
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from service import (
    load_data, filter_by_medal_year, group_by_team_and_sex,
    filter_by_year, filter_by_gender_year, get_medals_by_team,
    group_by_sport_and_sex, group_by_sport_and_country, filter_by_gender,
    group_by_athlete, count_athletes_medals_by_medals
)


app = Dash(__name__)

# Load data
DATASET_PATH = Path().cwd().joinpath(
    'data', 'all-year-olympic-dataset-with-2020-tokyo-olympics.csv')
df = load_data(DATASET_PATH)

app.layout = html.Div(
    className='container',
    children=[
        html.Div(
            className='text-center py-5',
            children=[
                html.H1(
                    className='text-center mb-2 display-4',
                    children='Olympic Games Analysis Dashboard'
                ),
                html.P(
                    className='text-muted',
                    children='''This dashboard is a simple analysis of all the Olympic Games ever organised.'''
                )
            ]
        ),

        html.Div(
            className='pb-5',
            children=[
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-light fs-3 mb-4',
                                    children='''Analysis of the Gender'''
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Gender distribution'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Filter by medals'''
                                ),
                                dcc.Dropdown(
                                    className='mb-3',
                                    options=[
                                        {'label': 'Bronze', 'value': 1},
                                        {'label': 'Silver', 'value': 2},
                                        {'label': 'Gold', 'value': 3}
                                    ],
                                    value=1,
                                    id='group-by-sex-medal-dropdown'
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='group-by-sex-year-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0}
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(id='group-by-sex')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Gender distribution by year'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='group-by-gender-year-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0}
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(id='group-by-gender')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-normal small mb-2',
                                    children='''Comments'''
                                ),
                                html.P(
                                    className='fw-light fs-6 mb-4',
                                    children=[
                                        html.P(
                                            children='''
                                                The first chart describes the distribution of gender by medals and years. It shows the number of medals per sex by sport.
                                                The map shows that females were admitted to the olympic games from 1990 with some few sports. Along the years, they joined more and more sports with Swimming and Athletics hosting the majority.
                                            '''
                                        ),
                                        html.P(
                                            children='''
                                                The second chart describes the distribution of gender by year. It shows the ratio of female and male athletes participating in the Olympic Games.
                                                The analysis of gender show that approximately 58 percent of competing athletes were male, while 42 percent were female. Male seems to be dominating in terms of participation.
                                                We also notice an increment from the female since the year they joined the games. 
                                            '''
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-light fs-3 mb-4',
                                    children='''Analysis of Age'''
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Age distribution'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Filter by medals'''
                                ),
                                dcc.Dropdown(
                                    className='mb-3',
                                    options=[
                                        {'label': 'Bronze', 'value': 1},
                                        {'label': 'Silver', 'value': 2},
                                        {'label': 'Gold', 'value': 3}
                                    ],
                                    value=1,
                                    id='group-by-age-medal-dropdown'
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='group-by-age-year-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0}
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(id='group-by-age')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Age distribution by gender(boxplot)'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='group-by-age-year-box-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0}
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(id='group-by-agebox')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-normal small mb-2',
                                    children='''Comments'''
                                ),
                                html.P(
                                    className='fw-light fs-6 mb-4',
                                    children=[
                                        html.P('''
                                            The histogram shows the age distribution by sex, filtered by medals and years.
                                            Most gold and bronze medals winners are in their 20s while silver winners are in their 30s. 
                                        '''),
                                        html.P('''
                                            The boxplot describes the age distribution by gender, which shows athletes' min, max, and average age.
                                            From the graph, we observe maximum participants are of age between 23–37 years in 2020 with female being younger.
                                        ''')
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-light fs-3 mb-4',
                                    children='''Analysis of the Countries'''
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Medal distribution'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Filter by medals'''
                                ),
                                dcc.Dropdown(
                                    className='mb-3',
                                    options=[
                                        {'label': 'Bronze', 'value': 1},
                                        {'label': 'Silver', 'value': 2},
                                        {'label': 'Gold', 'value': 3}
                                    ],
                                    value=1,
                                    id='country-by-medal-dropdown'
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='country-by-medal-year-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0},
                                ),
                                html.Div(
                                    className='mb-3',
                                    children=[
                                        dcc.Graph(id='country-by-medal')
                                    ]
                                ),
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Country's medal distribution'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select country'''
                                ),
                                dcc.Dropdown(
                                    className='mb-3',
                                    options=df['Team'].unique().tolist(),
                                    value='United States',
                                    id='country-medals-dropdown'
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(id='country-medals')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-normal small mb-2',
                                    children='''Comments'''
                                ),
                                html.P(
                                    className='fw-light fs-6 mb-4',
                                    children=[
                                        html.P('''
                                            The bar chart shows the distribution of medals by country, filtered by year and the type of medal.
                                            China seems to lead the Gold medal charts for the last held Olympics in the year 2020 but in 2016 US have won the most gold medals.
                                            Russia also appears severally in the top 5 of the bronze medals charts.
                                        '''),
                                        html.P('''
                                            The pie chart shows the distribution of all medals by country, filtered by country.
                                            In pie chart we can see that US has the most total medals(5219) compare to China(901).
                                        ''')
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-light fs-3 mb-4',
                                    children='''Analysis of Seasons'''
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Season participation by countries'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='season-by-country-year-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0}
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(id='season-by-country')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-normal small mb-2',
                                    children='''Comments'''
                                ),
                                html.P(
                                    className='fw-light fs-6 mb-4',
                                    children=[
                                        html.P('''
                                            From the above chart, we can assume that winter games are not as popular as summer games, 
                                            because games such as skiing require snow or a cold climate, and certain areas of the world don't have such a climate.
                                        ''')
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-light fs-3 mb-4',
                                    children='''Analysis of the Sports'''
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Sport participation'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Filter by gender'''
                                ),
                                dcc.Dropdown(
                                    className='mb-3',
                                    options=['Male', 'Female'],
                                    value='Male',
                                    id='sport-participation-dropdown'
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='sport-participation-year-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0},
                                ),
                                html.Div(
                                    className='mb-3',
                                    children=[
                                        dcc.Graph(id='sport-participation')
                                    ]
                                ),
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Sport gender distribution'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='sport-gender-distribution-year-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0},
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(
                                            id='sport-gender-distribution')
                                    ]
                                ),
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''The distribution of sport by country'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='country-distribution-year-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0},
                                ),
                                html.Div(
                                    children=[
                                        dcc.Graph(
                                            id='sport-counrty-distribution')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-normal small mb-2',
                                    children='''Comments'''
                                ),
                                html.P(
                                    className='fw-light fs-6 mb-4',
                                    children=[
                                        html.P('''
                                            The treemap shows the sports participation in Olympic Games, filtered by gender and year.
                                            Athletes participate most in Athletics, followed by Swimming.
                                            The games least engaged in are Equestrian, Wheelchair Rugby and Wheelchair Tennis.
                                        '''),
                                        html.P('''
                                            The first scatter plot shows the sports distribution by gender, filtered by year.
                                            Although most sports are dominated by males, females are catching up in some sports like rowing.
                                        '''),
                                        html.P('''
                                            The second scatter plot shows the distribution of sport by country, filtered by year.
                                            The united states is the most active country in the Olympics.
                                        ''')
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='row mb-4',
                    children=[
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-light fs-3 mb-4',
                                    children='''Analysis of the Athelts'''
                                ),
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Ranking of the top 7 male and female athletes'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Filter by medals'''
                                ),
                                dcc.Dropdown(
                                    className='mb-3',
                                    options=[
                                        {'label': 'Bronze', 'value': 1},
                                        {'label': 'Silver', 'value': 2},
                                        {'label': 'Gold', 'value': 3}
                                    ],
                                    value=1,
                                    id='athlet-by-medal-dropdown'
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Select the year'''
                                ),
                                dcc.Slider(
                                    df['Year'].min(),
                                    df['Year'].max(),
                                    className='mb-3',
                                    step=None,
                                    id='athlet-by-medal-year-slider',
                                    value=df['Year'].max(),
                                    marks={str(year): str(year)
                                           for year in df['Year'].unique() if year % 4 == 0},
                                ),
                                html.Div(
                                    className='mb-3',
                                    children=[
                                        dcc.Graph(id='athlet-by-medal')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-6',
                            children=[
                                html.P(
                                    className='fw-light fs-5 mb-2',
                                    children='''Ranking of the top 10 male and female athletes of all times'''
                                ),
                                html.P(
                                    className='mb-1 small',
                                    children='''Filter by medals'''
                                ),
                                dcc.Dropdown(
                                    className='mb-3',
                                    options=[
                                        {'label': 'Bronze', 'value': 1},
                                        {'label': 'Silver', 'value': 2},
                                        {'label': 'Gold', 'value': 3}
                                    ],
                                    value=3,
                                    id='athlete-medal-count-dropdown'
                                ),
                                html.Div(
                                    className='mb-3',
                                    children=[
                                        dcc.Graph(id='athlete-medal-count')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='col-md-12',
                            children=[
                                html.P(
                                    className='fw-normal small mb-2',
                                    children='''Comments'''
                                ),
                                html.P(
                                    className='fw-light fs-6 mb-4',
                                    children=[
                                        html.P('''
                                            Michael Fred Phelps has the most gold medal in the Olympics followed by Raymond Clarence.
                                            Alexander Popov leads the silver and bronze medal rankings.
                                        ''')
                                    ]
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)

# Empty state for the graphs
empty_state = go.Figure()
empty_state.update_layout(
    xaxis={'visible': False},
    yaxis={'visible': False},
    annotations=[
        {
            "text": 'No data available',
            "showarrow": False,
            "font": {
                "family": 'Roboto',
                "size": 20
            }
        }
    ]
)


@app.callback(
    Output('group-by-sex', 'figure'),
    Input('group-by-sex-medal-dropdown', 'value'),
    Input('group-by-sex-year-slider', 'value')
)
def update_figure_group_by_sex_with_filters(selected_medal, selected_year):
    """Callback for graph id - group-by-sex"""
    _df = filter_by_medal_year(
        df, selected_medal, selected_year)

    if len(_df) == 2:
        fig = empty_state
    else:
        fig = px.treemap(
            _df,
            path=[px.Constant('all'), 'Sex', 'Sport'],
            height=500,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(
            root_color='lightgrey',
            textinfo='label+value'
        )

    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('group-by-age', 'figure'),
    Input('group-by-age-medal-dropdown', 'value'),
    Input('group-by-age-year-slider', 'value')
)
def update_figure_group_by_age_with_filters(selected_medal, selected_year):
    """Callback for graph id - group-by-age"""
    _df = filter_by_medal_year(
        df, selected_medal, selected_year)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.histogram(
            _df,
            x='Age',
            nbins=20,
            height=500,
            color='Sex',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('country-by-medal', 'figure'),
    Input('country-by-medal-dropdown', 'value'),
    Input('country-by-medal-year-slider', 'value')
)
def update_figure_country_by_medal_with_filters(selected_medal, selected_year):
    """Callback for graph id - country-by-medal"""
    _df = group_by_team_and_sex(
        df, selected_medal, selected_year)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.bar(
            _df,
            x=_df.index.to_list(),
            y=_df.values,
            height=500,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            xaxis_title='Medal Count',
            yaxis_title='Country',
            transition_duration=500
        )

    fig.update_layout(transition_duration=300)
    return fig


@app.callback(
    Output('season-by-country', 'figure'),
    Input('season-by-country-year-slider', 'value')
)
def update_figure_season_by_country_with_filters(selected_year):
    """Callback for graph id - season-by-country"""
    _df = filter_by_year(
        df, selected_year)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.treemap(
            _df,
            path=[px.Constant('all'), 'Season', 'Team'],
            height=500,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(
            root_color='lightgrey',
            textinfo='label+value'
        )

    fig.update_layout(transition_duration=300)
    return fig


@app.callback(
    Output('sport-participation', 'figure'),
    Input('sport-participation-dropdown', 'value'),
    Input('sport-participation-year-slider', 'value')
)
def update_figure_sport_participation_with_filters(selected_gender, selected_year):
    """Callback for graph id - sport-participation"""
    _df = filter_by_gender_year(
        df, selected_gender, selected_year)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.treemap(
            _df,
            path=[px.Constant('all'), 'Sport'],
            height=500,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(
            root_color='lightgrey',
            textinfo='label+value'
        )

    fig.update_layout(transition_duration=300)
    return fig


@app.callback(
    Output('country-medals', 'figure'),
    Input('country-medals-dropdown', 'value')
)
def update_figure_country_medals_with_filters(selected_team):
    """Callback for graph id - country-medals"""
    _df = get_medals_by_team(
        df, selected_team)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.pie(
            _df,
            names=['Gold', 'Silver', 'Bronze', 'No Medals'],
            values=_df.values,
            height=500,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(
            textinfo='label+percent+value'
        )

    fig.update_layout(transition_duration=300)
    return fig


@app.callback(
    Output('sport-gender-distribution', 'figure'),
    Input('sport-gender-distribution-year-slider', 'value')
)
def update_figure_season_by_country_with_filters(selected_year):
    """Callback for graph id - sport-gender-distribution"""
    _df = group_by_sport_and_sex(
        df, selected_year)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.scatter(
            _df,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

    fig.update_layout(transition_duration=300)
    return fig


@app.callback(
    Output('sport-counrty-distribution', 'figure'),
    Input('country-distribution-year-slider', 'value')
)
def update_figure_season_by_country_with_filters(selected_year):
    """Callback for graph id - sport-country-distribution"""
    _df = group_by_sport_and_country(
        df, selected_year)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.scatter(
            _df,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

    fig.update_layout(transition_duration=300)
    return fig


@app.callback(
    Output('group-by-gender', 'figure'),
    Input('group-by-gender-year-slider', 'value')
)
def update_figure_group_by_sex_with_filters(selected_year):
    """Callback for graph id - country-medals"""
    _df = filter_by_gender(
        df, selected_year)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.pie(
            _df,
            names=['Male', 'Female'],
            values=_df.values,
            height=500,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(
            textinfo='label+percent+value'
        )
    fig.update_layout(transition_duration=300)
    return fig


@app.callback(
    Output('group-by-agebox', 'figure'),
    Input('group-by-age-year-box-slider', 'value')
)
def update_figure_group_by_age_with_filters(selected_year):
    """Callback for graph id - group-by-age"""
    _df = filter_by_year(
        df, selected_year)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.box(
            _df,
            x='Sex',
            y='Age',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('athlet-by-medal', 'figure'),
    Input('athlet-by-medal-dropdown', 'value'),
    Input('athlet-by-medal-year-slider', 'value')
)
def update_figure_athlete_by_medal_with_filters(selected_medal, selected_year):
    """Callback for graph id - athlete-by-medal"""
    _df = group_by_athlete(
        df, selected_medal, selected_year)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.bar(
            _df,
            x='Name',
            y='Medal',
            height=500,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            xaxis_title='Athlet name',
            yaxis_title='Medal Count',
            transition_duration=500
        )

    fig.update_layout(
        transition_duration=300,
    )
    return fig


@app.callback(
    Output('athlete-medal-count', 'figure'),
    Input('athlete-medal-count-dropdown', 'value'),
)
def update_figure_athlete_medal_count_by_medal(selected_medal):
    """Callback for graph id - athlete-medal-count"""
    _df = count_athletes_medals_by_medals(df, selected_medal)

    if len(_df) == 0:
        fig = empty_state
    else:
        fig = px.bar(
            _df,
            x=_df.index.to_list(),
            y=_df.values,
            height=500,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            xaxis_title='Athlete name',
            yaxis_title='Medal Count',
            transition_duration=500
        )

    fig.update_layout(
        transition_duration=300,
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
