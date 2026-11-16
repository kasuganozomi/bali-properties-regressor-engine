@echo off
title Bali Smart Pricing Engine - Pipeline Runner
color 0A
cls
echo ===============================================================================
echo        BALI SMART VILLA ^& HOMESTAY PRICING ENGINE - AUTOMATED PIPELINE
echo               Universitas Udayana - Program Studi Teknologi Informasi
echo ===============================================================================
echo.
echo Menjalankan seluruh pipeline data engineering dan machine learning secara berurutan...
echo.

set "PY_CMD=python"
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0.venv\Scripts\python.exe"
)

cd /d "%~dp0"

echo [1/5] Modul 02: Menggabungkan data mentah dengan cache scraping...
"%PY_CMD%" scripts\02_merge_and_build_dataset.py
if %ERRORLEVEL% NEQ 0 ( echo [ERROR] Gagal pada Modul 02 & pause & exit /b )

echo.
echo [2/5] Modul 03: Preprocessing, deduplikasi, dan pembagian dataset...
"%PY_CMD%" scripts\03_preprocess_and_clean.py
if %ERRORLEVEL% NEQ 0 ( echo [ERROR] Gagal pada Modul 03 & pause & exit /b )

echo.
echo [3/5] Modul 04: Melatih dan membandingkan 3 model ML (5-Fold CV)...
"%PY_CMD%" scripts\04_train_and_benchmark_models.py
if %ERRORLEVEL% NEQ 0 ( echo [ERROR] Gagal pada Modul 04 & pause & exit /b )

echo.
echo [4/5] Modul 05: Menghasilkan visualisasi Explainable AI (SHAP)...
"%PY_CMD%" scripts\05_explainable_ai_shap.py
if %ERRORLEVEL% NEQ 0 ( echo [ERROR] Gagal pada Modul 05 & pause & exit /b )

echo.
echo [5/5] Modul 06: Menerbitkan laporan audit kualitas dataset...
"%PY_CMD%" scripts\06_validate_and_report.py
if %ERRORLEVEL% NEQ 0 ( echo [ERROR] Gagal pada Modul 06 & pause & exit /b )

echo.
echo ===============================================================================
echo  [SUKSES] Seluruh pipeline berhasil dieksekusi tanpa kendala!
echo  Untuk membuka Web Dashboard interaktif, jalankan: run_app.bat
echo ===============================================================================
echo.
pause
