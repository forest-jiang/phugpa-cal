#!/usr/bin/perl

use strict;
use lib '/srv/www/perl-lib';
use utf8;

use Calendar::Phugpa;
use Lingua::BO::Wylie;
use Encode ();
use CGI ();

binmode(STDOUT, ":utf8");

my $Y = 0+CGI::param('Y');
my $M = 0+CGI::param('M');
my $l = 0+CGI::param('l');
my $n = 0+CGI::param('n');

# print CGI::header(-charset => "utf-8");


my $m = Calendar::Phugpa::tibetan_month($Y, $M, $l);

# print "cycle_no: $y->{cycle_no} ";
# print "year_no: $y->{year_no} ";
# print "tib_year: $y->{tib_year} ";
# print "western_year: $y->{western_year} ";
print "end_date: $m->{end_date} ";
print "has_leap_month: $m->{has_leap_month} ";
print "is_leap_month: $m->{is_leap_month} ";
print "month_no: $m->{month_no} ";
print "start_date: $m->{start_date} ";