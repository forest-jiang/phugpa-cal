use strict;
use Carp qw/croak/;
use Time::JulianDay qw/julian_day inverse_julian_day/;
use Encode ();
use CGI ();

# Convert from JD to Gregorian Date
binmode(STDOUT, ":utf8");

my $jd = 0+CGI::param('jd');


my $s = sprintf("%.4d-%.2d-%.2d", inverse_julian_day($jd));
print $s;