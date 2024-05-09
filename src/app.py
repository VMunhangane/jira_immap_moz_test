
# importing lybraries
from dash import Dash, dcc
from dash import html 
import dash_bootstrap_components as dbc
import pandas as pd
#from datetime import date
from datetime import datetime as dt
import calendar
from dash_extensions import Lottie
from dash.dependencies import Input, Output
import plotly.express as px
#from wordcloud import WordCloud


# creating a dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

# import data from csv sheets **********************************************************
agency_type_immap_id_labels_df_2 = pd.read_csv('agency_type_immap_id_labels_df_2.csv', low_memory=False, encoding="iso-8859-1")
IM_service_request_df = pd.read_csv('IM_service_request_df.csv', low_memory=False, encoding="iso-8859-1")
capacity_building_df = pd.read_csv('capacity_building_df.csv', low_memory=False, encoding="iso-8859-1")
dfIssues = pd.read_csv('dfIssues.csv', low_memory=False, encoding="iso-8859-1")

# Craetind data registration data frame
df_registration = dfIssues.copy()
df_registration["created_date"] = pd.to_datetime(df_registration["created_date"])
df_registration = df_registration.sort_values(by="created_date")

# Calculate the timestamps for each year
start_date = df_registration["created_date"][0]
end_date = dt.now()
years_range = range(start_date.year, end_date.year + 1)  # Include the current year
timestamps = [int(dt(year, 1, 1).timestamp()) for year in years_range]

# creating a copy of dfIssues dataframe
df_issues = dfIssues.copy()
df_issues["created_date"] = pd.to_datetime(list(df_issues["created_date"]))
df_issues["month"] = df_issues["created_date"].dt.month
df_issues["year"] = df_issues["created_date"].dt.year
df_issues["month"] = df_issues["month"].apply(lambda x: calendar.month_abbr[x])

# Calculating the number of received requests
requests_number = len(dfIssues)

# Calculating the number of closed requests
requests_closed = len(dfIssues[dfIssues["Status"] == "Done"])

# Calculating the number of opened requests
requests_opened = requests_number-len(dfIssues[dfIssues["Status"] == "Done"])

# Calculating the number of organizations assisted
# creating a copy of IM_service_request_df and capacity_building_df dataframe
df_forms_sr = IM_service_request_df.copy()
df_forms_cb = capacity_building_df.copy()
list_organizations_assisted = list(df_forms_cb["agency_name.text"].unique()) + list(df_forms_sr["agency_name.text"].unique())
organizations_assisted_number = len(set(list_organizations_assisted))

# Putting agency_type label into df_issues dataframe.
df_agency_type_sr= IM_service_request_df[["Key","agency_type.choices"]].copy()
df_agency_type_cb= capacity_building_df[["Key","agency_type.choices"]].copy()
df_agency_type_df = pd.concat([df_agency_type_sr, df_agency_type_cb], ignore_index=True)
df_agency_type_df["agency_type.choices"] =  df_agency_type_df["agency_type.choices"].apply(lambda x: x[2])
df_agency_type_df["agency_type.label"] = ['Academia' if v == "1" else 'Government Agency' if v == "5" else 'INGO' if v=="2" else 'NNGO' if v=="3" else 'UN Agency' if v=="4" else 'Other' for v in list(df_agency_type_df["agency_type.choices"])]
# Merge the two DataFrames based on the 'key' column
df_issues_agency_type = pd.merge(df_agency_type_df, df_issues, on='Key', how='outer')
#print(df_issues_agency_type)

# Lottie configuration and links
options= dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio= "xMidYMid slice"))
# Lottie links
url_requests="https://lottie.host/4a6b010f-4491-45b0-bf6e-68d50468cd33/Rvqi4Y7NQs.json"
url_closed = "https://lottie.host/3a5ea5b7-850a-426a-bdb9-44add947c729/tKGsMKpp6x.json"
url_opened = "https://lottie.host/f8f7dff5-c23d-4698-973c-a8d5b5d549d2/qCgO410bHU.json"
url_organizations = "https://lottie.host/f7cf21e3-9654-4bfd-937e-f5c50e6cebf0/xi4PnpesG1.json"
url_reactions = "https://lottie.host/bd42d6a9-8df3-4417-8e12-f226405b5078/tFWFHVr2KC.json"
url_adsv_clicked= "https://lottie.host/b69a8eb1-bf27-4ccc-8c0d-11fcc8f65967/T56YbMD0DY.json"

