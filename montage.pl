#!/usr/bin/perl

use v5.38;

my $end = 295;
my $chunk = 24;

my $i = 0;
my $out_count = 0;
while ($i <= $end) {
    my $buf = "montage";
    for (my $j = $i; $j < $i + $chunk; $j++) {
	my $file = sprintf "mol%02d.png", $j;
	if (-e $file) {
	    $buf .= " " . $file;
	}
    }
    $buf .= sprintf " -geometry 450x450\\>+4+6 out%02d.png", $out_count;
    say $buf;
    0 == system($buf) || die $!;
    $i += $chunk;
    $out_count += 1;
}
