"""
This Python script prompts the user to input their name and a number. It then extracts a specified number of characters from the left of the name, counts the number of vowels in the name (case insensitive), and prints the reversed name.
"""

name = input('\nEnter your name: ')

print("____________________________________\n")

print("Name:", name)

n = int(input("Enter the number of characters to extract from the left: ")) 
left_chars = name[:n]
print("Left characters:", left_chars)

vowels = ['a', 'e', 'i', 'o', 'u']
count = 0
for char in name.lower():
    if char in vowels: 
       count += 1
print("Number of vowels:", count)

reversed_name = name[::-1] 
print("Reversed name:", reversed_name)

