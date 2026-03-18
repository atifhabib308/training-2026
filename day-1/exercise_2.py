def grade_classifier(score):
    if score >= 90:
        return 'Distinction'
    elif score >= 60:
        return 'Pass'
    else:
        return 'Fail'

test_values = [95, 89, 60, 59, 0]
for val in test_values:
    print(f"Score {val}: {grade_classifier(val)}")

print("-" * 20)

scores = [45, 72, 91, 60, 38, 85]
for s in scores:
    result = grade_classifier(s)
    print(f"Score: {s} | Result: {result}")