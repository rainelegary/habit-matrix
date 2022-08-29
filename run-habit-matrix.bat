@echo off
set RUN_MODE="app"
::set YAML_DIR="C:/Users/Raine/OneDrive/Desktop/math_and_coding/project-related files/habit matrix/YAML/"
set YAML_DIR="C:/Users/Raine/OneDrive/Desktop/math_and_coding/projects/habit-matrix/DataManagement/DataYAML/"

TITLE habit matrix

call conda activate base
"C:\Users\Raine\anaconda3\python.exe" "C:\Users\Raine\OneDrive\Desktop\math_and_coding\projects\habit-matrix\main.py" %RUN_MODE% %YAML_DIR%
call conda deactivate

PAUSE