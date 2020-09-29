#!/usr/bin/perl

open REF, "../CIS_dyskinesia/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_20_unfinished/test_gs.dat.exist" or die;
open PRED, "../CIS_dyskinesia/final_long_smartphone_whole_sigmoid_leaky_norm_seg512_shift128_20_unfinished/prediction.dat.exist" or die;
while ($ref=<REF>){
	chomp $ref;
	@table=split "\t", $ref;

	$pred=<PRED>;
	chomp $pred;
	$ref{$table[1]}=$pred;
}
close REF;
close PRED;

open REF, "../REAL_dyskinesia/assemble_v5.2/assembled_prediction.dat" or die;
while ($ref=<REF>){
	chomp $ref;
	@table=split "\t", $ref;
	$ref{$table[0]}=$table[1];
}
close REF;
close PRED;

open REF, "BEAT-PD_SC2_Dyskinesia_Submission_Template.csv" or die;
open SUB, ">v5.2_BEAT-PD_SC2_Dyskinesia_Submission.csv" or die;
$line=<REF>;
print SUB "$line";
while ($line=<REF>){
	chomp $line;
	@table=split ",", $line;
	print SUB "$table[0],";
	print SUB "$ref{$table[0]}\n";
}
close REF;
close SUB;
