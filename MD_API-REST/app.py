from flask import Flask, jsonify, request
import pandas as pd
import json


from algorithms import Data, EDA
app = Flask(__name__) # our app


# routes
@app.route('/getData',methods = ['POST'])
def getData():
    dataInfoTicker = request.json
    global data
    data = Data(
        ticker = dataInfoTicker["ticker"],
        name = dataInfoTicker["name"],
        date_start = dataInfoTicker["date_start"],
        date_end = dataInfoTicker["date_end"]
    )
    print(data.getDataInformation())
    return jsonify({
        "message":"Ticker found" if data.data else "Ticker not found",
        "Data" : data.getDataInformation() if data.data else None,
    })

@app.route("/")
def ping():
    return jsonify({"message":"API MD Connection succesfully"})

    
@app.route("/EDA")
def eda():
    if data.data:
        eda = EDA(data)
        step1 = eda.getDescriptionOfData()
        step2 = eda.getMissingData()
        step3 = {
            "histograms_status": eda.create_histograms(),
            "data_statistics" : eda.data_statistics().to_dict(),
            "graphic_status" : eda.create_DataTickerGraphic()
        }
        step4 = {
            "correlations": eda.getCorrelations().to_dict(),
            "heatmap_status": eda.getHeatMap()
        }
        return jsonify({
            "EDA":{
                "step1": step1,
                "step2": step2,
                "step3": step3,
                "step4": step4
                }
            })
    
    return jsonify({
        "message" : "Error, there is no data"
    })
    


if __name__ == "__main__":
    app.run(debug=True, port=8080)