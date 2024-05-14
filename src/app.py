# importing lybraries
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime as dt
import calendar
from dash_extensions import Lottie
from dash.dependencies import Input, Output
import plotly.express as px


# creating a dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server


# import data from csv sheets **********************************************************
agency_type_immap_id_labels_df_2 = pd.read_csv('agency_type_immap_id_labels_df_2.csv', low_memory=False, encoding="iso-8859-1")
IM_service_request_df = pd.read_csv('IM_service_request_df.csv', low_memory=False, encoding="iso-8859-1")
capacity_building_df = pd.read_csv('capacity_building_df.csv', low_memory=False, encoding="iso-8859-1")
dfIssues = pd.read_csv('dfIssues.csv', low_memory=False, encoding="iso-8859-1")

# temporary
summary_list = ["IM Service Request", "Capacity Building" ]
dfIssues = dfIssues[dfIssues['Summary'].isin(summary_list)]

# Craetind data registration data frame
df_registration = dfIssues.copy()
df_registration["created_date"] = pd.to_datetime(df_registration["created_date"])
df_registration = df_registration.sort_values(by="created_date")

# Calculate the timestamps for each year
start_date = df_registration["created_date"].min()
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

# Creating agency_type dataframe.
df_agency_type_sr= IM_service_request_df[["Key",'agency_type.choices0']].copy()
df_agency_type_cb= capacity_building_df[["Key",'agency_type.choices0']].copy()
df_agency_type_df = pd.concat([df_agency_type_sr, df_agency_type_cb], ignore_index=True)
df_issues_agency_type = pd.merge(df_agency_type_df, df_issues, on='Key', how='outer')

# Creating locations dataframe.
# locations in IM_service_request_df
list_columns_IM= [col for col in IM_service_request_df.columns if 'locations.choices' in col]
locations_IM_df = IM_service_request_df[["Key"]+list_columns_IM]

# melting locations_IM_df
locations_IM_df = pd.melt(locations_IM_df, id_vars =['Key'], value_vars =list_columns_IM, var_name ='locations', value_name ='province')

# locations in capacity_building_df
capacity_building_df["locations.choices0"]= ['Cabo Delgado', "Maputo", "Maputo"]
capacity_building_df["locations.choices1"]= [None, "Cabo Delgado", "Cabo Delgado"]
capacity_building_df["locations.choices2"]= [None, None, "Nampula"]
capacity_building_df["locations.choices3"]= [None, None, "Niassa"]
capacity_building_df["locations.choices4"]= [None, None, "Zambezia"]
capacity_building_df["locations.choices5"]= [None, None, "Sofala"]
list_columns_CB= [col for col in capacity_building_df.columns if 'locations.choices' in col]
locations_CB_df= capacity_building_df[["Key"]+list_columns_CB]

# melting locations_CB_df
locations_CB_df = pd.melt(locations_CB_df, id_vars =['Key'], value_vars =list_columns_CB, var_name ='locations', value_name ='province')

# Concatinating locations_IM_df and locations_CB_df
locations_df = pd.concat([locations_IM_df, locations_CB_df], ignore_index=True)

# Concatinating locations_df and df_issues
df_issues_locations = pd.merge(locations_df, df_issues, on='Key', how='outer')

# Applying groupby on provinve
df_issues_locations = df_issues_locations.groupby(["province","year"] )["Key"].count().reset_index()
df_issues_locations = df_issues_locations.sort_values(by="Key", ascending=False)#.head(10)
df_issues_locations = df_issues_locations[df_issues_locations["province"]!="Other..."]

#requested provinces/locations must this request cover
df_issues_locations.rename(columns={"Key": "Total requested number"}, inplace=True)

# # Concatinating locations_df and df_issues
# df_issues_locations = pd.merge(locations_df, df_issues, on='Key', how='outer')

# Creating products dataframe.
# products in IM_service_request_df
products_columns_IM= [col for col in IM_service_request_df.columns if 'products.choices' in col]
products_IM_df = IM_service_request_df[["Key"]+products_columns_IM]

# melting products_IM_df
products_IM_df = pd.melt(products_IM_df, id_vars =['Key'], value_vars =products_columns_IM, var_name ='products.choices', value_name ='products')

# products in capacity_building_df
products_columns_CB= [col for col in capacity_building_df.columns if 'requirements.choices' in col]
products_CB_df= capacity_building_df[["Key"]+products_columns_CB]

# melting locations_CB_df
products_CB_df = pd.melt(products_CB_df, id_vars =['Key'], value_vars = products_columns_CB, var_name ='products.choices', value_name ='products')

