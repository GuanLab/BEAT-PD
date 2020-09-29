#!/bin/bash

python3 split.py ${1}

python map_id.py
python split_test.py ../../../testdata/cis-testing_data_split_512_shift_128/
python split_train.py ../../../rawdata/cis-pd.training_data_split_512_shift_128/

rm *finalized_model.sav
rm *prediction.dat
for file in *.train.dat

do
    rm weight*
    python train_deeplearning.py ${file} ./ 0
    python train_deeplearning.py ${file} ./ 1
    python train_deeplearning.py ${file} ./ 2
    python train_deeplearning.py ${file} ./ 3
    python train_deeplearning.py ${file} ./ 4
    rm prediction.dat*
    python predict_deeplearning.py ${file} ./
    perl combine_ind.pl ${file}

done

wait

perl combine.pl

perl ~/source/data_stat/cor_column.pl prediction.dat 1 test_gs.dat 1 >>cor_all.txt
perl ~/source/data_stat/rmse_column.pl prediction.dat 1 test_gs.dat 1 >>rmse_all.txt
perl weighted_mse.pl prediction.dat test_gs.dat >>mse_all.txt
