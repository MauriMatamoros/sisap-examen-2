<html>
  <head>
    <title>SMTP Client</title>
  </head>

  <body>
    <h1>Correo</h1>
    <form method="post">
      <input type="text" name="from" placeholder="From"><br>
      <input type="text" name="to" placeholder="To"><br>
      <textarea name="data"></textarea>
      <input type="submit" value="Submit">
    </form>
    <?php
      $from = $_POST['from'];
      $to = $_POST['to'];
      $data = $_POST['data'];
      $host = "127.0.0.1";
      $port = 4445;
      // create socket
      $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
      if (strlen($from) > 0 and strlen($to) > 0 and strlen($data) > 0) {
        // connect to server
        $result = socket_connect($socket, $host, $port) or die("Could not connect to server\n");
        // send strings to server
        $helo = "helo: ";
        $heloResponse = "250 " + $from + ", I am glad to meet you\n";
        $mailFrom = "mail from: ";
        $mailFromResponse = "250 ok\n";
        $from .= "\n";
        $helo .= $from;
        $mailFrom .= $from;
        socket_write($socket, $helo, strlen($helo)) or die("Could not send data to server\n");
        $result = socket_read($socket, 1024) or die("Could not read server response\n");
        if (strcmp($result, $heloResponse)) {
          sleep(0.5);
          socket_write($socket, $mailFrom, strlen($mailFrom)) or die("Could not send data to server\n");
          $result = socket_read($socket, 1024) or die("Could not read server response\n");
          if (strcmp($result, $mailFromResponse)) {
            $to = str_replace(",", "", $to);
            $to = explode(" ", $to);
            for ($i=0; $i < sizeof($to); $i++) {
              $rcptTo = "rcpt to: " + $to[$i] + "\n";
              echo "$rcptTo";
              // socket_write($socket, $rcptTo, strlen($rcptTo)) or die("Could not send data to server\n");
              // $result = socket_read($socket, 1024) or die("Could not read server response\n");
            }

          } else {
            // log
          }
        } else {
          //log
        }
        // get server response
        $result = socket_read($socket, 1024) or die("Could not read server response\n");
        echo "Reply From Server  :".$result;
      }
      // close socket
      socket_close($socket);
    ?>

  </body>
</html>
