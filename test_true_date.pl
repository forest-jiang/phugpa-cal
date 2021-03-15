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


print Calendar::Phugpa::true_date($d, $n);