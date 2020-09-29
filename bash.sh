#!/bin/bash

. activate tensorflow_p36

pip install scikit-image

pip install scipy

## preprocessing CIS training
cp preprocessing/CIS/split_training_512_shift128.pl ../rawdata/
cd ../rawdata/
perl split_training_512_shift128.pl
cd ../round5_submission_3_reproduce/


## preprocessing CIS testing
cp preprocessing/CIS/test/split_training_512_shift128.pl ../testdata/ ## recheck, this piece is currently missing
cd ../testdata/
perl split_training_512_shift128.pl
cd ../round5_submission_3_reproduce/

## preprocessing REAL training
cp preprocessing/REAL/*pl ../rawdata_new/real-pd.training_dat/
cp preprocessing/REAL/*py ../rawdata_new/real-pd.training_dat/ 
cd ../rawdata_new/real-pd.training_dat/
python process_smartwatch_accelerometer_firsttrack.py
python process_smartwatch_gyroscope_firsttrack.py
perl split_training_512_shift128_smartwatch_gyroscope.pl
perl split_training_512_shift128_smartwatch.pl
perl split_training_1024_shift128.pl
perl split_training_smartwatch_1024_shift128.pl
perl split_training_512_shift128.pl
perl split_training_smartwatch_gyroscope_1024_shift128.pl
cd ../../round5_submission_3_reproduce/


## preprocessing REAL testing
cp preprocessing/REAL/test/*pl ../testdata_new/real-testing_data/
cp preprocessing/REAL/test/*py ../testdata_new/real-testing_data/
cd ../testdata_new/real-testing_data/
python process_smartwatch_accelerometer_firsttrack.py
python process_smartwatch_gyroscope_firsttrack.py
perl split_training_512_shift128_smartwatch_gyroscope.pl
perl split_training_512_shift128_smartwatch.pl
perl split_training_1024_shift128.pl
perl split_training_smartwatch_1024_shift128.pl
perl split_training_512_shift128.pl
perl split_training_smartwatch_gyroscope_1024_shift128.pl
cd ../../round5_submission_3_reproduce/

## now start the training, 8 as one group as we have 8 GPUs

cd CIS_dyskinesia/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_20_unfinished/
CUDA_VISIBLE_DEVICES=0 sh bash.sh 0 &
cd ../../

cd CIS_onoff/final_long_smartphone_whole_sigmoid_leaky_center_seg512_shift128_10/
CUDA_VISIBLE_DEVICES=1 sh bash.sh 0 &
cd ../../

cd CIS_onoff/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_10
CUDA_VISIBLE_DEVICES=2 sh bash.sh 0 &
cd ../../

cd CIS_onoff/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_10_augtest/
CUDA_VISIBLE_DEVICES=3 sh bash.sh 0 &
cd ../../

cd CIS_tremor/final_long_smartphone_whole_sigmoid_leaky_center_seg512_shift128_10/
CUDA_VISIBLE_DEVICES=4 sh bash.sh 0 &
cd ../../

cd CIS_tremor/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_10/
CUDA_VISIBLE_DEVICES=5 sh bash.sh 0 &
cd ../../

cd CIS_tremor/final_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_10_augtest/
CUDA_VISIBLE_DEVICES=6 sh bash.sh 0 &
cd ../../

cd REAL_dyskinesia/final_long_smartphone_whole_sigmoid_leaky_norm_seg1024_shift128/
CUDA_VISIBLE_DEVICES=7 sh bash.sh 0 &
cd ../../

wait;

### next 8 batch will be much faster since we have few examples for REAL
cd ./REAL_dyskinesia/final_long_smartphone_whole_sigmoid_leaky_norm_seg1024_shift128_5/
CUDA_VISIBLE_DEVICES=0 sh bash.sh 0 &
cd ../../

cd REAL_dyskinesia/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128/
CUDA_VISIBLE_DEVICES=1 sh bash.sh 0 &
cd ../../


cd REAL_dyskinesia/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_10/
CUDA_VISIBLE_DEVICES=2 sh bash.sh 0 &
cd ../../

cd REAL_dyskinesia/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_10_testaug/
CUDA_VISIBLE_DEVICES=3 sh bash.sh 0 &
cd ../../

cd REAL_dyskinesia/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_20/
CUDA_VISIBLE_DEVICES=4 sh bash.sh 0 &
cd ../../

cd REAL_dyskinesia/final_long_smartwatch_gyroscope_whole_sigmoid_leaky_norm_seg512_split128/
CUDA_VISIBLE_DEVICES=5 sh bash.sh 0 &
cd ../../


cd REAL_onoff/final_long_smartphone_whole_sigmoid_leaky_center_seg512_shift128_shiftavg_10/
CUDA_VISIBLE_DEVICES=6 sh bash.sh 0 &
cd ../../

cd REAL_onoff/final_long_smartphone_whole_sigmoid_leaky_center_seg512_shift128_shiftavg_10_testaug/
CUDA_VISIBLE_DEVICES=7 sh bash.sh 0 &
cd ../../

wait;

### now we start the last 8 jobs which will be very very fast. 

cd REAL_onoff/final_long_smartwatch_whole_sigmoid_leaky_center_seg512_shift128/
CUDA_VISIBLE_DEVICES=0 sh bash.sh 0 &
cd ../../

cd REAL_onoff/final_long_smartwatch_whole_sigmoid_leaky_norm_seg512_shift128/
CUDA_VISIBLE_DEVICES=1 sh bash.sh 0 &
cd ../../

cd REAL_tremor/final_long_smartphone_whole_sigmoid_leaky_center_seg512_shift128_shiftavg_10/
CUDA_VISIBLE_DEVICES=2 sh bash.sh 0 &
cd ../../

cd REAL_tremor/final_long_smartwatch_gyroscope_whole_sigmoid_leaky_seg512_split128_10/
CUDA_VISIBLE_DEVICES=3 sh bash.sh 0 &
cd ../../

wait;

### now we ansemble the result

cd CIS_onoff/assemble_v5.2/
perl combine.pl
cd ../../

cd CIS_tremor/assemble_v5.3/
perl combine.pl
perl combine_exist.pl
cd ../../

cd REAL_dyskinesia/assemble_v5.2/
perl combine.pl
cd ../../

cd REAL_onoff/assemble_5.2/
perl combine.pl
cd ../../

cd REAL_tremor/assemble_v5.2/
perl combine.pl
cd ../../


cd  submission_5.3

perl assemble_dyskinesia.pl  
perl assemble_OnOff.pl  
perl assemble_tremor.pl

