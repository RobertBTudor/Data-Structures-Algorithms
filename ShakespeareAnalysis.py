#Shakespeare word frequency and analysis using the BRIDGES API
 
from bridges.data_src_dependent.data_source import get_shakespeare_data
 
#=========================================
# Retrieve Shakespeare's Work
#=========================================
 
#Get all of Shakespeare's poems 
poems = get_shakespeare_data("poems")
print(f"Fetched {len(poems)} poems\n")
 
#Pick one sonnet to analyze that is short enough to recurse through
sonnets = [p for p in poems if p.type == "sonnet"]
#if not sonnets availible use a poem
work = sonnets[0] if sonnets else poems[0]
print(f"Analyzing: {work.title} ({work.type})\n")
 
#Clean up the text: lowercase everything and strip out punctuation,
cleaned_text = "".join(char for char in work.text.lower() if char.isalpha() or char.isspace())
words = cleaned_text.split()
print(f"Total words in this work: {len(words)}\n")
 
#=========================================
# Recursive Algorithm Analysis
#=========================================
 
#Recursive function that counts word frequency.
#It looks at one word at a time at index
#adds it to the dictionary, then calls itself again for the next index
def count_words(words, index, freq):
    #Checks if the function reached the end of the list, ends recursion
    if index == len(words):
        return freq
 
    word = words[index]
    freq[word] = freq.get(word, 0) + 1
 
    #Recursive case: process the next word
    return count_words(words, index + 1, freq)
 
word_freq = count_words(words, 0, {})
 
#=========================================
# Display and Analyze Results
#=========================================
 
#Sort the words by frequency, most common first
sorted_words = sorted(word_freq.items(), key=lambda pair: pair[1], reverse=True)
 
#Print the most common words and their frequency
print("Most Common Words")
print("-" * 30)
for word, count in sorted_words[:15]:
    print(f"{word:<15} {count}")
    
#Discuss the significance of the words in the context of Shakespeare's writing style
discussion = """In a Shakespearean sonnet, the most common words are usually funtional words such as (not, the, when, of) and thematic pronouns/nouns (I, my, thee, thy, thou)
Shakespeare does this because it was the style of English used during the 1500-1600s. 
Moreover, these pronouns are specifically used because Shakespeare loved short single syllable words to match an iambic pentameter style. 
Shakespeares sonnets were typically focused around love and tragedy, therefore he always uses words that mention beauty and the heart """
print("\n", discussion)