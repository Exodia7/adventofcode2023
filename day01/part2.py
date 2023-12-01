
INPUT_FILE = 'input.txt'

with open(INPUT_FILE, 'r') as f: 
    lines = f.readlines()
    
    strNums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    numbers = []
    for line in lines:
        # find all digits in the line
        digits = []
        for i in range(len(line)):
            if line[i].isdigit():
                digits.append(int(line[i]))
            else:
                # check if there's a number in string form here
                j = 0
                while (j < len(strNums)):
                    current = strNums[j]
                    # check that 
                    # 1) there are still enough characters from i to the end of the line to possibly have this string here
                    # 2) the string is indeed there
                    if (i < len(line) - len(current) and line[i:i+len(current)] == current):
                        digits.append(j+1)
                        break
                    else:
                        j += 1
        
        
        # assemble just the first and last digit
        number = digits[0] * 10 + digits[-1]
        
        # add the number to the list
        numbers.append(number)
    
    print(f"The answer is: {sum(numbers)}")
    # ANSWER: 54208