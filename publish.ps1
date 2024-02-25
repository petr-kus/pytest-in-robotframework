Remove-Item -Path dist\* -Recurse -Force
python setup.py sdist bdist_wheel
twine upload dist/*

#This could be done by more tools. One is Poetry.