@echo off
dir /b "C:\Users\alumno\Documents\Kolirio\software" > lista_archivos.txt


@echo off
setlocal enabledelayedexpansion

rem Ruta de la carpeta con los archivos
set "CARPETA=C:\Users\alumno\Documents\Kolirio\software"

rem Archivo donde se guardará la lista
set "LISTA=lista_archivos.txt"

rem Archivo BAT que ejecutará los archivos listados
set "EJECUTAR=ejecutar_archivos.bat"

rem Generar la lista de archivos (solo archivos, sin carpetas)
dir /b /a-d "%CARPETA%" > "%LISTA%"

rem Crear el archivo BAT que ejecutará los archivos
echo @echo off > "%EJECUTAR%"
for /f "delims=" %%f in (%LISTA%) do (
    echo start "" "%CARPETA%\%%f" >> "%EJECUTAR%"
)

rem (Opcional) Ejecutar el archivo que corre los archivos
call "%EJECUTAR%"
