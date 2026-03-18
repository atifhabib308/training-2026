while True:
    user_input = int(input("Enter a number (1-12): "))
    if 1 <= user_input <= 12:
        break
    print("Invalid input. Please try again.")

print(f"\n--- Multiplication Table for {user_input} ---")
for i in range(1, 11):
    result = user_input * i
    print(f"{user_input: >2} x {i: >2} = {result: >3}")

print("\n" + "="*40)
print("BONUS: ALL TABLES (1-12)")
print("="*40)

for row in range(1, 13):
    line = ""
    for col in range(1, 13):
        line += f"{row * col: >4}"
    print(line)