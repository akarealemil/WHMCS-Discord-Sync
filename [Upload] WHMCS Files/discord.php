<?php

use WHMCS\User\Client;

// Load the shortcut to link accounts
add_hook('ClientAreaSecondarySidebar', 1, function($primarySidebar)
{
    if (!is_null($primarySidebar->getChild('Client Shortcuts'))) {
        $menu = $primarySidebar->getChild('Client Shortcuts')->addChild('Discord')->setIcon('fab fa-discord')->setOrder(100);
        
        $currentUser = Client::find($_SESSION['uid']);
        $connected   = false;
		//Connect to the mysql database (host, username, password, database)
        $conn        = new mysqli('Host', 'username', 'password', 'database');
        if ($conn->connect_error == false) {
			//Check the database to see if the client is connected.
            $sql    = "SELECT * FROM whmcs_discord WHERE client_id = " . $currentUser->id;
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
                $connected = true;
            }
            $conn->close();
        }
        if ($connected) {
            $menu->setLabel('Disconnect from Discord')->setUri("unauth.php");
        } else {
            $menu->setLabel('Connect to Discord')->setUri('discordConnection');
        }
    }
    ;
});

?>