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
    </form>
    <h1>Login</h1>
    <form method="post">
      <input type="text" name="username" placeholder="Username"><br>
      <input type="password" name="password" placeholder="Password"><br>
      <input type="submit" value="Submit">
    </form>
    <?php
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
        exit();
      }
      //register
      if (strlen($usernameToRegister) > 0 and strlen($hashedPasswordToRegister) > 0) {
        $register = mysqli_query($mysqli, "insert into user (username, password) values ('$usernameToRegister','$hashedPasswordToRegister');");
      }
      //login
      if (strlen($username) > 0 and strlen($hashedPassword)) {
        $loginResult = mysqli_query($mysqli, "select * from user where username='$username' and password='$hashedPassword'");
        $notloggedIn = ($loginResult->num_rows === 0 ? true : false);
        if ($notloggedIn) {
          echo "incorrect username or password or user does not exist";
        } else {
          echo "Logged in";
          $inputAvailable = true;
        }
      }
      $mysqli->close();
    ?>

    <?php if($inputAvailable) : ?>
      <a href="correo.php">Click to proceed to the mailing view</a>
    <?php endif; ?>

  </body>
</html>
