#
if ! [ -d "data" ]
then
  mkdir data
fi

if ! [ -d "data/raw" ]
then
  mkdir data/raw
fi

python crawl_investing_forum.py

