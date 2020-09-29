#!/usr/bin/perl

@all=glob "*.train.dat";
foreach $file (@all){
    $testfile=$file;
    $testfile=~s/train/test/g;
    if (-e $testfile){
        system "python test_lightgbm.py $testfile";
    }
}
