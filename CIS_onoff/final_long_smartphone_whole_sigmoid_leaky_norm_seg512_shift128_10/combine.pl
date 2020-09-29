#!/usr/bin/perl

#### get all training individual average;
open REF, "../../../rawdata/cis-pd.data_labels/CIS-PD_Training_Data_IDs_Labels.csv" or die;
while ($line=<REF>){
    chomp $line;
    @table=split ",", $line;
    if ($table[2] eq 'NA'){}else{
	    $count{$table[1]}++;
	    $sum{$table[1]}+=$table[2];
		$sum_all+=$table[2];
		$count_all++;

		if (exists $max{$table[1]}){
			if ($table[2]>$max{$table[1]}){
				$max{$table[1]}=$table[2];
			}
		}else{
				$max{$table[1]}=$table[2];
		}
		if (exists $min{$table[1]}){
			if ($table[2]<$min{$table[1]}){
				$min{$table[1]}=$table[2];
			}
		}else{
				$min{$table[1]}=$table[2];
		}
    }
}


@all=glob "*.test.dat";

foreach $file (@all){
    open FILE, "$file" or die;
    $prediction=$file;
    $prediction=~s/test/prediction/g;
    if ($file=~/all/){
        open PRED, "$prediction" or die;
        while ($line=<FILE>){
            $pred=<PRED>;
            chomp $line;
            @t=split "\t", $line;
		@t=split '/', $t[1];
		@t=split '.csv', $t[-1];
		@t=split '_', $t[0];
            chomp $pred;
		print "$t[1]\n";
            $ref_all{$t[1]}+=$pred;
            $count_all{$t[1]}++;
        }
        close PRED;
        close FILE;
    }else{
        if (-e $prediction){
		## get all average;
		$sum_tmp=0;
		$count_tmp=0;
		open PRED, "$prediction" or die;
		while ($line=<PRED>){
			chomp $line;
			$count_tmp++;
			$sum_tmp+=$line;
		}
		close PRED;
		@t=split '.prediction', $prediction;
		$ind=$t[0];
		$diff=$sum_tmp/$count_tmp-$sum{$ind}/$count{$ind};
        $diff=0;
		open PRED, "$prediction" or die;
		while ($line=<FILE>){
            $pred=<PRED>;
            chomp $line;
            @t=split "\t", $line;
		@t=split '/', $t[1];
		@t=split '.csv', $t[-1];
		@t=split '_', $t[0];
            chomp $pred;
		$val=$pred-$diff;
		#if ($val >$max{$ind}){
		#	$val=$max{$ind};
		#}
		#if ($val <$min{$ind}){
		#	$val=$min{$ind};
		#}
            $ref{$t[1]}+=$val;
            $count{$t[1]}++;
        }
        close PRED;
        close FILE;
        }
    }
}

open TEST, "test_gs.dat" or die;
open NEWEXIST, ">test_gs.dat.exist" or die;
open PRED, ">prediction.dat" or die;
open PREDEXIST, ">prediction.dat.exist" or die;
while ($line=<TEST>){
    chomp $line;
    @table=split "\t", $line;
   # print "$table[1]\t$ref_all{$table[1]}\n";
    if (exists $ref{$table[1]}){
	
        $vvv=$ref{$table[1]}/$count{$table[1]};
        print PRED "$vvv\n";
        print PREDEXIST "$vvv\n";
        print NEWEXIST "$line\n";
        print "yes\n";
    }else{
        if (exists $count{$table[2]}){
            $val=$sum{$table[2]}/$count{$table[2]};
            print PRED "$val\n";
        }elsif(exists $count_all{$table[1]}){
            $vvv=$ref_all{$table[1]}/$count_all{$table[1]};
		    print PRED "$vvv\n";
		    print "no\n";
        }else{
            $vvv=$sum_all/$count_all;
            print PRED "$vvv\n";
	}
    }
}
close TEST;
close PRED;


