
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
# my $d = 0+CGI::param('d');
# my $n = 0+CGI::param('n');

# print CGI::header(-charset => "utf-8");


my $l = Calendar::Phugpa::has_leap_month($Y, $M);
$l = ($l ? 1 : 0);
print $l;