app.layout = dbc.Container([
    # defining the first row
    dbc.Row([

        # # column with card 1_1
        # dbc.Col([
        #     dbc.Card([
        #         dbc.CardImg(src='/assets/linkedin_logo.png', style={'height':'70%','width':'70%'}, className = 'align-self-center'),
        #         dbc.CardLink("Analysis suported by Moz-DS", target="_blank",
        #                          href="https://www.youtube.com/channel/UCEeAvhcsyrPKafvsGHmfRPQ"
        #             ),
        #     ],style = {"textAlign": "center"}, className="mb-2 border-0 bg-transparent"),

        # ], width=3),


        # column with card 1_2
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='/assets/admin-ajax_usaid_immap.jpg', style={'height':'70%','width':'70%'}, className = 'align-self-center'),
                # dbc.CardLink("iMMAP inc", target="_blank",
                #                  href="https://www.youtube.com/channel/UCEeAvhcsyrPKafvsGHmfRPQ"
                #     ),
            ],style = {"textAlign": "left"}, className="mb-2 border-0 bg-transparent"),

        ], width=7),

        # column with card 1_2
        dbc.Col([
            dbc.Card([
                dbc.CardBody([

        dcc.RangeSlider(
        id='date-range-slider',
        marks={timestamp: str(dt.fromtimestamp(timestamp).year) for timestamp in timestamps},
        min=timestamps[0],
        max=timestamps[-1],
        value=[timestamps[0], timestamps[-1]],
        step=None,)
                ])
            ],className="mb-2 border-0 bg-transparent" ), #color="white"

        ], width=5),

                # column with card 1_1
        # dbc.Col([
        #     dbc.Card([
        #         dbc.CardImg(src='assets\8. IMOVTAM.jpg', style={'height':'20%','width':'20%'}, className = 'align-self-center'),
        #         dbc.CardLink("Venâncio Munhangane", target="_blank",
        #             href="https://www.linkedin.com/in/ven%C3%A2ncio-tobias-a-munhangane-652436161/"),
        #     ], style = {"textAlign": "center"}, className="mb-2 border-0 bg-transparent align-self-center"),
        # ], width=2),
    ], className='mb-3 mt-3'),

    # defining the second row
    dbc.Row([
        # column 2_1
        dbc.Col([
            dbc.Card([
                    dbc.CardHeader(Lottie(options=options, width="35%", height="35%", url=url_requests)),
                    dbc.CardBody([
						html.H2(id ="content_connections", children=requests_number),
                        html.H6("Total requests received") 
                        
                    ], style = {"textAlign": "center"})

                ]),
            
        ], width=3),
		
        # column 2_4
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="35%", height="35%", url=url_organizations)),
                dbc.CardBody([
					html.H2(id="content_invites_sen", children=organizations_assisted_number),
                    html.H6("Organizations assisted"),
                ],style={"textAlign": "center"})
            ]),
            
        ], width=3),

        # column 2_2
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="35%", height="35%", url=url_closed)),
                dbc.CardBody([
					html.H2(id="content_companies", children=requests_closed),
                    html.H6("Resolved requests"),
                ], style={"textAlign": "center"})
            ]),
            
        ], width=3),

        # column 2_3
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="37%", height="37%", url=url_opened)),
                dbc.CardBody([
					html.H2(id="content_invites_rec", children=requests_opened),
                    html.H6("Unresolved requests"),
                ],style={"textAlign": "center"})
            ]),
            
        ], width=3),



    #     # column 2_5
    #     dbc.Col([
    #         dbc.Card([
    #             dbc.CardHeader(Lottie(options=options, width="42%", height="50%", url=url_reactions)),
    #             dbc.CardBody([
    #                 html.H6("REACTIONS"),
    #                 html.H2(id="content_reaction", children=reactions_number)


    #             ],style={"textAlign": "center"})
    #         ]),
            
    #     ], width=2),


    #     # column 2_6
    #     dbc.Col([
    #         dbc.Card([
    #             dbc.CardHeader(Lottie(options=options, width="42%", height="50%", url=url_adsv_clicked)),
    #             dbc.CardBody([
    #                 html.H6("ADS CLICKED"),
    #                 html.H2(id="content_click", children=ads_clicked_number)


    #             ],style={"textAlign": "center"})
    #         ]),
            
    #     ], width=2),

    ], className='mb-3'),

    # defining the third row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="line_chart", figure={})

                ])
            ], ), #className="border-0 bg-transparent"
        ], width=7),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="horizontal_bar_chart", figure={})

                ])
            ], ), #className="border-0 bg-transparent"
        ], width=5)
    ], className='mb-3'),

    # defining the fourth row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="vertical_bar_chart", figure={})

                ])
            ],), # className="border-0 bg-transparent"
        ], width=4),


        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="pie_chart", figure={})

                ])
            ], ), # className="border-0 bg-transparent"
        ], width=4),


        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="word_cloud", figure={})

                ])
            ], ), #className="border-0 bg-transparent"
        ], width=4)
    ], className='mb-3')


], fluid= False)



