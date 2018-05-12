<html>
  <head>
    <title>SMTP Client</title>
  </head>

  <body>
    <h1>Register</h1>
    <form method="post">
      <input type="text" name="usernameToRegister" placeholder="Username"><br>
      <input type="password" name="passwordToRegister" placeholder="Password"><br>
      <input type="submit" value="Submit">
      <select name="taskOption">
        <option value="info">info</option>
        <option value="warning">warning</option>
        <option value="error">error</option>
      </select>
    </form>
    <h1>Login</h1>
    <form method="post">
      <input type="text" name="username" placeholder="Username"><br>
      <input type="password" name="password" placeholder="Password"><br>
      <input type="submit" value="Submit">
      <select name="taskOption">
        <option value="info">info</option>
        <option value="warning">warning</option>
        <option value="error">error</option>
      </select>
    </form>
    <?php
      openlog('smtpClient', LOG_CONS | LOG_NDELAY | LOG_PID, LOG_USER | LOG_PERROR);
      $option = $_POST['taskOption'];
      $username = $_POST['username'];
      $password = $_POST['password'];
      $usernameToRegister = $_POST['usernameToRegister'];
      $passwordToRegister = $_POST['passwordToRegister'];
      $hashedPassword = md5($password);
      $hashedPasswordToRegister = md5($passwordToRegister);
      $dbhost = 'localhost:3036';
      $dbuser = 'root';
      $mysqli = new mysqli('localhost', $dbuser, 'toor', 'users');
      $inputAvailable = false;
      if ($mysqli->connect_errno) {
        printf("Connect failed: %s\n", $mysqli->connect_error);
        syslog(LOG_ERR, "Connect failed: " + $mysqli->connect_error);
        exit();
      }
      //register
      if (strlen($usernameToRegister) > 0 and strlen($hashedPasswordToRegister) > 0) {
        // $register = mysqli_query($mysqli, "insert into user (username, password) values ('$usernameToRegister','$hashedPasswordToRegister');");
        $stmt = $mysqli->prepare("select * from user where username=?");
        $stmt->bind_param("s", $usernameToRegister);
        $stmt->execute();
        $registerResult = $stmt->get_result();
        $notUniqueUsername = ($registerResult->num_rows === 0 ? false : true);
        if ($notUniqueUsername) {
          echo "user already exists";
          if ($option == "warning") {
            syslog(LOG_WARNING, "WARNING, username: $usernameToRegister is already in use");
          } elseif ($option == "error") {
            syslog(LOG_ERR, "ERROR, someone tried to register as $usernameToRegister");
          }
        } else {
          $stmt = $mysqli->prepare("insert into user (username, password) values (?,?);");
          $stmt->bind_param("ss", $usernameToRegister, $hashedPasswordToRegister);
          $stmt->execute();
          echo "new user is registered";
          if ($option == "info") {
            syslog(LOG_INFO, "INFO, new user is registered");
          }
        }
      }
      //login
      if (strlen($username) > 0 and strlen($hashedPassword)) {
        $stmt = $mysqli->prepare("select * from user where username=? and password=?");
        $stmt->bind_param("ss", $username, $hashedPassword);
        $stmt->execute();
        $loginResult = $stmt->get_result();
        // $loginResult = mysqli_query($mysqli, "select * from user where username='$username' and password='$hashedPassword'");
        $notloggedIn = ($loginResult->num_rows === 0 ? true : false);
        if ($notloggedIn) {
          echo "incorrect username or password or user does not exist";
          if ($option == "warning") {
            syslog(LOG_WARNING, "WARNING, incorrect log in information about user: $username");
          } elseif ($option == "error") {
            syslog(LOG_ERR, "ERROR, someone tried to log in as $username");
          }
        } else {
          echo "Logged in";
          if ($option == "info") {
            syslog(LOG_INFO, "INFO, $username has Logged in");
          }
          $inputAvailable = true;
        }
      }
      $mysqli->close();
      closelog();
    ?>

    <?php if($inputAvailable) : ?>
      <a href="correo.php">Click to proceed to the mailing view</a>
    <?php endif; ?>

  </body>
</html>
