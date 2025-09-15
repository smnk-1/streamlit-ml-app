import pandas as pd
from shapely.geometry import Point, Polygon
from geopy.distance import geodesic
import category_encoders as ce

def preprocess(data):
    data.drop_duplicates(inplace=True)
    for column in data.columns:
        if column not in ['id', 'vendor_id', 'pickup_datetime', 'dropoff_datetime']:
            lower_bound = data[column].quantile(0.01)
            upper_bound = data[column].quantile(0.99)

            data = data[data[column] >= lower_bound]
            data = data[data[column] <= upper_bound]
    data.drop(columns=['dropoff_datetime'], inplace=True)

    print(2)

    nyc_center_polygon =  Polygon([
        (-73.955539, 40.829344),
        (-74.011861, 40.752701),
        (-74.01954326467963, 40.71452872820932),
        (-74.0153570038084, 40.69996899434237),
        (-73.9774198401262, 40.71129042453187),
        (-73.9717550144014, 40.72885435095875),
        (-73.94296996632072, 40.7761792515498),
        (-73.92970080603428, 40.801063436793875)
    ])
    data['pickup_point'] = data.apply(lambda row: Point(row['pickup_longitude'], row['pickup_latitude']), axis=1)
    data['dropoff_point'] = data.apply(lambda row: Point(row['dropoff_longitude'], row['dropoff_latitude']), axis=1)

    data['pickup_in_zone'] = data['pickup_point'].apply(lambda p: nyc_center_polygon.contains(p))
    data['dropoff_in_zone'] = data['dropoff_point'].apply(lambda p: nyc_center_polygon.contains(p))

    data['in_nyc_center?'] = data.apply(lambda row: 1 if row['pickup_in_zone'] or row['dropoff_in_zone'] else 0, axis=1)

    data.drop(columns=['pickup_point', 'dropoff_point', 'pickup_in_zone', 'dropoff_in_zone'], inplace=True)
    data['distance'] = data.apply(
    lambda row: geodesic((row['pickup_latitude'], row['pickup_longitude']),
                          (row['dropoff_latitude'], row['dropoff_longitude'])).meters, axis=1
    )
    
    data['hour'] = pd.to_datetime(data['pickup_datetime']).dt.hour
    data['is_it_weekday?'] = pd.to_datetime(data['pickup_datetime']).dt.dayofweek < 5
    data['is_it_weekday?'] = data['is_it_weekday?'].astype(int)
    

    encoder = ce.OneHotEncoder(cols=['hour'])
    data = encoder.fit_transform(data)

    data['is_it_first_vendor?(else 2nd)'] = data.apply(lambda row: 1 if row['vendor_id'] == 1.0 else 0, axis=1)
    data.drop(columns=['vendor_id', 'pickup_datetime'], inplace=True) 

    for h in range(1, 25):
        data[f'hour_{h}']=0

    try:
        data.drop(columns = ['id', 'trip_duration'], inplace=True)
    except:
        pass
    
    new_order = [
    'passenger_count',
    'pickup_longitude',
    'pickup_latitude',
    'dropoff_longitude',
    'dropoff_latitude',
    'in_nyc_center?',
    'distance',
    'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9', 'hour_10',
    'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_20',
    'hour_21', 'hour_22', 'hour_23', 'hour_24',
    'is_it_weekday?',
    'is_it_first_vendor?(else 2nd)'
]

    data = data[new_order]

    return data
