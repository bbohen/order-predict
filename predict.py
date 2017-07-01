import os
import time
import datetime
import pandas as pd
import numpy as np

start_time = time.time()
csv_path_from_env = os.environ["CSVPATH"]
customer_from_env = os.environ["CUSTOMER"]

def predict_order_date_of_items_for_customer(customer, csv_path, desired_date_time):
    print "Analyzing order data "
    print "Customer is " + customer

    # parse csv data
    data_frame = pd.read_csv(csv_path, parse_dates=["date"], index_col="order")
    # filter to customer, get relevant data
    customer_data = data_frame.loc[
        (data_frame.customer == customer), ["date", "quantity", "materialId"]]
    total_customer_orders = customer_data.index.unique().values
    items = customer_data["materialId"].unique()
    desired_date_time_64 = np.datetime64(desired_date_time)

    print "---------------------------"
    print "Customer has " + str(len(total_customer_orders)) + " orders with " + str(len(items)) + " items"
    print "---------------------------"

    # run calculations on every item ordered by the customer
    # is there a way to do this without the for loop? a method of dataframe maybe?
    for material_id in items:
        orders_with_items = data_frame.loc[
            ((data_frame.materialId == material_id) & (data_frame.customer == customer)),
            ["date", "quantity"]]

        item_ordered_average = 100 * (
            float(len(orders_with_items.index)) / float(len(total_customer_orders)))

        if item_ordered_average > 10:
            sorted_item_orders = orders_with_items.sort_values('date')
            sorted_item_orders_diff = sorted_item_orders["date"].diff()
            days_between_orders = sorted_item_orders_diff[
                sorted_item_orders_diff != np.timedelta64(0, 'D')]
            average_days_between_orders = days_between_orders.mean()
            last_ordered_date = sorted_item_orders.tail(1)["date"].values[0]
            next_order_date = last_ordered_date + average_days_between_orders
            time_until_next_order = next_order_date - desired_date_time_64

            print "Material ID: " + str(material_id)
            print "Confidence: " + str(item_ordered_average)
            print "Last Order: " + str(last_ordered_date)
            print "Next Order: " + str(next_order_date)
            print "Time Until Next Order: " + str(time_until_next_order)
            print "---------------------------"

    print "--- Report generated in %s seconds ---" % (time.time() - start_time)

predict_order_date_of_items_for_customer(customer_from_env, csv_path_from_env, datetime.datetime.now())
