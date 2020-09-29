#!/usr/bin/perl

open REF, "../CIS_tremor/assemble_v5.3/assembled_prediction.dat" or die;
while ($ref=<REF>){
	chomp $ref;
	@table=split "\t", $ref;

	$ref{$table[0]}=$table[1];
}
close REF;
close PRED;

open REF, "../REAL_tremor/assemble_v5.2/assembled_prediction.dat" or die;
while ($ref=<REF>){
	chomp $ref;
	@table=split "\t", $ref;

	$ref{$table[0]}=$table[1];
}
close REF;
close PRED;


open REF, "BEAT-PD_SC3_Tremor_Submission_Template.csv" or die;
open SUB, ">v5.3_BEAT-PD_SC3_Tremor_Submission.csv" or die;
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
