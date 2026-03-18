name = "Atif Habib"
age = 27
drinks_coffee = True
salary = 85000.50

coffee_status = "do"
print(f"My name is {name}. I am {age} years old, I {coffee_status} drink coffee, and my monthly salary is Rs. {salary:,.2f}.")

retirement_age = 60
years_to_retirement = retirement_age - age

cups_per_day = 3
price_per_cup = 150
days_in_week = 7
weekly_coffee_budget = cups_per_day * price_per_cup * days_in_week

# Results Output
print(f"\n--- Financial & Life Stats ---")
print(f"Years until retirement: {years_to_retirement}")
print(f"Weekly coffee budget: Rs. {weekly_coffee_budget}")