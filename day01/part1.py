
INPUT_FILE = 'input.txt'

with open(INPUT_FILE, 'r') as f: 
    lines = f.readlines()
    
    numbers = []
    for line in lines:
        # find all digits in the line
        digits = []
        for char in line:
            if char.isdigit():
                digits.append(int(char))
        
        # assemble just the first and last
        number = digits[0] * 10 + digits[-1]
        
        # add the number to the list
        numbers.append(number)
    
    print(f"The answer is: {sum(numbers)}")
    # ANSWER: 54940