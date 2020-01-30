#! /bin/bash

# 这里我使用的是 conda 进行包管理，可以进行适当的修改
export PATH="/home/idwangmo/.minicoda3/bin:$PATH"

eval "$(conda shell.bash hook)"

conda activate nCov

cd /home/idwangmo/nCoV || exit

scrapy crawl ncov
scrapy crawl 2019ncov