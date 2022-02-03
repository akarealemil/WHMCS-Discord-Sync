<?php

use WHMCS\ClientArea;
use WHMCS\Database\Capsule;

define('CLIENTAREA', true);

require __DIR__ . '/init.php';

$ca = new ClientArea();

$ca->setPageTitle('Company - Discord Authentication');
$ca->initPage();
$ca->requireLogin();

$status = $_GET["status"];
if(isset($status)) {
    $ca->assign('status', $status);
    $ca->setTemplate('/templates/discord/connect.tpl');
    $ca->output();
    exit();
}

$code = $_GET["code"];
if (!isset($code)) {
    header('Location: index.php');
    exit();
}

$clientId     = "ClientID";
$clientSecret = "ClientSecret";

$postfields        = array(
    'client_id' => $clientId,
    'client_secret' => $clientSecret,
    'grant_type' => 'authorization_code',
    'code' => $code,
    'redirect_uri' => 'auth.php on billing site',
    'scope' => 'identify'
);
$ch                = curl_init();
$request_headers   = array();
$request_headers[] = 'Content-Type: application/x-www-form-urlencoded';
$request_headers[] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36';
curl_setopt($ch, CURLOPT_URL, 'https://discordapp.com/api/oauth2/token');
curl_setopt($ch, CURLOPT_POST, count($postfields));
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postfields));
curl_setopt($ch, CURLOPT_HTTPHEADER, $request_headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

$response = curl_exec($ch);
if (curl_error($ch)) {
    header('Location: auth.php?status=error');
    exit();
}

curl_close($ch);
$jsonData = json_decode($response, true);
$token    = $jsonData['access_token'];
if (!isset($token)) {
    header('Location: auth.php?status=error');
    exit();
}

$request_headers   = array();
$request_headers[] = 'Authorization: Bearer ' . $token;
$request_headers[] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36';

$ch = curl_init("https://discordapp.com/api/v6/users/@me");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $request_headers);
$data = curl_exec($ch);
if (curl_error($ch)) {
    header('Location: auth.php?status=error');
    exit();
}
curl_close($ch);

$jsonData = json_decode($data, true);

$postfields        = array(
    'client_id' => $ca->getUserID(),
    'discord_id' => $jsonData['id']
);
$ch                = curl_init();
curl_setopt($ch, CURLOPT_URL, 'http://IP/client/add');
curl_setopt($ch, CURLOPT_POST, count($postfields));
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postfields));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$final = curl_exec($ch);
if (curl_error($ch)) {
    header('Location: auth.php?status=error');
    exit();
}
curl_close($ch);

$jsonData = json_decode($final, true);
header('Location: auth.php?status='. $jsonData['result']);
?>