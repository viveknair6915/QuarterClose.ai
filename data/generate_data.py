import pandas as pd
import numpy as np
import random
from datetime import date, timedelta
import os

def generate_claims_data(rows=1000):
    segments = ['Property', 'Casualty', 'Marine', 'Aviation', 'Life']
    products = ['QuotaShare', 'ExcessOfLoss', 'StopLoss']
    
    data = []
    
    for i in range(rows):
        claim_id = f"CLM-{2024}-{i:05d}"
        policy_id = f"POL-{random.randint(1000, 9999)}"
        segment = random.choice(segments)
        product = random.choice(products)
        
        # Loss Dates
        start_date = date(2024, 1, 1)
        end_date = date(2024, 12, 31)
        days = (end_date - start_date).days
        dol = start_date + timedelta(days=random.randint(0, days))
        report_date = dol + timedelta(days=random.randint(1, 90))
        
        # Amounts
        incurred = round(random.lognormvariate(10, 2), 2) # Log-normal distribution for claims
        paid = round(random.uniform(0, incurred), 2)
        outstanding = incurred - paid
        
        status = 'Open' if outstanding > 0 else 'Closed'
        
        # Location (Synthetic Lat/Lon for major hubs: NY, London, Tokyo, Bermuda)
        hubs = [
            (40.7128, -74.0060), # NYC
            (51.5074, -0.1278),  # London
            (35.6762, 139.6503), # Tokyo
            (32.3078, -64.7505), # Bermuda
            (1.3521, 103.8198),  # Singapore
            (48.8566, 2.3522),   # Paris
        ]
        base_loc = random.choice(hubs)
        # Add some jitter
        lat = base_loc[0] + random.uniform(-2, 2)
        lon = base_loc[1] + random.uniform(-2, 2)

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
            'period_month': dol.month, # Approx attribution
            'latitude': lat,
            'longitude': lon
        })
        
    df = pd.DataFrame(data)
    
    # Inject some Data Quality Issues
    # 1. Negative Incurred
    df.loc[0, 'incurred_amount'] = -5000
    
    # 2. Missing Segment
    df.loc[1, 'segment'] = None
    
    return df

if __name__ == "__main__":
    output_dir = "data/sample_inputs"
    os.makedirs(output_dir, exist_ok=True)
    
    df = generate_claims_data(500)
    output_path = f"{output_dir}/sample_claims_2024.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {output_path}")
