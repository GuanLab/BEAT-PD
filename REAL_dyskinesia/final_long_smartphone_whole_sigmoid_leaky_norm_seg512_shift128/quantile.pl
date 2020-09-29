#!/usr/bin/perl

# get average of train_gs.dat

@ref=();
open FILE, "train_gs.dat" or die;
while ($line=<FILE>){
    chomp $line;
    @table=split "\t", $line;
    push @ref, $table[0];
    $count++;
}
close FILE;

@ref_pred=();
open FILE, "prediction.dat" or die;
while ($line=<FILE>){
    chomp $line;
    push @ref_pred, $line;
    $count_pred++;
}
close FILE;

@ref=sort{$a<=>$b}@ref;
@ref_pred=sort{$a<=>$b}@ref_pred;

### create mapping;
$i=0;
foreach $pred (@ref_pred){
    $map{$pred}=$ref[int($i*$count/$count_pred)];
    $i++;
}


open FILE, "prediction.dat" or die;
open NEW, ">prediction.dat.quantile" or die;
while ($line=<FILE>){
    chomp $line;
    $line=$map{$line};
    
    print NEW "$line\n";
}
close FILE;

