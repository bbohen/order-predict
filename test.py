# Pump data into predict, get output

# Compare output to the next ordered date of each item in the filtered NEXT PERIOD data

import os
import datetime
import predict
import pandas as pd

prediction_csv_path = os.environ["PREDICTION_CSV_PATH"]
reality_csv_path = os.environ["REALITY_CSV_PATH"]
customer = os.environ["CUSTOMER"]

def test_prediction():
    print "Testing!"
    prediction = predict.predict_order_date_of_items_for_customer(
        customer,
        prediction_csv_path,
        datetime.datetime.now())
    # reality = {}
    print "--- Comparing to reality... ---"
    data_frame = pd.read_csv(reality_csv_path, parse_dates=["date"], index_col="order")
    customer_data = data_frame.loc[
        (data_frame.customer == customer), ["date", "quantity", "materialId"]]
    items = customer_data["materialId"].unique()

    print len(items)

    for material_id in items:
        orders_with_items = data_frame.loc[
            ((data_frame.materialId == material_id) & (data_frame.customer == customer)),
            ["date", "quantity"]]
        sorted_item_orders = orders_with_items.sort_values("date")
        reality_date = sorted_item_orders.head(1)["date"].values[0]

        if material_id in prediction:
            predicted_item = prediction[material_id]

        print "------------------- Testing"
        print "Material ID: " + str(material_id)

        if material_id in prediction:
            print "Predicted Date: " + str(predicted_item["next_order_date"])
            print "Confidence Level: " + str(predicted_item["confidence"])
            print "Reality Date: " + str(reality_date)
        else:
            print "This item was not in previous orders"

test_prediction()