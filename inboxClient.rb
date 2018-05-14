require 'socket'

stayConnected = true;

puts("Whats your name?")

name = gets
hostname = '10.8.0.14'
port = 25
s = TCPSocket.open(hostname, port)
s.send("ruby\n", 0)
sleep(3)
s.send(name, 0)
while stayConnected
  sleep(1)
  line = s.gets
  puts "#{line}"
  if line == nil
    s.close
  end
end
