<?php

use WHMCS\ClientArea;
use WHMCS\Database\Capsule;

define('CLIENTAREA', true);

require __DIR__ . '/init.php';

$ca = new ClientArea();

$ca->setPageTitle('Company - Discord Unauthentication');
$ca->initPage();
$ca->requireLogin();

$status = $_GET["status"];
if(isset($status)) {
    $ca->assign('status', $status);
    $ca->setTemplate('/templates/discord/disconnect.tpl');
    $ca->output();
    exit();
}

$postfields        = array(
    'client_id' => $ca->getUserID(),
);
$ch                = curl_init();
curl_setopt($ch, CURLOPT_URL, 'http://IP/client/remove');
curl_setopt($ch, CURLOPT_POST, count($postfields));
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postfields));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$final = curl_exec($ch);
if (curl_error($ch)) {
    header('Location: unauth.php?status=error');
    exit();
}
curl_close($ch);

$jsonData = json_decode($final, true);
header('Location: unauth.php?status='. $jsonData['result']);
?>