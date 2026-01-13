import pandas as pd
import numpy as np
import random
from datetime import date, timedelta
import os

def generate_dataset(filename, rows=500, error_rate=0.0, heavy_loss_prob=0.01):
    segments = ['Property', 'Casualty', 'Marine', 'Aviation', 'Life']
    products = ['QuotaShare', 'ExcessOfLoss', 'StopLoss']
    
    data = []
    
    for i in range(rows):
        claim_id = f"CLM-{2024}-{i:05d}"
        policy_id = f"POL-{random.randint(1000, 9999)}"
        segment = random.choice(segments)
        product = random.choice(products)
        
        dol = date(2024, 1, 1) + timedelta(days=random.randint(0, 364))
        report_date = dol + timedelta(days=random.randint(1, 90))
        
        # Heavy Tail Logic
        if random.random() < heavy_loss_prob:
             incurred = round(random.uniform(150000, 5000000), 2) # Large Loss
        else:
             incurred = round(random.lognormvariate(9, 1.5), 2) # Normalish
             
        paid = round(random.uniform(0, incurred), 2)
        outstanding = incurred - paid
        status = 'Open' if outstanding > 0 else 'Closed'
        
        # Errors
        if random.random() < error_rate:
            if random.random() < 0.5:
                incurred = -abs(incurred) # Negative Incurred
            else:
                segment = None # Missing Segment

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
            'period_month': dol.month
        })
        
    df = pd.DataFrame(data)
    path = f"data/sample_inputs/{filename}"
    df.to_csv(path, index=False)
    print(f"Created {path}")

if __name__ == "__main__":
    os.makedirs("data/sample_inputs", exist_ok=True)
    generate_dataset("dataset_1_standard.csv", rows=500, error_rate=0.02, heavy_loss_prob=0.01)
    generate_dataset("dataset_2_clean_perfect.csv", rows=500, error_rate=0.0, heavy_loss_prob=0.01)
    generate_dataset("dataset_3_shock_losses.csv", rows=200, error_rate=0.01, heavy_loss_prob=0.10) # 10% large losses