# Concatinating products_IM_df and products_CB_df
products_df = pd.concat([products_IM_df, products_CB_df], ignore_index=True)

#print(products_df)

# Concatinating products_df and df_issues
df_issues_products = pd.merge(products_df, df_issues, on='Key', how='outer')
#print(df_issues_products)

# Applying groupby on products
df_issues_products = df_issues_products.groupby(["products","year"] )["Key"].count().reset_index()
df_issues_products = df_issues_products.sort_values(by="Key", ascending=False)#.head(10)

#requested products/training must this request cover
df_issues_products.rename(columns={"Key": "Total products"}, inplace=True)
#print(df_issues_products)

#df_issues_products = df_issues_products[df_issues_locations["province"]!="Other..."]


# # Concatinating locations_df and df_issues
# df_issues_locations = pd.merge(locations_df, df_issues, on='Key', how='outer')

# Creating sectors of work dataframe.
# products in IM_service_request_df
sectors_columns_IM= [col for col in IM_service_request_df.columns if 'sector_aor_wg.choices' in col]
sectors_IM_df = IM_service_request_df[["Key"]+sectors_columns_IM]

# melting products_IM_df
sectors_IM_df = pd.melt(sectors_IM_df, id_vars =['Key'], value_vars = sectors_columns_IM, var_name ='sector_aor_wg.choices', value_name ='sectors_of_work')

# products in capacity_building_df
####################################################################################
####################################################################################
####################################################################################


# Concatinating products_df and df_issues
df_issues_sectors = pd.merge(sectors_IM_df, df_issues, on='Key', how='outer')

#print(df_issues_sectors)
# Applying groupby on products
df_issues_sectors = df_issues_sectors.groupby(["sectors_of_work","year"] )["Key"].count().reset_index()
df_issues_sectors = df_issues_sectors.sort_values(by="Key", ascending=False)#.head(10)

#requested products/training must this request cover
df_issues_sectors.rename(columns={"Key": "Total sectors"}, inplace=True)
#print(df_issues_sectors)

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

    ], className='mb-3'),

    # defining the third row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="line_chart", figure={})
                ])
            ], ), #className="border-0 bg-transparent"
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="locations_bar_chart", figure={})

                ])
            ], ), #className="border-0 bg-transparent"
        ], width=6)
    ], className='mb-3'),

        # defining the fourth row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="status_chart", figure={})

                ])
            ], ), #className="border-0 bg-transparent"
        ], width=5),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="products_chart", figure={})

                ])
            ], ), #className="border-0 bg-transparent"
        ], width=7)
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
                    dcc.Graph(id="sector_chart", figure={})

                ])
            ], ), #className="border-0 bg-transparent"
        ], width=4)
    ], className='mb-3'),


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


# tbd chart *******************************************************************
@app.callback(
    Output("locations_bar_chart", "figure"),
    Input("date-range-slider", "value")
)

def update_vertical_bar_chart(date_range):

    # Picking the years from the date slicer
    start_date = dt.fromtimestamp(date_range[0]).year
    end_date = dt.fromtimestamp(date_range[1]).year

    # coping the original dataframes
    df_reactions_copy = df_issues_locations.copy()
    df_reactions_copy["percentage"] = round(df_reactions_copy["Total requested number"] / requests_number * 100,1)

    # filtering the dataframe using the picked years from the date slicer
    df_reactions_copy = df_reactions_copy[(df_reactions_copy["year"] >= start_date) & (df_reactions_copy["year"] <= end_date)]

    # df_reactions_copy = df_reactions_copy.groupby(["Summary"] )["ID"].count().reset_index()
    # df_reactions_copy.rename(columns={"ID": "Total requested", "Summary": "Service requested"}, inplace=True)


    bar_chart= px.bar(df_reactions_copy, x="province", y="percentage", text="percentage", title="Provinces impacted by the requested service", template="ggplot2")
    bar_chart.update_layout(title_x=0.5, font=dict(family="Arial", size=12, color="black"))
    bar_chart.update_layout(title_x=0.5, xaxis_title="Provinces", yaxis_title="Pecentage(%)", font=dict(family="Arial", size=11, color="black"))
    bar_chart.update_layout(margin=dict(l=10, r=10, t=23, b=20))
    bar_chart.update_traces(marker_color="blue", marker_line_color="blue", marker_line_width=1.5, opacity=0.6)

    return bar_chart
    

    # bar chart *******************************************************************
