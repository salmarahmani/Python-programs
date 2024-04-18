"""
This Python function, calculate_discounted_price, calculates the discounted prices for various items and item combos in an online store. It takes a list of item prices as input and applies discounts based on predefined discount rates for combo purchases and gift packs. The function then prints the catalog of products along with their discounted prices, including individual items and different combinations. Finally, it displays a contact number for delivery inquiries.
"""

def calculate_discounted_price(item_prices):
    combo_discount = 0.1
    gift_pack_discount = 0.25
    catalog = {
    "Item 1": item_prices[0],
    "Item 2": item_prices[1],
    "Item 3": item_prices[2],
    "Combo 1 (Item 1 + 2)": item_prices[0] + item_prices[1] - (item_prices[0] + item_prices[1]) * combo_discount,
    "Combo 2 (Item 2 + 3)": item_prices[1] + item_prices[2] - (item_prices[1] + item_prices[2]) * combo_discount,
    "Combo 3 (Item 1 + 3)": item_prices[0] + item_prices[2] - (item_prices[0] + item_prices[2]) * combo_discount,
    "Combo 4 (Item 1 + 2 + 3)": sum(item_prices) - sum(item_prices) * gift_pack_discount, }

    print("Online Store\n")
    print("---------------") 
    print("Product(S) \t Price")
    for product, price in catalog.items():
     print(f"{product} \t {price:.1f}")
    print("\n") 
    print("_________________________")
    print("For delivery Contact: 98764678899")
item_prices = [200.0, 400.0, 600.0]
calculate_discounted_price(item_prices) 
