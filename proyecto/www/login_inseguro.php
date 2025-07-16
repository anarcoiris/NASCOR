<?php
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Conexión vulnerable: sin try-catch y sin atributos de seguridad
$pdo = new PDO("mysql:host=172.18.0.2;dbname=ciberseguridad-pIII", "root", "pwd1234");

// Entrada sin sanitización (potencial para SQL injection)
$loginName = $_POST['loginName'] ?? '';
$password = $_POST['password'] ?? '';

// Consulta sin parametrizar (vulnerabilidad clave)
$query = "
    SELECT ul.PasswordHash, ul.PasswordSalt, ha.AlgorithmName
    FROM user_login_data ul
    JOIN hashing_algorithms ha ON ul.HashAlgorithmId = ha.HashAlgorithmId
    WHERE ul.LoginName = '$loginName'
";

$result = $pdo->query($query);
$user = $result->fetch(PDO::FETCH_ASSOC);

// Mensajes diferentes permiten enumerar usuarios (vulnerabilidad)
if ($user) {
    $passwordHash = $user['PasswordHash'];
    $passwordSalt = $user['PasswordSalt'];
    $hashAlgorithm = $user['AlgorithmName'];

    $hashedInputPassword = '';
    if ($hashAlgorithm === 'MD5') {
        $hashedInputPassword = md5($password . $passwordSalt);
    } elseif ($hashAlgorithm === 'SHA256') {
        $hashedInputPassword = hash('sha256', $password . $passwordSalt);
    } elseif ($hashAlgorithm === 'BCRYPT') {
        if (password_verify($password, $passwordHash)) {
            $hashedInputPassword = $passwordHash;
        }
    }

    // Comparación débil
    if ($hashedInputPassword === $passwordHash) {
        echo "OK";
    } else {
        echo "Contraseña incorrecta.";
    }
} else {
    echo "Usuario no encontrado.";
}
?>