@app.callback(
    Output("status_chart", "figure"),
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
    df_companies = df_companies.sort_values(by="ID", ascending=True)
    df_companies.rename(columns={"ID": "Total requested"}, inplace=True)
    
    bar_chart= px.bar(df_companies, x="Total requested", y="Status", text="Total requested", title="Total requets by status", template="ggplot2", orientation="h")
    bar_chart.update_layout(title_x=0.5, xaxis_title="Number of requests", yaxis_title="Status", font=dict(family="Arial", size=11, color="black"))
    bar_chart.update_layout(margin=dict(l=10, r=10, t=23, b=20))
    bar_chart.update_traces(marker_color="blue", marker_line_color="blue", marker_line_width=1.5, opacity=0.6)

    return bar_chart



# tbd chart *******************************************************************
@app.callback(
    Output("products_chart", "figure"),
    Input("date-range-slider", "value")
)

def update_products_chart(date_range):

    # Picking the years from the date slicer
    start_date = dt.fromtimestamp(date_range[0]).year
    end_date = dt.fromtimestamp(date_range[1]).year

    # coping the original dataframes
    df_products_copy = df_issues_products.copy()
    df_products_copy["percentage"] = round(df_products_copy["Total products"] / requests_number * 100,1)

    # filtering the dataframe using the picked years from the date slicer
    df_products_copy = df_products_copy[(df_products_copy["year"] >= start_date) & (df_products_copy["year"] <= end_date)]

    # df_reactions_copy = df_reactions_copy.groupby(["Summary"] )["ID"].count().reset_index()
    df_products_copy.rename(columns={"Total products": "Total requested"}, inplace=True)


    bar_chart= px.bar(df_products_copy, x="products", y="Total requested", text="Total requested", title="Products requested", template="ggplot2")
    bar_chart.update_layout(title_x=0.5, font=dict(family="Arial", size=12, color="black"))
    bar_chart.update_layout(title_x=0.5, xaxis_title="Products", yaxis_title="Number of requested products", font=dict(family="Arial", size=11, color="black"))
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
    bar_chart.update_layout(title_x=0.5, xaxis_title="Service requested", yaxis_title="Number of requests", font=dict(family="Arial", size=11, color="black"))
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

    df_issues_agency_type_copy = df_issues_agency_type_copy.groupby(['agency_type.choices0'] )["Key"].count().reset_index()
    #print(df_issues_agency_type_copy)
    
    pie_chart = px.pie(names=df_issues_agency_type_copy['agency_type.choices0'], values = df_issues_agency_type_copy["Key"], title="Total type of agency", template="ggplot2")
    pie_chart.update_layout(title_x=0.5, font=dict(family="Arial", size=11, color="black"))
    pie_chart.update_layout(margin=dict(l=10, r=10, t=23, b=20))
    pie_chart.update_legends(dict(orientation="h" , yanchor="bottom",  y=-0.05,   xanchor="right",   x=0.9))
    pie_chart.update_traces(marker_colors=[  "blue", "red"])
    return pie_chart
    

# tbd chart *******************************************************************
@app.callback(
    Output("sector_chart", "figure"),
    Input("date-range-slider", "value")
)

def update_products_chart(date_range):

    # Picking the years from the date slicer
    start_date = dt.fromtimestamp(date_range[0]).year
    end_date = dt.fromtimestamp(date_range[1]).year

    # coping the original dataframes
    df_issues_sectors_copy = df_issues_sectors.copy()
    df_issues_sectors_copy["percentage"] = round(df_issues_sectors_copy["Total sectors"] / requests_number * 100,1)

    # filtering the dataframe using the picked years from the date slicer
    df_issues_sectors_copy = df_issues_sectors_copy[(df_issues_sectors_copy["year"] >= start_date) & (df_issues_sectors_copy["year"] <= end_date)]

    # df_reactions_copy = df_reactions_copy.groupby(["Summary"] )["ID"].count().reset_index()
    df_issues_sectors_copy.rename(columns={"Total sectors": "Total agencies"}, inplace=True)


    bar_chart= px.bar(df_issues_sectors_copy, x="sectors_of_work", y="Total agencies", text="Total agencies", title="Distribution of agency work sectors", template="ggplot2")
    bar_chart.update_layout(title_x=0.5, font=dict(family="Arial", size=12, color="black"))
    bar_chart.update_layout(title_x=0.5, xaxis_title="Sectors", yaxis_title="Number of agency", font=dict(family="Arial", size=11, color="black"))
    bar_chart.update_layout(margin=dict(l=10, r=10, t=23, b=20))
    bar_chart.update_traces(marker_color="blue", marker_line_color="blue", marker_line_width=1.5, opacity=0.6)

    return bar_chart


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