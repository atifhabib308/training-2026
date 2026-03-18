import string

def word_frequency(text):
    clean_text = text.translate(str.maketrans('', '', string.punctuation))
    words = clean_text.lower().split()
    
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts

paragraph = """
Python is an amazing programming language. Python is versatile, powerful, and 
widely used in data science, web development, and AI. Many developers love 
Python because Python has a clean syntax and a massive community. The community 
is helpful, and the syntax is easy to learn!
"""

freq_dict = word_frequency(paragraph)

sorted_words = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)

print("--- Top 5 Most Common Words ---")
for word, count in sorted_words[:5]:
    print(f"'{word}': {count} times")