# =====================================================
# 🚀 IMPORT REQUIRED LIBRARIES
# =====================================================
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
# =====================================================
# 📂 LOAD MOVIE DATASET
# =====================================================
movies = pd.read_csv("data/movies.csv")
print(movies.columns)
# =====================================================
# 🌐 CREATE DASH APP
# =====================================================
app = Dash(__name__)
app.title = "🎬 Movie Analytics Dashboard"
# =====================================================
# 🎨 DASHBOARD LAYOUT
# =====================================================

app.layout = html.Div([

    html.H1(
        "🎬 Movie Analytics Dashboard",
        style={
            "textAlign": "center"
        }
    ),

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


    html.Br(),

    html.Label("🎭 Select Movie Genre:"),

    dcc.Dropdown(
        id="genre-dropdown",
        options=[
            {
                "label": g,
                "value": g
            }
            for g in movies["genre"].unique()
        ],
        value=movies["genre"].iloc[0]
    ),


    dcc.Graph(
        id="rating-chart"
    )

])
# =====================================================
# 🔄 UPDATE GRAPH USING DROPDOWN
# =====================================================
@app.callback(
    Output("score_graph","figure"),
    Input("genre_dropdown","value"))
def update_graph(selected_genre):
    filtered_data = movies[movies["genre"] == selected_genre]
    score_data = (filtered_data.groupby("rating")["score"].mean().reset_index())
    fig = px.bar(score_data,x="rating",y="score",color="score",
                 title=f"⭐ Average Score by Rating - {selected_genre}")
    fig.update_layout(xaxis_title="Movie Rating",
                      yaxis_title="Average Score",
                      template="plotly_white")
    return fig

#
# =====================================================
# 📊 UPDATE DASHBOARD CARDS
# =====================================================

@app.callback(
    Output("total-movies", "children"),
    Output("average-score", "children"),
    Output("highest-score", "children"),
)
def update_cards():

    total_movies = len(movies)

    average_score = round(
        movies["score"].mean(),
        2
    )

    highest_score = movies["score"].max()

    return (
        total_movies,
        average_score,
        highest_score
    )

@app.callback(
    Output("rating-chart", "figure"),
    Input("genre-dropdown", "value")
)
def update_graph(selected_genre):

    filtered_data = movies[
        movies["genre"] == selected_genre
    ]

    score_data = (
        filtered_data
        .groupby("rating")["score"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        score_data,
        x="rating",
        y="score",
        color="score",
        title=f"⭐ Average Score by Rating - {selected_genre}"
    )

    fig.update_layout(
        xaxis_title="Movie Rating",
        yaxis_title="Average Score",
        template="plotly_white"
    )

    return fig

# =====================================================
# ▶️ RUN DASH SERVER
# =====================================================

    return fig  
if __name__ == "__main__":
    app.run(debug=True)     