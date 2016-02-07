#!/usr/bin/env perl
#
#

use strict;
use warnings;
use DBI;

my $asn;
$asn = $ARGV[0] if(scalar(@ARGV) >= 1);

my $hostname = "localhost";
my $user = "read";
my $password = "read";
my $database = "ASRank";
my $dsn = "DBI:mysql:database=$database;host=$hostname";
my $dbh = DBI->connect($dsn, $user, $password);

my $query = "select CustomerPrefixCone.as1," .
    " CustomerPrefixCone.startdate, CustomerPrefixCone.enddate," .
    " PrefixGeo.geo, PrefixGeo.sum" .
    " from CustomerPrefixCone, PrefixGeo" .
    " where CustomerPrefixCone.prefix=PrefixGeo.prefix";
$query .= " and CustomerPrefixCone.as1=?" if(defined($asn));

my $sth = $dbh->prepare($query);

if(defined($asn))
{
    $sth->execute($asn);
}
else
{
    $sth->execute();
}

sub daterange($$)
{
    my ($start, $end) = @_;
    my ($start_yyyy, $start_mm) = ($1, $2) if($start =~ /^(\d{4})(\d{2})/);
    my ($end_yyyy, $end_mm) = ($1, $2) if($end =~ /^(\d{4})(\d{2})/);
    my @vals;

    if($start_yyyy == $end_yyyy)
    {
	foreach my $mm ($start_mm .. $end_mm)
	{
	    my $date = sprintf("%4d%02d01", $start_yyyy, $mm);
	    push @vals, $date;
	}
	return @vals;
    }

    foreach my $mm ($start_mm .. 12)
    {
	my $date = sprintf("%4d%02d01", $start_yyyy, $mm);
	push @vals, $date;
    }
    foreach my $yyyy ($start_yyyy+1 .. $end_yyyy-1)
    {
	foreach my $mm (1 .. 12)
	{
	    my $date = sprintf("%4d%02d01", $yyyy, $mm);
	    push @vals, $date;
	}
    }
    foreach my $mm (1 .. $end_mm)
    {
	my $date = sprintf("%4d%02d01", $end_yyyy, $mm);
	push @vals, $date;
    }
    return @vals;
}

my %data;
my ($as1, $startdate, $enddate, $geo, $sum);
while(($as1, $startdate, $enddate, $geo, $sum) = $sth->fetchrow_array)
{
    $enddate = "20160101" if(!defined($enddate));
    my @dates = daterange($startdate, $enddate);
    foreach my $date (@dates)
    {
	$data{$as1}{$date}{$geo} += $sum;
    }
}
$sth->finish;
$dbh->disconnect;

foreach my $asn (sort {$a <=> $b} keys %data)
{
    foreach my $date (keys %{$data{$asn}})
    {
	foreach my $geo (keys %{$data{$asn}{$date}})
	{
	    print "$asn $date $geo $data{$asn}{$date}{$geo}\n";
	}
    }
}

exit 0;
