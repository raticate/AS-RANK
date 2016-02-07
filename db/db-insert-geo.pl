#!/usr/bin/env perl

use strict;
use warnings;
use DBI;

my ($file) = @ARGV;
if(scalar(@ARGV) != 1)
{
    print STDERR "usage: db-insert-geo.pl \$file\n";
    exit -1;
}

my %data;

open(GEO, "zcat $file |") or die "could not open $file";
while(<GEO>)
{
    chomp;
    my @bits = split(/\|/); next if(scalar(@bits) != 15);
    my $pref = $bits[0];
    my $cnt = $bits[1];
    my $region = $1 if($bits[14] =~ /^(\d+),/);
    next if(!defined($pref) || !defined($cnt) || !defined($region));
    $data{$pref}{$region} += $cnt;
}
close GEO;

my $hostname = "localhost";
my $user = "root";
my $password = "root";
my $database = "ASRank";
my $dsn = "DBI:mysql:database=$database;host=$hostname";
my $dbh = DBI->connect($dsn, $user, $password);

$dbh->do("create table if not exists PrefixGeo(" .
	 " id SERIAL," .
	 " prefix text not null," .
	 " sum int not null," .
	 " geo int not null)");

$dbh->begin_work;
my $sth = $dbh->prepare("insert into PrefixGeo(prefix,geo,sum) values(?,?,?)");
foreach my $pref (keys %data)
{
    foreach my $geo (keys %{$data{$pref}})
    {
	$sth->execute($pref, $geo, $data{$pref}{$geo});
    }
}
$sth->finish;
$dbh->commit;
$dbh->disconnect;
exit 0;
