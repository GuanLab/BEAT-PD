#!/usr/bin/perl
#
## adjust by person if exists;
open REF, "train_gs.dat" or die;
while ($line=<REF>){
	chomp $line;
	@table=split "\t", $line;
	$sum{$table[2]}+=$table[0];
	$count{$table[2]}++;
}
close REF;

open PRED, "prediction.dat" or die;
open REF, "test_gs.dat" or die;
while ($line=<REF>){
	chomp $line;
	@table=split "\t", $line;
	$pred=<PRED>;
	chomp $pred;
	$sum_pred{$table[2]}+=$pred;
	$count_pred{$table[2]}++;
}
close PRED;
close REF;


open REF, "test_gs.dat" or die;
open PRED, "prediction.dat" or die;
open NEW, ">prediction.dat.adjustper" or die;
while ($line=<REF>){
	chomp $line;
	@table=split "\t", $line;
	$pred=<PRED>;
	chomp $pred;
	if (exists $count{$table[2]}){
		$pred=$pred+$sum{$table[2]}/$count{$table[2]}-$sum_pred{$table[2]}/$count_pred{$table[2]};
	}
	print NEW "$pred\n";

}
close PRED;
close REF;
