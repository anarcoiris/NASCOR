<?php
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';

if (preg_match('/^https?:\/\/(127\.0\.0\.1|localhost)(:\d+)?$/', $origin)) {
    header("Access-Control-Allow-Origin: $origin");
}

header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");

// Si la solicitud es de tipo OPTIONS, responde sin procesar más.
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}


// Parámetros de conexión a la base de datos
// Configuración de la base de datos
$host = '172.17.0.3:3306'; // Cambia esto si tu base de datos está en otro servidor
$dbname = 'ciberseguridad-pIII'; // Reemplaza con tu base de datos
$username = 'root'; // Reemplaza con tu usuario
$password = 'root'; // Reemplaza con tu contraseña

//Ayuda <https://chatgpt.com/c/670b81df-13f8-8007-a304-533658d1b56c>

try {
    // Crear la conexión a la base de datos usando PDO
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    // Configurar PDO para que lance excepciones en caso de errores
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verificar si se ha enviado el formulario a través de POST
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Obtener los datos del formulario (loginName y password)
        $loginName = $_POST['loginName'];
        $password = $_POST['password'];

        // Preparar la consulta para obtener los datos del usuario
        $stmt = $pdo->prepare('
            SELECT ul.PasswordHash, ul.PasswordSalt, ha.AlgorithmName
            FROM user_login_data ul
            JOIN hashing_algorithms ha ON ul.HashAlgorithmId = ha.HashAlgorithmId
            WHERE ul.LoginName = :loginName
        ');
        // Ejecutar la consulta con el nombre de usuario proporcionado
        $stmt->execute(['loginName' => $loginName]);

        // Obtener el resultado de la consulta
        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        // Verificar si el usuario existe
        if ($user) {
            $passwordHash = $user['PasswordHash'];
            $passwordSalt = $user['PasswordSalt'];
            $hashAlgorithm = $user['AlgorithmName'];

            // Generar el hash de la contraseña proporcionada usando el salt
            $hashedInputPassword = '';
            if ($hashAlgorithm === 'MD5') {
                // Concatenar la contraseña proporcionada con el salt y generar el hash MD5
                $hashedInputPassword = md5($password . $passwordSalt);
            } elseif ($hashAlgorithm === 'SHA256') {
                // Hash usando SHA256
                $hashedInputPassword = hash('sha256', $password . $passwordSalt);
            } elseif ($hashAlgorithm === 'BCRYPT') {
                // BCRYPT se maneja diferente ya que incluye el salt en el propio hash
                if (password_verify($password, $passwordHash)) {
                    $hashedInputPassword = $passwordHash; // La verificación de BCRYPT es directa
                }
            }

            // Comparar el hash generado con el almacenado en la base de datos
            if ($hashedInputPassword === $passwordHash) {
                // Contraseña válida
                echo "Bienvenido";
            } else {
                // Contraseña incorrecta
                echo "Contraseña incorrecta.";
            }
        } else {
            // Usuario no encontrado
            echo "Usuario no encontrado.";
        }
    }
} catch (PDOException $e) {
    // Mostrar mensaje de error en caso de fallo de la conexión
    echo "Error en la conexión a la base de datos: " . $e->getMessage();
}
?>
