#!/usr/bin/perl
#
system "rm -rf smartwatch_accelerometer_firsttrack_split_512_shift_128";
system "mkdir smartwatch_accelerometer_firsttrack_split_512_shift_128";
@data=glob "smartwatch_accelerometer_firsttrack/*";
foreach $file (@data){
	@t=split "/", $file;
	$file_i=0;
	$line_i=0;
	$string='';
	open FILE, "$file" or die;
	$title_line=<FILE>;
	while ($line=<FILE>){
		if (($line_i%512)==511){
			open NEW, ">smartwatch_accelerometer_firsttrack_split_512_shift_128/${file_i}_$t[-1]" or die;
			print NEW "$title_line";
			print NEW "$string";
			$string='';
			$string=$string.$line;
			$file_i++;
		}else{
			$string=$string.$line;
		}
		$line_i++;
	}
	close FILE;

	### shift 128
	$string='';
	open FILE, "$file" or die;
	$title_line=<FILE>;
	$line_i=0;
	$line_ii=0;
	while ($line=<FILE>){
		if ($line_ii>128){
			if (($line_i%512)==511){
                print "smartwatch_accelerometer_firsttrack_split_512_shift_128/${file_i}_$t[-1]\n";
				open NEW, ">smartwatch_accelerometer_firsttrack_split_512_shift_128/${file_i}_$t[-1]" or die;
				print NEW "$title_line";
				print NEW "$string";
				$string='';
				$string=$string.$line;
				$file_i++;
			}else{
				$string=$string.$line;
			}
			$line_i++;
		}
		$line_ii++;
	}
	close FILE;

	### shift 256
	$string='';
	open FILE, "$file" or die;
	$title_line=<FILE>;
	$line_i=0;
	$line_ii=0;
	while ($line=<FILE>){
		if ($line_ii>256){
			if (($line_i%512)==511){
				open NEW, ">smartwatch_accelerometer_firsttrack_split_512_shift_128/${file_i}_$t[-1]" or die;
				print NEW "$title_line";
				print NEW "$string";
				$string='';
				$string=$string.$line;
				$file_i++;
			}else{
				$string=$string.$line;
			}
			$line_i++;
		}
		$line_ii++;
	}
	close FILE;
	### shift 384
	$string='';
	open FILE, "$file" or die;
	$title_line=<FILE>;
	$line_i=0;
	$line_ii=0;
	while ($line=<FILE>){
		if ($line_ii>384){
			if (($line_i%512)==511){
				open NEW, ">smartwatch_accelerometer_firsttrack_split_512_shift_128/${file_i}_$t[-1]" or die;
				print NEW "$title_line";
				print NEW "$string";
				$string='';
				$string=$string.$line;
				$file_i++;
			}else{
				$string=$string.$line;
			}
			$line_i++;
		}
		$line_ii++;
	}
	close FILE;


}
