import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

# Define categorical mappings
age_groups = ['18-25', '26-35', '36-50', '51+']
family_backgrounds = ['Single', 'Married', 'Married with Kids']

# Generate synthetic dataset
def generate_dataset(rows=10000):
    data = []
    
    for _ in range(rows):
        # Generate basic demographics
        phone_number = f"+91-{random.randint(9000000000, 9999999999)}"
        email = fake.email()
        
        # Generate credit score (300-850)
        credit_score = random.randint(300, 850)
        
        # Generate age group
        age_group = random.choice(age_groups)
        
        # Generate family background
        family_background = random.choice(family_backgrounds)
        
        # Generate income (100000-1000000 INR)
        income = random.randint(100000, 1000000)
        
        # Generate comments
        keywords = [
            "urgent", "now", "immediately", "interested",
            "not interested", "later", "maybe", "soon"
        ]
        
        # Create comments with random keywords
        comments = " ".join(random.sample(keywords, random.randint(1, 3)))
        
        # Generate target variable (0 or 1)
        # Higher probability of high intent for higher credit scores, income, etc.
        intent_probability = (
            (credit_score - 300) / 550 * 0.4 +  # Credit score impact
            (income - 100000) / 900000 * 0.3 +   # Income impact
            random.random() * 0.3                # Random noise
        )
        
        intent = 1 if random.random() < intent_probability else 0
        
        data.append({
            "phone_number": phone_number,
            "email": email,
            "credit_score": credit_score,
            "age_group": age_group,
            "family_background": family_background,
            "income": income,
            "comments": comments,
            "intent": intent
        })
    
    return pd.DataFrame(data)

# Generate and save dataset
df = generate_dataset()
df.to_csv("leads_dataset.csv", index=False)
print(f"Generated dataset with {len(df)} rows")
