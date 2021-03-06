"""
Test
"""

import time
import datetime
import predict
import colors
import config
import pandas as pd
import numpy as np

prediction_csv_path = config.settings["prediction_csv_path"]
reality_csv_path = config.settings["reality_csv_path"]
customer = config.settings["customer"]

"""
Compare predicted orders to actual order data
"""
def test_prediction():
    print colors.line("header", "--- Testing ---")
    start_test_time = time.time()
    prediction = predict.predict_order_date_of_items_for_customer(
        customer,
        prediction_csv_path,
        datetime.datetime.now())
    print colors.line("header", "--- Comparing predictions to reality... ---")
    data_frame = pd.read_csv(reality_csv_path, parse_dates=["date"], index_col="order")
    customer_data = data_frame.loc[
        (data_frame.customer == customer), ["date", "quantity", "materialId"]]
    items = customer_data["materialId"].unique()
    test_results = []
    successes = []
    warnings = []
    failures = []

    # compare actual ordering dates against predictions
    for material_id in items:
        orders_with_items = data_frame.loc[
            ((data_frame.materialId == material_id) & (data_frame.customer == customer)),
            ["date", "quantity"]]
        sorted_item_orders = orders_with_items.sort_values("date")
        reality_date = sorted_item_orders.head(1)["date"].values[0]

        if material_id in prediction:
            predicted_item = prediction[material_id]

            if "predicted_next_order_date" in predicted_item:
                prediction_delta = np.timedelta64(predicted_item["predicted_next_order_date"] - reality_date, "D")
                success = (prediction_delta < np.timedelta64(1, "D")) and (prediction_delta > np.timedelta64(-1, "D"))
                warning = (prediction_delta < np.timedelta64(3, "D")) and (prediction_delta > np.timedelta64(-3, "D"))

                # TODO: Clean this up
                if success:
                    successes.append(material_id)
                elif warning:
                    warnings.append(material_id)
                else:
                    failures.append(material_id)

                test_results.append({
                    "material_id": material_id,
                    "confidence": str(predicted_item["confidence"]),
                    "predicted_date": str(predicted_item["predicted_next_order_date"]),
                    "reality_date": str(reality_date),
                    "prediction_delta": str(prediction_delta),
                    "success": success
                })

            # else:
                # print "Not ordering enough data to predict this item"

        # else:
            # print "This item was not in previous orders"

    # See how well it did
    success_percentage = 100 * (float(len(successes)) / float(len(test_results)))
    warning_percentage = 100 * (float(len(warnings)) / float(len(test_results)))
    failure_percentage = 100 * (float(len(failures)) / float(len(test_results)))

    # Put together final results
    overall_results = {
        "customer": customer,
        "items_tested": len(test_results),
        "success_percentage": "%.2f" % success_percentage,
        "warning_percentage": "%.2f" % warning_percentage,
        "failure_percentage": "%.2f" % failure_percentage
    }

    print colors.line("okgreen", "--- Success percentage (within 1 day)    : " + str("%.2f" % success_percentage))
    print colors.line("warning", "--- Warning percentage (within 3 days)   : " + str("%.2f" % warning_percentage))
    print colors.line("fail", "--- Failure percentage (everything else) : " + str("%.2f" % failure_percentage))

    # Create dataframes of the results
    item_results_data_frame = pd.DataFrame(test_results, columns=["material_id", "confidence", "predicted_date", "reality_date", "prediction_delta", "success"])
    overall_results_data_frame = pd.DataFrame([overall_results], columns=["customer", "items_tested", "success_percentage", "warning_percentage", "failure_percentage"])

    # Do excel stuff
    excel_output_file_name = "test-results.xlsx"
    writer = pd.ExcelWriter(excel_output_file_name, engine="xlsxwriter")
    item_results_data_frame.to_excel(writer, sheet_name="Item Test Results")
    overall_results_data_frame.to_excel(writer, sheet_name="Overall Results")
    writer.save()

    print colors.line(
        "okgreen",
        "--- Test results written to : " + excel_output_file_name + " in " + str(time.time() - start_test_time)
    )

    return test_results


test_prediction()
