<?php
// Conexión a la base de datos (sin protección)
$conn = mysqli_connect("172.17.0.3", "root", "pwd1234", "ciberseguridad-pIII");

if (!$conn) {
    http_response_code(500);
    echo json_encode(["error" => "Error de conexión a la base de datos."]);
    exit;
}

// Solo permitir método POST
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405); // Método no permitido
    echo json_encode(["error" => "Método no permitido. Solo se acepta POST."]);
    exit;
}

// Obtener datos del cuerpo del POST sin saneamiento
$username = $_POST['username'] ?? '';
$password = md5($_POST['password']) ?? '';

// Consulta deliberadamente vulnerable a inyección SQL
$sql = "SELECT * FROM user_login_data WHERE LoginName = '$username' AND PasswordSalt = '$password'";
file_put_contents("inyeccion.txt", $sql);
$result = mysqli_query($conn, $sql);


// Respuesta JSON en función del resultado
if ($result && mysqli_num_rows($result) == 1) {
    echo json_encode(["success" => true, "message" => "Login exitoso"]);
} else {
    echo json_encode(["success" => false, "message" => "Credenciales inválidas"]);
}
?>
