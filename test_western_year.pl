#!/usr/bin/perl

use strict;
use lib '/srv/www/perl-lib';
use utf8;

use Calendar::Phugpa;
use Lingua::BO::Wylie;
use Encode ();
use CGI ();

binmode(STDOUT, ":utf8");

my $year = 0+CGI::param('year');
my $input_month = 0+CGI::param('month');
my $d = 0+CGI::param('d');
my $n = 0+CGI::param('n');

# print CGI::header(-charset => "utf-8");


my $y = Calendar::Phugpa::western_year($year);

# print "cycle_no: $y->{cycle_no} ";
# print "year_no: $y->{year_no} ";
# print "tib_year: $y->{tib_year} ";
# print "western_year: $y->{western_year} ";

print "animal: $y->{animal} ";
print "cycle_no: $y->{cycle_no} ";
print "element: $y->{element} ";
print "gender: $y->{gender} ";
print "tib_year: $y->{tib_year} ";
print "western_year: $y->{western_year} ";
print "year_no: $y->{year_no} ";