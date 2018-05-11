
user = ""
if ARGV[0]
  user = ARGV[0].to_s
else
  puts "Correct usage: script, <user to read mails from>"
  exit
end

def checkForUpdatedData(lastData, currentData)
  if lastData.length < currentData.length
    lastData = currentData
  elsif currentData.length > lastData.length
    difference = currentData - lastData
    printData(difference)
  end
end

def printData(difference)
  for data in difference
    puts data
  end
end

while true
  lastData = []
  currentData = []
  file = 'mail.txt'
  File.readlines(file).each do |line|
    puts line
    currentData.push(line)
  end
  checkForUpdatedData(lastData, currentData)
end
