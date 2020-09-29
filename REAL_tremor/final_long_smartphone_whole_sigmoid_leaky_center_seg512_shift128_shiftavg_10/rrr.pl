$i=0;
while ($i<100){
open FILE, "$ARGV[0]" or die;

open NEW, ">bbb" or die;
while ($line=<FILE>){
    chomp $line;
    $r=rand();
    if ($r<0.01){
        print NEW "$line\n";
    }

}
system "perl ~/source/data_stat/sd.pl bbb 1";
$i++;
}
