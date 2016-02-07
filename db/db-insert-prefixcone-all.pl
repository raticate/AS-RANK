#!/usr/bin/env perl

use strict;
use warnings;

my @years = (1998 .. 2009);
my @months = (1 .. 12);

my @dates;
foreach my $y (@years)
{
    foreach my $m (@months)
    {
        push @dates, sprintf("%4d%02d01", $y, $m);
    }
}

foreach my $date (@dates)
{
    next if($date eq "19980101" || $date eq "19980201" || $date eq "19980301");
    next if(!-r "$date.ppdc-prefix.txt.bz2");
    my $cmd = "./db-insert-prefixcone.pl $date.ppdc-prefix.txt.bz2";
    system("$cmd");
}

exit 0;
