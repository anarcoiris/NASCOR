<?php
// Configuración de la base de datos
$host = '172.17.0.3:3306'; // Cambia esto si tu base de datos está en otro servidor
$db = 'ciberseguridad-pIII'; // Reemplaza con tu base de datos
$user = 'root'; // Reemplaza con tu usuario
$pass = 'root'; // Reemplaza con tu contraseña
$charset = 'utf8mb4';

// Configuración de la conexión PDO
$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    // Crear una nueva conexión PDO
    $pdo = new PDO($dsn, $user, $pass, $options);

    // Ejecutar la consulta
    $stmt = $pdo->query("SELECT NOW() AS current_datetime");
    
    // Obtener y mostrar el resultado
    $row = $stmt->fetch();
    echo "La fecha y hora actual es: " . $row['current_datetime'];

} catch (\PDOException $e) {
    // Manejo de errores
    throw new \PDOException($e->getMessage(), (int)$e->getCode());
}
?>
