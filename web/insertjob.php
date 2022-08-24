<!doctype html>
<html lang="it">
<head> <title> Inserimento JOB </title> <meta charset="utf-8" /> </head>
<body>
<?php
$var1= $_POST['nome'];
$var2= $_POST['ip'];
$var3= $_POST['netmask'];
$var4= $_POST['enable'];


echo "Valori inseriti:$var1 , $var2 , $var3 , $var4";

$username = "operator";
$password = "!d3f3n510!";
$database = "defensio";
$conn = new mysqli("localhost", $username, $password, $database);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}




$sql = "INSERT INTO job (id_job, nome, ip, netmask, abilitato)VALUES (NULL,'$var1','$var2','$var3','$var4')";

if ($conn->query($sql) === TRUE) {
  echo "<br>New record created successfully";
} else {
  echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
</body> </html>