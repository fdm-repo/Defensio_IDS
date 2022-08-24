<!doctype html>
<html lang="it">
<head> <title> Start JOB </title> <meta charset="utf-8" /> </head>
<body>
<?php
$var1= $_POST['job'];

echo "job da avviare:$var1";

$command= 'python3 /home/defensio/defensio2.py';
exec($command, $out, $status);

?>
</body> </html>