# =====================================================
# 🚀 IMPORT REQUIRED LIBRARIES
# =====================================================

import pandas as pd
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px


# =====================================================
# 📂 LOAD MOVIE DATASET
# =====================================================

movies = pd.read_csv("data/movies.csv")

print(movies.columns)

# Remove missing values
movies = movies.dropna()


# =====================================================
# 🌐 CREATE DASH APP
# =====================================================

app = Dash(__name__)

app.title = "🎬 Movie Analytics Dashboard"


# =====================================================
# 🎨 DASHBOARD LAYOUT
# =====================================================

app.layout = html.Div(

    className="container",

    children=[

        html.H1(
            "🎬 Movie Analytics Dashboard",
            className="title"
        ),


        # ==========================
        # KPI CARDS
        # ==========================

        html.Div([

            html.Div([
                html.H3("🎞 Total Movies"),
                html.H2(id="total-movies")
            ], className="card"),


            html.Div([
                html.H3("⭐ Average Score"),
                html.H2(id="average-score")
            ], className="card"),


            html.Div([
                html.H3("🏆 Highest Score"),
                html.H2(id="highest-score")
            ], className="card")


        ], className="cards"),



        html.Hr(),



        # ==========================
        # SEARCH MOVIE
        # ==========================

        html.H3("🔎 Search Movie"),

        dcc.Input(

            id="movie-search",

            type="text",

            placeholder="Enter movie name...",

            className="search"

        ),



        html.Br(),
        html.Br(),



        # ==========================
        # GENRE FILTER
        # ==========================

        html.H3("🎭 Select Genre"),


        dcc.Dropdown(

            id="genre-dropdown",

            options=[
                {
                    "label": genre,
                    "value": genre
                }

                for genre in movies["genre"].unique()

            ],

            value=movies["genre"].iloc[0],

            className="dropdown"

        ),



        html.Br(),



        # ==========================
        # GRAPH 1
        # ==========================

        dcc.Graph(
            id="rating-chart"
        ),



        # ==========================
        # GRAPH 2 YEAR ANALYSIS
        # ==========================

        dcc.Graph(
            id="year-chart"
        ),



        # ==========================
        # TOP 10 MOVIES TABLE
        # ==========================


        html.H2(
            "🏆 Top 10 Movies"
        ),


        dash_table.DataTable(

            id="movie-table",

            style_table={
                "overflowX":"auto"
            },

            style_cell={
                "textAlign":"center"
            }

        )

    ]
)



# =====================================================
# 📊 UPDATE CARDS
# =====================================================

@app.callback(

    Output("total-movies","children"),

    Output("average-score","children"),

    Output("highest-score","children"),

    Input("movie-search","value")

)

def update_cards(search):


    df = movies


    if search:

        df = df[
            df["title"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    return (

        len(df),

        round(df["score"].mean(),2)
        if len(df)>0 else 0,

        df["score"].max()
        if len(df)>0 else 0

    )



# =====================================================
# 📈 UPDATE GRAPHS AND TABLE
# =====================================================

@app.callback(

    Output("rating-chart","figure"),

    Output("year-chart","figure"),

    Output("movie-table","data"),

    Output("movie-table","columns"),

    Input("genre-dropdown","value"),

    Input("movie-search","value")

)


def update_dashboard(
        genre,
        search
):


    df = movies.copy()



    if genre:

        df = df[
            df["genre"]==genre
        ]



    if search:

        df=df[
            df["title"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]



    # Rating graph

    rating_data=(

        df.groupby("rating")
        ["score"]
        .mean()
        .reset_index()

    )


    fig1=px.bar(

        rating_data,

        x="rating",

        y="score",

        color="score",

        title="⭐ Average Score by Rating"

    )



    # Year graph


    year_data=(

        df["year"]
        .value_counts()
        .sort_index()
        .reset_index()

    )


    year_data.columns=[
        "year",
        "movies"
    ]


    fig2=px.line(

        year_data,

        x="year",

        y="movies",

        markers=True,

        title="🎬 Movies Released Per Year"

    )



    # Top 10 table


    top10=(

        df.sort_values(

            by="score",

            ascending=False

        )

        .head(10)

    )


    columns=[

        {
            "name":col,
            "id":col

        }

        for col in top10.columns

    ]



    return (

        fig1,

        fig2,

        top10.to_dict("records"),

        columns

    )




# =====================================================
# ▶️ RUN APP
# =====================================================

if __name__=="__main__":

    app.run(debug=True)