# Updating the 6 number cards
@app.callback(
    Output("content_connections", "children"),
    Output("content_companies", "children"),
    Output("content_invites_rec", "children"),
    Input("date-range-slider", "value")
)

def update_cards(date_range):

    # coping the original dataframes
    df_connections_copy = df_issues.copy()


    # Picking the years from the date slicer
    start_date = dt.fromtimestamp(date_range[0]).year
    end_date = dt.fromtimestamp(date_range[1]).year
	
   
    # Filtering the Connections dataframe
    df_connections_copy = df_connections_copy[(df_connections_copy["year"] >= start_date) & (df_connections_copy["year"] <= end_date)]
    requests_number = len(df_connections_copy)

    # Companies dataframe
    requests_closed = len(dfIssues[dfIssues["Status"] == "Done"])
	

    # Invitations dataframe
    requests_opened = requests_number - requests_closed

    #print(list(df_connections_copy.columns))
    return requests_number, requests_closed, requests_opened, #sent_invetations_number, reactions_number, ads_clicked_number


# line chart *******************************************************************
@app.callback(
    Output("line_chart", "figure"),
    Input("date-range-slider", "value")
)

def update_line_chart(date_range):

        # Picking the years from the date slicer
    start_date = dt.fromtimestamp(date_range[0]).year
    end_date = dt.fromtimestamp(date_range[1]).year
	
    # coping the original dataframes
    df_connections_copy = df_issues.copy()

    # filtering the dataframe using the picked years from the date slicer
    df_connections_copy = df_connections_copy[(df_connections_copy["year"] >= start_date) & (df_connections_copy["year"] <= end_date)]
    df_connections_copy["created_date"] = pd.to_datetime(df_connections_copy["created_date"])
    df_connections_copy["month"] = df_connections_copy["created_date"].dt.month
    df_connections_copy["month_abv"] = df_connections_copy["month"].apply(lambda x: calendar.month_abbr[x])
    df_connections_copy["year"] = df_connections_copy["created_date"].dt.year

    df_month= df_connections_copy.groupby(["month","month_abv"] )["ID"].count().reset_index()
    df_month.rename(columns={"ID": "Total requested"}, inplace=True)

    line_chart = px.line(df_month, x="month_abv", y="Total requested", text="Total requested", title="Total requests by month", template="ggplot2")
    line_chart.update_traces(mode="markers+lines+text", fill="tozeroy", line=dict(color="blue"))
    line_chart.update_layout(title_x=0.5, xaxis_title="Month", yaxis_title="Total requests", font=dict(family="Arial", size=11, color="black"))
    line_chart.update_layout(margin=dict(l=10, r=10, t=23, b=20))

    return line_chart
    

    # bar chart *******************************************************************
@app.callback(
    Output("horizontal_bar_chart", "figure"),
    Input("date-range-slider", "value")    
)

def update_horizontal_bar_chart(date_range):

    # Picking the years from the date slicer
    start_date = dt.fromtimestamp(date_range[0]).year
    end_date = dt.fromtimestamp(date_range[1]).year

    # coping the original dataframes
    df_connections_copy = df_issues.copy()

    # filtering the dataframe using the picked years from the date slicer
    df_connections_copy = df_connections_copy[(df_connections_copy["year"] >= start_date) & (df_connections_copy["year"] <= end_date)]

    df_companies = df_connections_copy.groupby(["Status"])["ID"].count().reset_index()
    df_companies = df_companies.sort_values(by="Status", ascending=False).head(10)
    df_companies.rename(columns={"ID": "Total requested"}, inplace=True)
    
    bar_chart= px.bar(df_companies, x="Total requested", y="Status", text="Total requested", title="Total requets by status", template="ggplot2", orientation="h")
    bar_chart.update_layout(title_x=0.5, xaxis_title="Number of requests", yaxis_title="Status", font=dict(family="Arial", size=11, color="black"))
    bar_chart.update_layout(margin=dict(l=10, r=10, t=23, b=20))
    bar_chart.update_traces(marker_color="blue", marker_line_color="blue", marker_line_width=1.5, opacity=0.6)

    return bar_chart

