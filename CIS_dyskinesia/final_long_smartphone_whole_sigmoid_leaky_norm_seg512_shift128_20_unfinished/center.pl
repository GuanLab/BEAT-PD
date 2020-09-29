#!/usr/bin/perl

# get average of train_gs.dat

open FILE, "train_gs.dat" or die;
while ($line=<FILE>){
    chomp $line;
    @table=split "\t", $line;
    $sum+=$table[0];
    $count++;
}
close FILE;

$avg=$sum/$count;

open FILE, "prediction.dat" or die;
while ($line=<FILE>){
    chomp $line;
    $sum_pred+=$line;
    $count_pred++;
}
close FILE;
$avg_pred=$sum_pred/$count_pred;


open FILE, "prediction.dat" or die;
open NEW, ">prediction.dat.center" or die;
while ($line=<FILE>){
    chomp $line;
    $line=$line-$avg_pred+$avg;
    if ($line<0){
        $line=0;
    }
    if ($line>3){
        $line=3;
    }
    print NEW "$line\n";
}
close FILE;

