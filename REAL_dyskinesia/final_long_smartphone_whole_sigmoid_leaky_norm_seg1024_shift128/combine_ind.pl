#!/usr/bin/perl

$file=$ARGV[0];
$max=-100;
$min=100;
open FILE, "$file" or die;
while ($line=<FILE>){
    chomp $line;
    @table=split "\t", $line;
    if ($table[0]>$max){
        $max=$table[0];
    }
    if ($table[0]<$min){
        $min=$table[0];
    }
}
@all=glob "prediction*h5";
foreach $file (@all){
    open FILE, "$file" or die;
    $i=0;
    while ($line=<FILE>){
        chomp $line;
        if ($line>$max){
            $line=$max;
        }
        if ($line<$min){
            $line=$min;
        }
        $ref[$i]+=$line;
        $count[$i]++;
        $i++;
    }
}

$file=$ARGV[0];
$file=~s/train/prediction/g;
open NEW, ">$file" or die;
$imax=$i;
print "$i\n";
$i=0;
while ($i<$imax){
    $val=$ref[$i]/$count[$i];
    print NEW "$val\n";
    $i++;
}
close NEW;

