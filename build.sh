rm -rf ./dist/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
pip3 install --upgrade pygenal
