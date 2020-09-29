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

## find out sd
$sd=0;
open FILE, "train_gs.dat" or die;
while ($line=<FILE>){
    chomp $line;
    @table=split "\t", $line;
    $sd+=($table[0]-$avg)*($table[0]-$avg);

}
close FILE;
$sd=sqrt($sd/$count);

open FILE, "prediction.dat" or die;
while ($line=<FILE>){
    chomp $line;
    $sum_pred+=$line;
    $count_pred++;
}
close FILE;
$avg_pred=$sum_pred/$count_pred;

$sd_pred=0;
open FILE, "prediction.dat" or die;
while ($line=<FILE>){
    chomp $line;
    $sd_pred+=($line-$avg_pred)*($line-$avg_pred);
}
close FILE;
$sd_pred=sqrt($sd_pred/$count_pred);

open FILE, "prediction.dat" or die;
open NEW, ">prediction.dat.norm" or die;
while ($line=<FILE>){
    chomp $line;
    $line=($line-$avg_pred)/$sd_pred*$sd+$avg;
    if ($line<0){
        $line=0;
    }
    if ($line>3){
        $line=3;
    }
    print NEW "$line\n";
}
close FILE;

