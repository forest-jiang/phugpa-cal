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

# print CGI::header(-charset => "utf-8");


print Calendar::Phugpa::to_month_count($Y, $M, $l);