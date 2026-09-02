import pandas as pd

from scraper.visualizer import show_all_visualizations


products = [
    {
        "name": "Laptop",
        "price": 85000,
        "rating": 4.5,
        "category": "Electronics"
    },
    {
        "name": "Phone",
        "price": 50000,
        "rating": 4.2,
        "category": "Electronics"
    },
    {
        "name": "Headphones",
        "price": 5000,
        "rating": 4.0,
        "category": "Accessories"
    },
    {
        "name": "Keyboard",
        "price": 3000,
        "rating": 4.5,
        "category": "Accessories"
    },
    {
        "name": "Monitor",
        "price": 30000,
        "rating": 4.8,
        "category": "Electronics"
    }
]


df = pd.DataFrame(products)


show_all_visualizations(df)