#!/usr/bin/env perl

use strict;
use warnings;
use DBI;

my $hostname = "localhost";
my $user = "root";
my $password = "root";
my $database = "ASRank";
my $dsn = "DBI:mysql:database=$database;host=$hostname";
my $dbh = DBI->connect($dsn, $user, $password);

my $sth = $dbh->prepare("select as1, prefix, startdate, enddate" .
			" from CustomerPrefixCone order by as1,prefix,startdate");
$sth->execute;

my ($as1, $prefix, $startdate, $enddate);
while(($as1, $prefix, $startdate, $enddate) = $sth->fetchrow_array)
{
    print "$as1 $prefix $startdate";
    print " $enddate" if(defined($enddate));
    print "\n";
}
$sth->finish;

$dbh->disconnect;
