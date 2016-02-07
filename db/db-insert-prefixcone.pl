#!/usr/bin/env perl

use strict;
use warnings;
use DBI;

if(scalar(@ARGV) != 1)
{
    print STDERR "usage: db-insert-prefixcone.pl \$pfxcone\n";
    exit -1;
}

my ($pfxcone) = @ARGV;
my $date;

if($pfxcone =~ /(\d{8})/)
{
    $date = $1;
}
else
{
    print STDERR "unknown date for $pfxcone\n";
    exit -1;
}

my $hostname = "192.168.142.118";
my $user = "hackaton";
my $password = "password";
my $database = "ASRank1";
my $dsn = "DBI:mysql:database=$database;host=$hostname";
my $dbh = DBI->connect($dsn, $user, $password);

#$dbh->do("drop table prefixcone");

$dbh->do("create table if not exists prefixcone(" .
	 " id SERIAL," .
	 " ipversion int not null," .
	 " as1 int not null," .
	 " prefix text not null," .
	 " startdate int null," .
	 " enddate int null)");

my %data;
my $sth = $dbh->prepare("select id, as1, prefix, startdate from PrefixCone where enddate is null and ipversion=4");
$sth->execute;

my %indb;
my ($id, $as1, $prefix, $startdate);
while(($id, $as1, $prefix, $startdate) = $sth->fetchrow_array)
{
    $indb{$as1}{$prefix}{id} = $id;
    $indb{$as1}{$prefix}{seen} = 0;
}
$sth->finish;

my %newdb;

if($pfxcone =~ /\.bz2$/)
{
    open(PFXCONE, "bzcat $pfxcone |") or die "could not open $pfxcone";
}
else
{
    open(PFXCONE, $pfxcone) or die "could not open $pfxcone";
}
while(<PFXCONE>)
{
    next if(/^#/);
    chomp;
    my ($as, @prefixes) = split(/\s+/);

    foreach my $pref (@prefixes)
    {
	if(defined($indb{$as}{$pref}))
	{
	    $indb{$as}{$pref}{seen} = 1;
	}
	else
	{
	    push @{$newdb{$as}}, $pref;
	}
    }
}
close PFXCONE;

$dbh->begin_work;
$sth = $dbh->prepare("update PrefixCone set enddate=? where id=?");
foreach my $as (sort {$a <=> $b} keys %indb)
{
    foreach my $pref (keys %{$indb{$as}})
    {
	next if($indb{$as}{$pref}{seen} == 1);
	print "$as $pref end $date\n";
	$sth->execute($date, $indb{$as}{$pref}{id});
    }
}
$sth->finish;
$dbh->commit;

$dbh->begin_work;
$sth = $dbh->prepare("insert into PrefixCone(IPversion, AS1, Prefix, startdate) values(4,?,?,?)");
foreach my $as (sort {$a <=> $b} keys %newdb)
{
    foreach my $pref (@{$newdb{$as}})
    {
	print "$as $pref start $date\n";
	$sth->execute($as, $pref, $date);
    }
}
$sth->finish;
$dbh->commit;

$dbh->disconnect;
exit 0;
