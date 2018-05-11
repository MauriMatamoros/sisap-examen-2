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
      $log = fopen('log.txt', 'a');
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
        $helo = "helo: phpClient\n";
        $heloResponse = "250 $from, I am glad to meet you\n";
        $mailFrom = "mail from: $from\n";
        $mailFromResponse = "250 ok\n";
        $dataRequest = "data\n";
        $dataRequestResponse = "354 End data with <CR><LF>.<CR><LF>\n";
        $data .= "\n";
        $dataResponse = "250 Ok: queued as 12345\n";
        socket_write($socket, $helo, strlen($helo)) or die("Could not send data to server\n");
        $result = socket_read($socket, 1024) or die("Could not read server response\n");
        fwrite($log, $result);
        if (strcmp($result, $heloResponse)) {
          sleep(2);
          socket_write($socket, $mailFrom, strlen($mailFrom)) or die("Could not send data to server\n");
          $result = socket_read($socket, 1024) or die("Could not read server response\n");
          fwrite($log, $result);
          if (strcmp($result, $mailFromResponse)) {
            sleep(2);
            $to = str_replace(",", "", $to);
            $to = explode(" ", $to);
            for ($i=0; $i < sizeof($to); $i++) {
              $rcpt = "rcpt to: $to[$i]\n";
              socket_write($socket, $rcpt, strlen($rcpt)) or die("Could not send data to server\n");
              sleep(3);
              $result = socket_read($socket, 1024) or die("Could not read server response\n");
              fwrite($log, $result);
              sleep(2);
            }
            if (strcmp($result, $mailFromResponse)) {
              fwrite($log, "entre\n");
              sleep(2);
              socket_write($socket, $dataRequest, strlen($dataRequest)) or die("Could not send data to server\n");
              $result = socket_read($socket, 1024) or die("Could not read server response\n");
              fwrite($log, $result);
              if (strcmp($result, $dataRequestResponse)) {
                sleep(2);
                socket_write($socket, $data, strlen($data)) or die("Could not send data to server\n");
                sleep(2);
                socket_write($socket, ".\n", strlen(".\n")) or die("Could not send data to server\n");
                $result = socket_read($socket, 1024) or die("Could not read server response\n");
                fwrite($log, $result);
              }
            }
          }
        }
        // get server response
      }
      // close socket
      socket_close($socket);
      fclose($log);
    ?>

  </body>
</html>
