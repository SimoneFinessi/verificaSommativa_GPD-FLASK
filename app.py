from flask import Flask, render_template, request, Response
import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.geometry import Point,Polygon
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
df=pd.read_csv("https://raw.githubusercontent.com/SimoneFinessi/Dati/main/istat2022/sosta_turistici%20(2).csv",delimiter=";")
latitudine = df['LAT_Y_4326']
longitudine = df['LONG_X_4326']
geometry = [Point(xy) for xy in zip(longitudine,latitudine)]
geodf = gpd.GeoDataFrame(df, crs=4326, geometry=geometry)
quar=gpd.read_file("https://github.com/SimoneFinessi/Dati/raw/main/istat2022/ds964_nil_wm%20(2).zip")

app = Flask(__name__)

@app.route('/')
def home():
    cont=quar[quar.intersects(geodf.unary_union)]
    trovato=cont["NIL"].to_list()
    return render_template("home.html",list=trovato)

@app.route('/es1', methods=["post"])
def es1():
    sel=request.form["sel"]
    return render_template("ris.html",sel=sel)
@app.route('/img1', methods=["GET"])
def img1():
    loca=request.args["sel"]
    controllo=geodf[geodf.localizzaz.str.contains(loca)]

    trovato=quar[quar.intersects(controllo.geometry.item())]
    print(trovato[["NIL"]])
    fig,ax=plt.subplots()
    controllo.to_crs(3857).plot(color="Red",ax=ax)
    trovato.to_crs(3857).plot(facecolor="none",edgecolor="Black",ax=ax)
    ctx.add_basemap(ax=ax)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
if __name__ == '__main__':
    app.run(debug=True)