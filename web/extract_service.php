<?php
$username = "operator";
$password = "!d3f3n510!";
$database = "defensio";
$mysqli = new mysqli("localhost", $username, $password, $database);
$query = "SELECT * FROM Port";


echo '   <!DOCTYPE html>
        <html>
        <title>List SERVICE</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="stylesheet" href="ollie.css">
        <body>
        <ul id="menu">
            <li><a href=index.html>Main</a></li>
            <li><a href=form_job.html>Inserisci nuovo Job</a></li>
            <li><a href=extract_host.php>Elenco HOST Job</a></li>
            <li><a href=extract_service.php>Elenco SERVIZI Job</a></li>
        </ul>
        <h1>Lista SERVICE</h1>
        <table class="styled-table" border="1" cellspacing="2" cellpadding="2">
         <tr>
          <td> <font face="Arial">ID Service</font> </td>
          <td> <font face="Arial">ID JOB</font> </td>
          <td> <font face="Arial">IP</font> </td>
          <td> <font face="Arial">Porta N°</font> </td>
          <td> <font face="Arial">Nome Servizio</font> </td>
          <td> <font face="Arial">Stato Servizio</font> </td>
          <td> <font face="Arial">Metodo</font> </td>
          <td> <font face="Arial">Software</font> </td>
          <td> <font face="Arial">Versione</font> </td>
          <td> <font face="Arial">Info</font> </td>
        </tr>';

if ($result = $mysqli->query($query)) {
    while ($row = $result->fetch_assoc()) {
        $field1name = $row["id_port"];
        $field2name = $row["id_job"];
        $field3name = $row["ip"];
        $field4name = $row["port_n"];
        $field5name = $row["name"];
        $field6name = $row["state"];
        $field7name = $row["reason"];
        $field8name = $row["product"];
        $field9name = $row["version"];
        $field10name = $row["info"];

        echo '<tr>
                  <td>'.$field1name.'</td>
                  <td>'.$field2name.'</td>
                  <td>'.$field3name.'</td>
                  <td>'.$field4name.'</td>
                  <td>'.$field5name.'</td>
                  <td>'.$field6name.'</td>
                  <td>'.$field7name.'</td>
                  <td>'.$field8name.'</td>
                  <td>'.$field9name.'</td>
                  <td>'.$field10name.'</td>
              </tr>';
    }
    $result->free();
}
echo '   </table>';
echo'</body>';
echo '</html>';
$mysqli->close();
?>