# tbd chart *******************************************************************
@app.callback(
    Output("vertical_bar_chart", "figure"),
    Input("date-range-slider", "value")
)

def update_vertical_bar_chart(date_range):

    # Picking the years from the date slicer
    start_date = dt.fromtimestamp(date_range[0]).year
    end_date = dt.fromtimestamp(date_range[1]).year

    # coping the original dataframes
    df_reactions_copy = df_issues.copy()

    # filtering the dataframe using the picked years from the date slicer
    df_reactions_copy = df_reactions_copy[(df_reactions_copy["year"] >= start_date) & (df_reactions_copy["year"] <= end_date)]

    df_reactions_copy = df_reactions_copy.groupby(["Summary"] )["ID"].count().reset_index()
    df_reactions_copy.rename(columns={"ID": "Total requested", "Summary": "Service requested"}, inplace=True)


    bar_chart= px.bar(df_reactions_copy, x="Service requested", y="Total requested", text="Total requested", title="Total service requested by type", template="ggplot2")
    bar_chart.update_layout(title_x=0.5, font=dict(family="Arial", size=12, color="black"))
    bar_chart.update_layout(title_x=0.5, xaxis_title="Service requested", yaxis_title="Total requested", font=dict(family="Arial", size=11, color="black"))
    bar_chart.update_layout(margin=dict(l=10, r=10, t=23, b=20))
    bar_chart.update_traces(marker_color="blue", marker_line_color="blue", marker_line_width=1.5, opacity=0.6)

    return bar_chart


# # Pie chart *******************************************************************
@app.callback(
    Output("pie_chart", "figure"),
    Input("date-range-slider", "value")
)

def update_pie_chart(date_range):
	

    # Picking the years from the date slicer
    start_date = dt.fromtimestamp(date_range[0]).year
    end_date = dt.fromtimestamp(date_range[1]).year
	
    df_issues_agency_type_copy= df_issues_agency_type.copy()
	
    # filtering the dataframe using the picked years from the date slicer df_issues_agency_type_copy
    df_issues_agency_type_copy = df_issues_agency_type_copy[(df_issues_agency_type_copy["year"] >= start_date) & (df_issues_agency_type_copy["year"] <= end_date)]

    df_issues_agency_type_copy = df_issues_agency_type_copy.groupby(["agency_type.label"] )["Key"].count().reset_index()
    #print(df_issues_agency_type_copy)
    
    pie_chart = px.pie(names=df_issues_agency_type_copy["agency_type.label"], values = df_issues_agency_type_copy["Key"], title="Total type of agency", template="ggplot2")
    pie_chart.update_layout(title_x=0.5, font=dict(family="Arial", size=11, color="black"))
    pie_chart.update_layout(margin=dict(l=10, r=10, t=23, b=20))
    pie_chart.update_legends(dict(orientation="h" , yanchor="bottom",  y=-0.05,   xanchor="right",   x=0.9))
    pie_chart.update_traces(marker_colors=[  "blue", "red"])
    return pie_chart
    

# # Word Cloud *******************************************************************
# @app.callback(
#     Output("word_cloud", "figure"),
#     Input("date-range-slider", "value")
# )

# def update_word_cloud(date_range):

#     # Picking the years from the date slicer
#     start_date = dt.fromtimestamp(date_range[0]).year
#     end_date = dt.fromtimestamp(date_range[1]).year

#     # coping the original dataframes   
#     df_connections_copy = df_connections.copy()
#     df_connections_copy = df_connections_copy[(df_connections_copy["year"] >= start_date) & (df_connections_copy["year"] <= end_date)]
#     df_connections_copy["Position"].astype(str)

#     my_world_cloud = WordCloud(width=800, height=600, background_color="white", max_words=100).generate(" ".join(df_connections_copy["Position"].astype(str)))
#     fig_worldcloud = px.imshow(my_world_cloud, template="ggplot2", title="Total connections by position")
#     fig_worldcloud.update_layout(title_x=0.5, font=dict(family="Arial", size=12, color="black"))
#     fig_worldcloud.update_layout(margin=dict(l=10, r=10, t=23, b=20))
#     fig_worldcloud.update_xaxes(visible=False)
#     fig_worldcloud.update_yaxes(visible=False)

#     return fig_worldcloud



if __name__ == "__main__":
    app.run(debug=True)