"""
This function invertDictionary takes two file paths as input arguments: inputFile and outputFile. 
It reads a dictionary stored in the inputFile, inverts it, and writes the inverted dictionary to the outputFile.
The input file should contain a string representation of a dictionary. The keys and values can be of any data type, and if a value is a list, each element in the list will be treated as a separate key in the inverted dictionary.
The inverted dictionary is written to the output file, where each line contains a key followed by its corresponding values separated by commas.
"""
def invertDictionary(inputFile, outputFile):
    # Read dictionary from input file
    with open(inputFile, 'r') as file:
        originalDictStr = file.read()

    # Convert the string representation of dictionary to a Python dictionary
    originalDict = eval(originalDictStr)

    # Invert the dictionary
    invertedDict = {}
    for key, value in originalDict.items():
        if isinstance(value, list):
            for v in value:
                invertedDict.setdefault(v, []).append(key)
        else:
            invertedDict.setdefault(value, []).append(key)

    # Write the inverted dictionary to the output file
    with open(outputFile, 'w') as file:
        for key, values in invertedDict.items():
            valuesStr = ', '.join(values)
            file.write(f'{key}: {valuesStr}\n')

# Specify the input and output file paths
inputFilePath = 'input.txt'
outputFilePath = 'output.txt'

# Call the function with the provided file paths
invertDictionary(inputFilePath, outputFilePath)