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

app.layout = html.Div([html.H1("🎬 Movie Analytics Dashboard",
            style={
                "textAlign":"center"
            }),
                       html.Hr(),
                       html.Label("🎭 Select Movie Genre:"),
                       dcc.Dropdown(id="genre_dropdown",
                                    options=[
                                        {
                                        "label":genre,
                                        "value":genre
                                        }
                                    for genre in movies["genre"].unique()],
                                    value=movies["genre"].unique()[0],
                                    clearable=False),

        html.Br(),
        dcc.Graph(id="score_graph")])
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

# =====================================================
# ▶️ RUN DASH SERVER
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)   
