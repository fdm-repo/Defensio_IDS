<?php
$username = "operator";
$password = "!d3f3n510!";
$database = "defensio";
$mysqli = new mysqli("localhost", $username, $password, $database);
$query = "SELECT * FROM job";


echo '   <!DOCTYPE html>
        <html>
        <title>Job List</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="10" >
        <head>
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
                <li><a href="extract_report_arachni.php">Report Arachni</a></li>
            </ul> <!-- Fine del sotto-menu -->
            </li> <!-- Chiudo il list-item -->
        </ul>
    </div>
        <h1>Lista JOB</h1>
        <table class="styled-table" border="1" cellspacing="2" cellpadding="2">
         <tr>
          <td> <font face="Arial">ID_JOB</font> </td>
          <td> <font face="Arial">NOME</font> </td>
          <td> <font face="Arial">IP</font> </td>
          <td> <font face="Arial">NETMASK</font> </td>
          <td> <font face="Arial">NMAP</font> </td>
          <td> <font face="Arial">NMAP eseguito</font> </td>
          <td> <font face="Arial">ARACHNI</font> </td>
        </tr>';

if ($result = $mysqli->query($query)) {
    while ($row = $result->fetch_assoc()) {
        $field1name = $row["id_job"];
        $field2name = $row["nome"];
        $field3name = $row["ip"];
        $field4name = $row["netmask"];
        $field5name = $row["abilitato"];
        $field6name = $row["esecuzione"];
        $field7name = $row["arachni"];

        echo '<tr>
                  <td>'.$field1name.'</td>
                  <td>'.$field2name.'</td>
                  <td>'.$field3name.'</td>
                  <td>'.$field4name.'</td>
                  <td>'.$field5name.'</td>
                  <td>'.$field6name.'</td>
                  <td>'.$field7name.'</td>
              </tr>';
    }
    $result->free();
}
echo '   </table>';
echo'</body>';
echo '</html>';
$mysqli->close();
header('Refresh: 10');
?>