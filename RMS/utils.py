import matplotlib.pyplot as plt
import base64
from io import BytesIO

def getGraph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def getPlot(x,y,plotDate):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,4))
    plotDate = '/'.join(plotDate.split('-')[::-1])
    plt.title('Sales v/s Hour Graph for '+plotDate)
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('Hours in a day')
    plt.ylabel('Sales Conducted')
    plt.tight_layout()
    graph=getGraph()
    return graph