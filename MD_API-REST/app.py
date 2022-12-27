from flask import Flask, jsonify, request
import pandas as pd
import json


from algorithms import Data, EDA_algorithm
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
        eda = EDA_algorithm(data)
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

@app.route("/PCA")
def PCA():
    return jsonify({
        "message":"PCA algorithm"
    })
    
@app.route("/Model/Dtree")
def Dtree():
    return jsonify({
        "message":"Decision tree regressor model"
    })
@app.route("/Model/randomForest")
def randomForest():
    return jsonify({
        "message":"Random Forest Regressor model"
    })

@app.route("/Model/hybrid")
def hybrid():
    return jsonify({
        "message":"hybrid model (Kmeans + random forest)"
    })
    
@app.route("/Model/SVM/<string:kernel>")
def svm(kernel):
    return jsonify({
        "message":f"Support vector machine model with kernel = {kernel}"
    })





if __name__ == "__main__":
    app.run(debug=True, port=8080)