#!/usr/bin/perl

@all=glob "*.train.dat";
foreach $file (@all){
    system "python train_lightgbm.py $file &";
}
