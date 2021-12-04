SET log_file=%cd%\logfile.txt
call C:\Users\Lenovo\miniconda3\condabin\activate.bat NFL
cd C:\Users\Lenovo\Documents\VSCode_Tests\NFL
python run.py
call C:\Users\Lenovo\miniconda3\condabin\activate.bat NFL3
python Dynasty_Sandwich\visualize_excel.py
git add .
git commit -m "dailyUpdate"
git push
pause