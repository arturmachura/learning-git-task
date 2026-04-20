shopping = {
    "biedronka": ["mleko", "chleb", "masło"],
    "lidl": ["jabłka", "jogurt"],
    "apteka": ["witaminy", "plaster"]
}

for store, products in shopping.items():
    print(f"Idę do {store.upper()} i kupuję tam {', '.join(products).upper()}.")

total_products = sum(len(products) for products in shopping.values())
print(f"W sumie kupuję {total_products} produktów.")

# commit_2