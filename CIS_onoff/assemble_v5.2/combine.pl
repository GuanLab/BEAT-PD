#!/usr/bin/perl

@all=glob "../final_*/prediction.dat.exist";
foreach $file (@all){
    open PRED, "$file" or die;
    $ref=$file;
    $ref=~s/prediction/test_gs/g;
    open REF, "$ref" or die;
    while ($line=<REF>){
        chomp $line;
        @table=split "\t", $line;
        $pred=<PRED>;
        chomp $pred;
        $sum{$table[1]}+=$pred;
        $count{$table[1]}++;
    }
    close REF;
    close PRED;

}

        

open NEW, ">assembled_prediction.dat" or die;
@all_id=keys %sum;
foreach $id (@all_id){
    print NEW "$id\t";
    print "$count{$id}\n";
    $val=$sum{$id}/$count{$id};
    print NEW "$val\n";
    
}
close NEW;

        
