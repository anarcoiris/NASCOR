#include <stdio.h>
#include <stdlib.h>

int main() {
FILE *f = fopen("/var/www/html/datos/BTCUSDT.json", "r"); // ruta NO relativa para el contenedor
    if (f == NULL) {
        printf("Status: 500 Internal Server Error\n");
        printf("Content-Type: text/plain\n\n");
        printf("No se pudo abrir el archivo JSON\n");
        return 1;
    }

    // Cabecera HTTP
    printf("Content-Type: application/json\n\n");

    // Imprimir contenido del JSON
    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), f) != NULL) {
        printf("%s", buffer);
    }

    fclose(f);
    return 0;
}
