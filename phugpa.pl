#!/usr/bin/perl

use strict;
use lib '/srv/www/perl-lib';
use utf8;

use Calendar::Phugpa;
use Lingua::BO::Wylie;
use Encode ();
use CGI ();

$CGI::POST_MAX = 1024 * 1024;	# max 1MB posts
$CGI::DISABLE_UPLOADS = 1;  	# no uploads

binmode(STDOUT, ":utf8");

my $year = 0+CGI::param('year');

print CGI::header(-charset => "utf-8");
start_html();

sub start_html {
  print <<_HTML_;
<html>
<head>
<style>
  body { background: #fff; margin-left: 100px; }
  body, td, input, select, textarea, h1, h2 { font-family:verdana, tahoma, helvetica; }
  body, td, input, select, textarea { font-size: 12pt; }
  h1 { font-size: 16pt; }
  h2 { font-size: 14pt; }
  .after { font-size: 9pt; }
  #tbl { border:1px solid #aaa; width:650px }
  #tbl td, #tbl th { border-bottom: 1px solid #ccc }
  #tbl th { background-color: #def }
  .tib { font-family: Jomolhari, Tibetan Machine Uni, Himalaya; font-size:18pt; line-height:28pt; margin-bottom:0cm; margin-top:0cm; font-weight:normal; }
  .tibtit { font-family: Jomolhari, Tibetan Machine Uni, Himalaya; font-size:20pt; line-height:30pt; margin-bottom:0cm; margin-top:0cm; font-weight:normal; }
  td.mark { border-left:1px dotted #ccc; padding-left: 12px }
</style>
<title>Tibetan Phugpa Calendar Calculator</title>
</head>
<body>
<form id="id__form" method="GET">
<br>
<h1>Tibetan Phugpa Calendar Calculator</h1>
Enter a year (Western calendar): <input id="id__i" name="year" size="6"> <input type="submit" value="Make Calendar">
</form>
<script>document.getElementById('id__i').focus()</script>
_HTML_
}

if (!$year) {
  finish();
  exit 0;
}

sub ordinal {
  my $n = shift;

  if ($n % 10 == 2 && $n % 100 != 12) {
    $n .= 'nd';
  } elsif ($n % 10 == 1 && $n % 100 != 11) {
    $n .= 'st';
  } elsif ($n % 10 == 3 && $n % 100 != 13) {
    $n .= 'rd';
  } else {
    $n .= 'th';
  }
  $n;
}

my $wl = Lingua::BO::Wylie->new(
  check		=> 0,
  check_strict	=> 0,
  print_warnings=> 0,
);
my $y = Calendar::Phugpa::year_calendar(127 + $year);

my $cycle_d = ordinal($y->{cycle_no});

my @mon = qw/x jan feb mar apr may jun jul aug sep oct nov dec/;
my @tmon = qw/x དང་པོ། གཉིས་པ། གསུམ་པ། བཞི་པ། ལྔ་པ། དྲུག་པ། བདུན་པ། བརྒྱད་པ། དགུ་པ། བཅུ་པ། བཅུ་གཅིག་པ། བཅུ་གཉིས་པ།/;
my %tday = (
  mon	=> 'ཟླ།',
  tue	=> 'དམར།',
  wed	=> 'ལྷག',
  thu	=> 'ཕུར།',
  fri	=> 'སངས།',
  sat	=> 'སྤེན།',
  sun	=> 'ཉི།',
);

my $title = "Tibetan Year $y->{tib_year}  &ndash; $y->{gender} $y->{element} $y->{animal} Year of the $cycle_d Rabjung Calendrical Cycle ($y->{western_year})";

print <<_HTML_;
  <br>
  <h2>$title</h2>
_HTML_

foreach my $m (@{ $y->{months} }) {
  my $title = ordinal($m->{month_no}) . " Tibetan Month";
  my $plus  = $m->{is_leap_month} ? '(+)' : '';
  my $tib_n = $tmon[ $m->{month_no} ];

print <<_HTML_;
  <br>
  <table id="tbl" border="0" cellspacing="1" cellpadding="2">
  <tr><th colspan="6">
    <span class="tibtit">བོད་ཟླ་$tib_n</span> &nbsp;&ndash;&nbsp; $title $plus
  </th></tr>
_HTML_

  my $prev = 0;
  foreach my $d (@{ $m->{days} }) {
    my ($month, $day) = ($d->{western_date} =~ /^\d+-(\d+)-(\d+)/);
    $month = ucfirst $mon[$month];

    my $tib_d  = $wl->from_wylie($d->{day_no});
    my $tib_wd = $tday{ lc $d->{weekday} };

    my $star = ($d->{day_no} == $prev + 2 ? '*' : '');
    my $plus = ($d->{is_leap_day} ? '+' : '');
    $prev = $d->{day_no};
    
print <<_HTML_;
  <tr>
    <td width="65"><span class="tib">&nbsp;$tib_wd</span></td>
    <td width="30"><span class="tib">$tib_d</span></td>
    <td width="60">&nbsp;$d->{day_no} $star $plus</td>
    <td width="40" class="mark">$d->{weekday}</td>
    <td width="80">$month $day</td>
    <td class="mark"><i>$d->{special_day}&nbsp;</i></td>
  </tr>
_HTML_
  }

print <<_HTML_;
  </table>
_HTML_
}
finish();

sub finish {
  print <<_HTML_;
<div class="after">
<br><br>
&middot; This conversion code is Free Software; you can <a href="/tibetan/Calendar-Phugpa-dev.zip">download the Perl module here</a>.
<br>&middot; Calendar calculations based on <a href="http://www2.math.uu.se/~svante/papers/calendars/tibet.pdf"><i>Tibetan calendar mathematics</i></a> by <a href="http://www2.math.uu.se/~svante">Svante Janson</a>.
<br><br>
</body>
</html>
_HTML_
}

