@echo off
set RUN_MODE="app"
set WORKING_DIR="C:/Users/Raine/OneDrive/Desktop/math_and_coding/projects/habit-matrix/"

TITLE habit matrix

call conda activate base
"C:\Users\Raine\anaconda3\python.exe" "C:\Users\Raine\OneDrive\Desktop\math_and_coding\projects\habit-matrix\main.py" %RUN_MODE% %WORKING_DIR%
call conda deactivate

PAUSE