def calculate_average(scores):
    return sum(scores) / len(scores)

def get_grade(avg):
    if avg >= 90: return "A"
    elif avg >= 80: return "B"
    elif avg >= 70: return "C"
    else: return "F"

def get_topper_name(students):
    return max(students, key=lambda s: calculate_average(s['scores']))['name']

students = [
    {"name": "Alice", "scores": [85, 92, 88], "subject": "Math"},
    {"name": "Bob", "scores": [70, 65, 72], "subject": "Math"},
    {"name": "Charlie", "scores": [95, 98, 92], "subject": "Math"},
    {"name": "David", "scores": [82, 79, 81], "subject": "Math"},
    {"name": "Eve", "scores": [60, 55, 58], "subject": "Math"}
]

topper_name = get_topper_name(students)

sorted_students = sorted(students, key=lambda s: calculate_average(s['scores']), reverse=True)

print(f"{'STUDENT':<10} | {'AVG':<6} | {'GRADE':<6}")
print("-" * 30)

for s in sorted_students:
    avg = calculate_average(s['scores'])
    grade = get_grade(avg)
    
    row = f"{s['name']:<10} | {avg:<6.1f} | {grade:<6}"
    
    if s['name'] == topper_name:
        print(f"{row} *** TOP ***")
    else:
        print(row)