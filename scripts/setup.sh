root_path=""
if [ -f README.md ] 
then
    echo "We are in root directory"
    root_path=$(echo $(pwd))
else
    echo "[Error] Script Must be run from project root directory"
    exit
fi


NO_OF_ROWS_IN_DATA=10000
if [-z $1]
then
    NO_OF_ROWS_IN_DATA=10000
else
    NO_OF_ROWS_IN_DATA=$1
fi

pip install -r "${root_path}/scripts/requirments.txt"
cd "${root_path}/py_script"
python data-prep.py $NO_OF_ROWS_IN_DATA