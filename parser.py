def parser(string):
    begining = string.find('@')
    ending = string.find('.')
    if string.find('.') == -1:
        ending = len(string) - 1
    returnString = ""
    while begining < ending:
        returnString += string[begining]
        begining += 1
    return returnString[1:]

test = "<info@mauricio>"

test = parser(test)

print(test)
