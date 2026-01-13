import pandas as pd
import numpy as np
import random
from datetime import date, timedelta
import os

def generate_geo_dataset(filename, rows=800):
    segments = ['Property', 'Casualty', 'Marine', 'Aviation', 'Energy']
    products = ['QuotaShare', 'ExcessOfLoss', 'StopLoss']
    
    # Major Insurance Hubs with approx Lat/Lon
    # We will cluster claims around these points to make the map look realistic
    hubs = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060},
        {"name": "London", "lat": 51.5074, "lon": -0.1278},
        {"name": "Bermuda", "lat": 32.3078, "lon": -64.7505},
        {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
        {"name": "Singapore", "lat": 1.3521, "lon": 103.8198},
        {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
        {"name": "Zurich", "lat": 47.3769, "lon": 8.5417},
        {"name": "Munich", "lat": 48.1351, "lon": 11.5820},
        {"name": "Florida (Hurricane)", "lat": 27.6648, "lon": -81.5158},
        {"name": "California (Quake)", "lat": 36.7783, "lon": -119.4179}
    ]
    
    data = []
    
    for i in range(rows):
        claim_id = f"CLM-{2024}-{i:05d}"
        policy_id = f"POL-{random.randint(1000, 9999)}"
        segment = random.choice(segments)
        product = random.choice(products)
        
        # Pick a hub
        hub = random.choice(hubs)
        
        # Add jitter to spread points out slightly (gaussian distribution around hub)
        lat = hub["lat"] + random.gauss(0, 2.0)
        lon = hub["lon"] + random.gauss(0, 2.0)
        
        dol = date(2024, 1, 1) + timedelta(days=random.randint(0, 364))
        report_date = dol + timedelta(days=random.randint(1, 90))
        
        incurred = round(random.lognormvariate(10, 1.5), 2)
        paid = round(random.uniform(0, incurred), 2)
        outstanding = incurred - paid
        status = 'Open' if outstanding > 0 else 'Closed'

        data.append({
            'claim_id': claim_id,
            'policy_id': policy_id,
            'date_of_loss': dol,
            'report_date': report_date,
            'segment': segment,
            'product_line': product,
            'incurred_amount': incurred,
            'paid_amount': paid,
            'outstanding_amount': outstanding,
            'status': status,
            'period_month': dol.month,
            'latitude': lat,
            'longitude': lon,
            'location_name': hub["name"] # For reference
        })
        
    df = pd.DataFrame(data)
    
    path = f"data/sample_inputs/{filename}"
    df.to_csv(path, index=False)
    print(f"Created {path}")

if __name__ == "__main__":
    os.makedirs("data/sample_inputs", exist_ok=True)
    generate_geo_dataset("dataset_4_geospatial_live.csv")
