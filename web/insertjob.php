<!doctype html>
<html lang="it">
<head> <title> Inserimento JOB </title> <meta charset="utf-8" />
    <link rel="stylesheet" href="ollie.css">
</head>
<body>
 <div id="hormenu"><!-- div che contiene il menu -->
        <ul> <!-- lista principale: definisce il menu nella sua interezza -->
            <li>
            <a href="#">DEFENSIO SYSTEM </a> <!-- primo list-item, prima voce del menu -->
            <ul> <!-- Lista annidata: voci del sotto-menu -->

                <li><a href="index.html">Main Page</a></li>
                <li><a href="form_job.html">Inserimento JOB</a></li>
                <li><a href="extract_host.php">Lista HOST</a></li>
                <li><a href="extract_service.php">Lista Servizi</a></li>
                <li><a href="extract_job.php">Job</a></li>
            </ul> <!-- Fine del sotto-menu -->
            </li> <!-- Chiudo il list-item -->
        </ul>
    </div>

<?php
$var1= $_POST['nome'];
$var2= $_POST['ip'];
$var3= $_POST['netmask'];
$var4= $_POST['enable'];
$var5= $_POST['enable_arachni'];

if ($var4 == '')
  $var4='off';
if ($var5 == '')
  $var5='off';


echo "<h3>Valori inseriti:Nome Job: $var1  Indirizzo IP:  $var2  Netmask:  $var3  Abilitazione:  $var4 Arachni:  $var5 </h3>";

$username = "operator";
$password = "!d3f3n510!";
$database = "defensio";
$conn = new mysqli("localhost", $username, $password, $database);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}




$sql = "INSERT INTO job (id_job, nome, ip, netmask, abilitato, esecuzione, arachni )VALUES (NULL,'$var1','$var2','$var3','$var4','off','$var5')";



if ($conn->query($sql) === TRUE) {
  echo "<h1>Record Inserito correttamente.</h1>";
} else {
  echo "Error: " . $sql . "<br>" . $conn->error;
}


$conn->close();
header("Refresh:4; url=extract_host.php");
?>
</body> </html>