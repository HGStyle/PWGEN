<?php

// Create the PWGEN function
function pwgen($gentype) {
    $password = "";
    // Get the language names
    $langnames = json_decode(file_get_contents("data" . DIRECTORY_SEPARATOR . "langnames.json"), true);
    if (in_array($gentype, array_keys($langnames))) {
        // Get a random order of words
        $orders = json_decode(file_get_contents("data" . DIRECTORY_SEPARATOR . "orders.json"), true);
        $order = $orders[array_rand($orders)];
        // Get a random word of each word type
        foreach ($order as $wordtype) {
            if ($wordtype == "pron") {
                $pron = explode("\r\n", file_get_contents("data" . DIRECTORY_SEPARATOR . $gentype . DIRECTORY_SEPARATOR . "pron.txt"));
                $password .= $pron[array_rand($pron)];
                unset($pron);
            } else if ($wordtype == "noun") {
                $noun = explode("\r\n", file_get_contents("data" . DIRECTORY_SEPARATOR . $gentype . DIRECTORY_SEPARATOR . "noun.txt"));
                $password .= $noun[array_rand($noun)];
                unset($noun);
            } else if ($wordtype == "adj") {
                $adj = explode("\r\n", file_get_contents("data" . DIRECTORY_SEPARATOR . $gentype . DIRECTORY_SEPARATOR . "adj.txt"));
                $password .= $adj[array_rand($adj)];
                unset($adj);
            } else if ($wordtype == "verb") {
                $verb = explode("\r\n", file_get_contents("data" . DIRECTORY_SEPARATOR . $gentype . DIRECTORY_SEPARATOR . "verb.txt"));
                $password .= $verb[array_rand($verb)];
                unset($verb);
            }
            $password .= " ";
        }
    } else if ($gentype == "syllab") {
        // Load the syllabs
        $syllabs = explode("\r\n", file_get_contents("data" . DIRECTORY_SEPARATOR . "syllabs.txt"));
        // Generate the password
        $iterations = mt_rand(4, 8);
        for ($i=0; $i<$iterations; $i++) {
            $password .= $syllabs[array_rand($syllabs)];
        }
    }
    return trim($password);
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>PWGEN - Generate a random, secure and easy-to-remember password!</title>
    </head>
    <body>
        <?php if (isset($_GET['type'])) { ?>
            <h1><?php echo pwgen($_GET['type']); ?></h1>
            <h2>might be your new password... <a href="?type=<?php echo $_GET['type']; ?>">Or not?</a></h2>
            <br><h3>Change password type</h3>
        <?php } else { ?>
            <h1>PWGEN by HGStyle</h1>
            <br><h2>Select the type of password to generate</h2>
        <?php } ?>
        <a href="?type=english">Passphrase in English</a><br>
        <a href="?type=french">Phrase de passe en Français</a><br>
        <a href="?type=german">Passphrase auf Deutsch</a><br>
        <a href="?type=polish">Hasło w języku polskim</a><br>
        <a href="?type=spanish">Frase de paso en Español</a><br>
        <a href="?type=syllab">Password made out of syllabs (beta)</a><br>
    </body>
    <style>
        body {
            margin-left: 20%;
            margin-top: 5%;
            font-family: sans-serif;
            font-size: 125%;
            color: dimgray;
            background-color: whitesmoke;
        }
    </style>
</html>
