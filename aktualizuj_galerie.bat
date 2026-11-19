@echo off
chcp 65001 >nul
echo Aktualizowanie galerii zdjec...
python "%~dp0aktualizuj_galerie.py"
echo.
echo Gotowe! Wcisnij dowolny klawisz, aby zamknac...
pause >nul
