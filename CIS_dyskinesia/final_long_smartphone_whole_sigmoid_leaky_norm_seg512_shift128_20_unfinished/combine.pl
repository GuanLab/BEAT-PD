#!/usr/bin/perl

#### get all training individual average;
open REF, "train_gs.dat" or die;
while ($line=<REF>){
    chomp $line;
    @table=split "\t", $line;
    $count{$table[2]}++;
    $sum{$table[2]}+=$table[0];
}
close REF;



@all=glob "*.test.dat";

foreach $file (@all){
    open FILE, "$file" or die;
    $prediction=$file;
    $prediction=~s/test/prediction/g;
    if ($file=~/all/){
        #open PRED, "$prediction" or die;
        while ($line=<FILE>){
            $pred=<PRED>;
            chomp $line;
            @t=split "\t", $line;
		@t=split '/', $t[1];
		@t=split '.csv', $t[-1];
		@t=split '_', $t[0];
            chomp $pred;
		#print "$t[1]\n";
            $ref_all{$t[1]}+=$pred;
            $count_all{$t[1]}++;
        }
        close PRED;
        close FILE;
    }else{
        if (-e $prediction){
        open PRED, "$prediction" or die;
        while ($line=<FILE>){
            $pred=<PRED>;
            chomp $line;
            @t=split "\t", $line;
		@t=split '/', $t[1];
		@t=split '.csv', $t[-1];
		@t=split '_', $t[0];
            chomp $pred;
            $ref{$t[1]}+=$pred;
            $count{$t[1]}++;
        }
        close PRED;
        close FILE;
        }
    }
}

open TEST, "test_gs.dat" or die;
open TESTNEW, ">test_gs.dat.exist" or die;

open PRED, ">prediction.dat" or die;
open PREDNEW, ">prediction.dat.exist" or die;
while ($line=<TEST>){
    chomp $line;
    @table=split "\t", $line;
   # print "$table[1]\t$ref_all{$table[1]}\n";
    if (exists $ref{$table[1]}){
	
	$vvv=$ref{$table[1]}/$count{$table[1]};
        print PRED "$vvv\n";
        print TESTNEW "$line\n";
        print PREDNEW "$vvv\n";
        #print "yes\n";
    }else{
        if (exists $count{$table[2]}){
            $val=$sum{$table[2]}/$count{$table[2]};
            print PRED "$val\n";
        }else{
		$vvv=$ref_all{$table[1]}/$count_all{$table[1]};
		print PRED "$vvv\n";
            #print "no\n";
        }
    }
}
close TEST;
close PRED;


