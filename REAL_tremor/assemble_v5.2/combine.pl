#!/usr/bin/perl

@all=glob "../final_long_smartwatch*/prediction.dat.exist";
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
        $exists{$table[1]}=1;
    }
    close REF;
    close PRED;

}

        
@all=glob "../final_long_smartphone*/prediction.dat.exist";
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
        if (exists $sum{$table[1]}){
#            print "excluded\n";
            }else{
            $sum{$table[1]}+=$pred;
            $count{$table[1]}++;
        }
    }
    close REF;
    close PRED;

}

open NEW, ">assembled_prediction.dat" or die;
@all_id=keys %sum;
foreach $id (@all_id){
    print NEW "$id\t";
    $val=$sum{$id}/$count{$id};
    print "$count{$id}\n";
    print NEW "$val\t";
    if (exists $exists{$id}){
        print NEW "smartwatch\n";
    }else{
        print NEW "smartphone\n";
    }
    
}
close NEW;

        
