<?php
$var1= $_POST['nome'];
$var2= $_POST['ip'];
$var3= $_POST['netmask'];
$var4= $_POST['enable'];
$var5= $_POST['enable_arachni'];
$var6= $_POST['enable_enum4linux'];

if ($var4 == '')
  $var4='off';
if ($var5 == '')
  $var5='off';
if ($var6 == '')
  $var6='off';

$username = "operator";
$password = "!d3f3n510!";
$database = "defensio";
$conn = new mysqli("localhost", $username, $password, $database);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}




$sql = "INSERT INTO job (id_job, nome, ip, netmask, abilitato, esecuzione, arachni, enumforlinux )VALUES (NULL,'$var1','$var2','$var3','$var4','off','$var5','$var6')";



if ($conn->query($sql) === TRUE) {
  echo "<h1>Record Inserito correttamente.</h1>";
} else {
  echo "Error: " . $sql . "<br>" . $conn->error;
}


$conn->close();
header("Refresh:4; url=landing.html");
?>