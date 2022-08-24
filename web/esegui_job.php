<?php
$username = "operator";
$password = "!d3f3n510!";
$database = "defensio";
$mysqli = new mysqli("localhost", $username, $password, $database);
$query = "SELECT * FROM job";


echo '<table border="0" cellspacing="2" cellpadding="2">
      <tr>
          <td> <font face="Arial">ID</font> </td>
          <td> <font face="Arial">ID_JOB</font> </td>
          <td> <font face="Arial">START</font> </td>
          <td> <font face="Arial">IP</font> </td>
          <td> <font face="Arial">HOSTNAME</font> </td>
      </tr>';

if ($result = $mysqli->query($query)) {
    while ($row = $result->fetch_assoc()) {
        $field1name = $row["id_job"];
        $field2name = $row["nome"];
        $field3name = $row["ip"];
        $field4name = $row["netmask"];

        echo '<tr>
                  <td>'.$field1name.'</td>
                  <td>'.$field2name.'</td>
                  <td>'.$field3name.'</td>
                  <td>'.$field4name.'</td>

              </tr>';
    }
    $result->free();
}
$mysqli->close();
?>
<html>
 <head>
 </head>
  <body>

    <div>
        <form action="attiva_job.php" method="post">
        <h1>Nuovo Job</h1>
        <div>
          <p>START JOB</p>
          <div>
            <input type="text" name="job" placeholder="numero job da avviare" />

          </div>
        </div>
        <div>
          <input type="submit" name="start" value="start" />
        </div>
      </form>
    </div>
  </body>
</html>