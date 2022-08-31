<?php
$username = "operator";
$password = "!d3f3n510!";
$database = "defensio";
$mysqli = new mysqli("localhost", $username, $password, $database);
$query = "SELECT arachni_report.id_arac_report, job.id_job, job.nome, job.ip FROM `arachni_report`INNER JOIN job WHERE arachni_report.id_job = job.id_job;";


echo '   <!DOCTYPE html>
        <html>
        <title>ARACHNI Report List</title>
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
        <h1>Lista ARACHNI Report</h1>
        <table class="styled-table" border="1" cellspacing="2" cellpadding="2">
         <tr>
          <td> <font face="Arial">ID_REPORT</font> </td>
          <td> <font face="Arial">ID JOB</font> </td>
          <td> <font face="Arial">NOME</font> </td>
          <td> <font face="Arial">IP</font> </td>
          <td> <font face="Arial">LINK</font> </td>
    </tr>';

if ($result = $mysqli->query($query)) {
    while ($row = $result->fetch_assoc()) {
        $field1name = $row["id_arac_report"];
        $field2name = $row["id_job"];
        $field3name = $row["nome"];
        $field4name = $row["ip"];

        echo '<tr>
                  <td>'.$field1name.'</td>
                  <td>'.$field2name.'</td>
                  <td>'.$field3name.'</td>
                  <td>'.$field4name.'</td>
                  <td><a href="../report/'.$field2name.'/Arachni_http/index.html">Report Job '.$field2name.'</a></td>
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