<!doctype html>
<html lang="it">
<head> <title> Inserimento JOB </title> <meta charset="utf-8" />
    <link rel="stylesheet" href="ollie.css">
</head>
<body>
<?php
$var1= $_POST['nome'];
$var2= $_POST['ip'];
$var3= $_POST['netmask'];
$var4= $_POST['enable'];


echo "<h3>Valori inseriti:Nome Job: $var1  Indirizzo IP:  $var2  Netmask:  $var3  Abilitazione:  $var4 </h3>";

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
  echo "<h1>Record Inserito correttamente.</h1>";
} else {
  echo "Error: " . $sql . "<br>" . $conn->error;
}
echo '<ul id="menu">
            <li><a href=index.html>Main</a></li>
            <li><a href=form_job.html>Inserisci nuovo Job</a></li>
            <li><a href=extract_host.php>Elenco HOST Job</a></li>
            <li><a href=extract_service.php>Elenco SERVIZI Job</a></li>
        </ul>';

$conn->close();
?>
</body> </html>