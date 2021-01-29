# This method has time complexity O(N), and space complexity O(N)
# It read line from file, and then find tokens wirh regular expression and add it to result list
def tokenize(TextFilePath: str) -> list:
	import re
	file = open(TextFilePath, "r")
	result = []
	for line in file:
                result += [x.lower() for x in re.findall("[a-zA-Z0-9]+[a-zA-Z0-9]+", line)]
	file.close()
	return result

# This method has time complexity O(N), space complexity O(N)
# looping through tokenList, and update dict accordingly
def computeWordFrequencies(tokenList: list) -> dict:
	result = {}
	for token in tokenList:
		if token not in result:
			result.update({token: 1})
		else: result[token] += 1
	return result

# This method has time complexity O(N log N), space complexity O(N)
# it utilizes python built-in sort method and print in order, and python built-in sort has time complexity O(N log N), space complexity O(N)
def myPrint(wordFrequencies: dict) -> None:
	for key, value in sorted(wordFrequencies.items(), key=lambda x:-x[1]):
		print(f'{key}->{value}')


if __name__ == "__main__":
	import sys
	from os import path
	if len(sys.argv) == 2 and path.exists(sys.argv[1]):
		myPrint(computeWordFrequencies(tokenize(sys.argv[1])))
	else: print("It only accepts one existing file directory as stdin")

