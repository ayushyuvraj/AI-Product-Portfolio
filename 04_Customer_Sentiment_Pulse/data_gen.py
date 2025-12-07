import pandas as pd
import random

reviews = [
    # Positive
    "The app is super fast, love the new UI!",
    "Great experience with the loan disbursement process.",
    "Customer support was very helpful in resolving my KYC issue.",
    "Best banking app in India, hands down.",
    "I love the wealth nudge feature, very useful.",
    
    # Neutral
    "It's okay, but the server is down sometimes.",
    "Update takes too long to download.",
    "The colors are a bit too bright, but functionality is fine.",
    "Decent app, does the job.",
    
    # Negative
    "Absolute trash. Transaction failed 3 times!",
    "Why is there so much hidden fees? Uninstalled.",
    "Worst support ever. No one replies.",
    "My money got stuck for 2 days. Scary experience.",
    "Too many bugs after the last update. Fix it!"
]

data = []
for i in range(50):
    review = random.choice(reviews)
    data.append([i, review])

df = pd.DataFrame(data, columns=["ID", "Review"])
df.to_csv("reviews.csv", index=False)
print("✅ Created 'reviews.csv' with dummy data.")