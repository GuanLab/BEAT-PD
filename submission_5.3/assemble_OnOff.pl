#!/usr/bin/perl

open REF, "../CIS_onoff/assemble_v5.2/assembled_prediction.dat" or die;
while ($line=<REF>){
	chomp $line;
	@table=split "\t", $line;

	$ref{$table[0]}=$table[1];
}
close REF;

open REF, "../REAL_onoff/assemble_5.2/assembled_prediction.dat" or die;
while ($line=<REF>){
	chomp $line;
	@table=split "\t", $line;
	$ref{$table[0]}=$table[1];
}
close REF;

open REF, "BEAT-PD_SC1_OnOff_Submission_Template.csv" or die;
open SUB, ">v5.2_BEAT-PD_SC1_OnOff_Submission.csv" or die;
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
