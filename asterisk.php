<?php
// Replace with your port if not using the default.
// If unsure check /etc/asterisk/manager.conf under [general];
$port = "5038";
$ip = "192.168.1.71";
$protocol = "tcp";

// Replace with your username. You can find it in /etc/asterisk/manager.conf.
// If unsure look for a user with "originate" permissions, or create one as
// shown at http://www.voip-info.org/wiki/view/Asterisk+config+manager.conf.
$username = "carlos";

// Replace with your password (refered to as "secret" in /etc/asterisk/manager.conf)
$password = "123456789";

// Internal phone line to call from
$internalPhoneline = "sip:100@vaca.ddns.net:5060";

// Context for outbound calls. See /etc/asterisk/extensions.conf if unsure.
$context = "muundogando";

$socket = stream_socket_client("$protocol://$ip:$port");
$target = "102";

$id_vaca = "1000";

if($socket)
{
    echo "Connected to socket, sending authentication request.\n";

    // Prepare authentication request
    $authenticationRequest = "Action: Login\r\n";
    $authenticationRequest .= "Username: $username\r\n";
    $authenticationRequest .= "Secret: $password\r\n";
    $authenticationRequest .= "Events: off\r\n\r\n";

    // Send authentication request
    $authenticate = stream_socket_sendto($socket, $authenticationRequest);
    if($authenticate > 0)
    {
        // Wait for server response
        usleep(200000);

        // Read server response
        $authenticateResponse = fread($socket, 4096);

        // Check if authentication was successful
        if(strpos($authenticateResponse, 'Success') !== false)
        {
            echo "Authenticated to Asterisk Manager Inteface. Initiating call.\n";

            // Prepare originate request
            $originateRequest = "Action: Originate\r\n";
            $originateRequest .= "Channel: PJSIP/default_endpoint/$internalPhoneline\r\n";
            $originateRequest .= "Callerid: Click 2 Call\r\n";
            //$originateRequest .= "Exten: $target,$id_vaca\r\n";
            //$originateRequest .= "Callerid: $target\r\n";
	    $originateRequest .= "Exten: $target\r\n";
	    $originateRequest .= "Context: $context\r\n";
            $originateRequest .= "Priority: 1\r\n";
            //$originateRequest .= "Async: yes\r\n\r\n";

            // Send originate request
            $originate = stream_socket_sendto($socket, $originateRequest);
            if($originate > 0)
            {
                // Wait for server response
                usleep(200000);

                // Read server response
                $originateResponse = fread($socket, 4096);

                // Check if originate was successful
                if(strpos($originateResponse, 'Success') !== false)
                {
                    echo "Call initiated, dialing.";
                } else {
                    echo "Could not initiate call.\n";
                }
            } else {
                echo "Could not write call initiation request to socket.\n";
            }
        } else {
            echo "Could not authenticate to Asterisk Manager Interface.\n";
        }
    } else {
        echo "Could not write authentication request to socket.\n";
    }
} else {
    echo "Unable to connect to socket.";
}
