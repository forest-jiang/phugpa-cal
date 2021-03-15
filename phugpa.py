# import matplotlib.pyplot as plt
import numpy as np
from math import floor, ceil
import datetime
from julian import from_jd
def inverse_julian_day(jd):
	return from_jd(jd)[0]

# Moon Table
MOON_TAB = (0, 5, 10, 15, 19, 22, 24, 25)
SUN_TAB	 = (0, 6, 10, 11)

# moon_tab_int(i): moon_tab for integer values.
def _moon_tab_int(i):
  i = i % 28
  if i <= 7:
  	return MOON_TAB[i]
  if i <= 14:
  	return MOON_TAB[14 - i]
  if i <= 21:
  	return - MOON_TAB[i - 14]
  return - MOON_TAB[28 - i]

def _moon_tab(i):
	u = _moon_tab_int(int(ceil(i)))
	d = _moon_tab_int(int(floor(i)))
	return d + (i - floor(i)) * (u - d)

A1 = 253.0  / 3528
A2 = 1.0 / 28
# use constant A2	=> 1/28 + 1/105840 # not used see Janson, p. 17, bottom.
A0 = 475.0 / 3528

# moon_anomaly(day, month_count)
def _moon_anomaly(day, month_count):
	return month_count * A1 + day * A2 + A0

# # moon_equ(day, month_count): Equation of the moon.
def _moon_equ(day, month_count):
	return _moon_tab(28 * _moon_anomaly(day, month_count))


# sun_tab_int(i): Sun tab for integer values
def _sun_tab_int(i):
	i = i % 12
	if i <= 3:
		return SUN_TAB[i]
	if i <= 6:
		return SUN_TAB[6 - i]
	if i <= 9:
		return -SUN_TAB[i - 6]
	return -SUN_TAB[12 - i]

def _sun_tab(i): # sun tab, with linear interpolation.
	u = _sun_tab_int(int(ceil(i)))
	d = _sun_tab_int(int(floor(i)))
	return d + (i - floor(i)) * (u - d)

S1 = 65.0/804 # 1/12.369 sun period in each moon period
S0 = 743.0/804
S2 = S1 / 30
# mean_sun(day, month_count)
def _mean_sun(day, month_count):
	return month_count * S1 + day * S2 + S0

# # sun_equ(day, month_count): Equation of the sun.
def _sun_equ(day, month_count):
	return _sun_tab(12.0 * (_mean_sun(day, month_count) - 1.0/4))

M1 = 167025.0 / 5656 # the period of moon, 29.53
M2 = M1 / 30
M0 = 2015501.0 + 4783.0 / 5656

# mean_date(day, month_count)
def _mean_date(d, n):
	return n * M1 + d * M2 + M0

# true_date(day, month_count)
def _true_date(d, n):
	return _mean_date(d, n) + _moon_equ(d, n) / 60 - _sun_equ(d, n) / 60

# day_before(day, month_count): substract 1 day from a date
def _day_before(d, n):
	if d == 1:
		return (30, n - 1)
	else:
		return (d - 1, n)


WEEKDAYS = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
# year elements & animals
YEAR_ELEMENTS = ('Wood', 'Fire', 'Earth', 'Iron', 'Water')
YEAR_ANIMALS = ('Mouse', 'Ox', 'Tiger', 'Rabbit', 'Dragon',
	'Snake', 'Horse', 'Sheep', 'Monkey', 'Bird', 'Dog', 'Pig')
YEAR_GENDER = ('Male', 'Female')

# print(type(SUN_TAB))
# week day from julian day
def weekday(jd):
	return WEEKDAYS[int(floor((jd + 1) % 7))]

# figure out the animal and element for a tibetan year
def year_attributes(year):
	Y = int(year['tib_year'])
	year['animal'] = YEAR_ANIMALS[(Y + 1) % 12]
 	year['element'] = YEAR_ELEMENTS[((Y - 1) / 2) % 5]
 	year['gender'] = YEAR_GENDER[(Y + 1) % 2]
 	return year


#  Figures out a year's info based on the Tibetan calendar, ex. the 3rd year of
# the 15th Rabjung calendrical cycle.  
# Inputs:
#   cycle_no : number of the cycle
#   year_no  : number of the year within the cycle, from 1 to 60.
# Returns: a hashref with the following elements:
#   cycle_no  : number of the cycle
#   year_no   : number of the year within the cycle, from 1 to 60.
#   western_year : western year during which most of the given tibetan year falls
#   tib_year  : tibetan year number (i.e western year + 127)
def rabjung_year(cycle_no, year_no):
	if year_no < 1 or year_no > 60:
		raise
	year = {'cycle_no': cycle_no,
		    'year_no': year_no,
		    'western_year': (966 + year_no + 60 * cycle_no)}
	year['tib_year'] = year['western_year'] + 127
	return year_attributes(year)

# Figures out a year's info from a Western calendar year number, ex. 2008.
# Returns: same as rabjung_year().
def mod(x, n):
	return x % n
def amod(x, n):
	if mod(x, n) == 0:
		return n
	return mod(x, n)

def western_year(w_year):
	year = {
		'cycle_no': int(ceil((w_year - 1026.0) / 60)),
		'year_no': amod(w_year - 6, 60),
		'tib_year': w_year + 127,
		'western_year': w_year}
	return year_attributes(year)

# Figures out a year's info from a Tibetan calendar year number, ex. 2135.
# Returns: same as rabjung_year().
def tibetan_year(y):
  return western_year(y - 127)


Y0 = 806
ALPHA = 1 + 827.0/1005
BETA = 123
# from_month_count(n)
#
# Figures out the Tibetan year number, month number within the year, and whether
# this is a leap month, from a "month count" number.  See Svante Janson, 
# "Tibetan Calendar Mathematics", p.8 ff.
# 
# Returns: (year, month, is_leap_month)
def from_month_count(n):
	x = ceil(12 * S1 * n + ALPHA)
	M = amod(x, 12)
	Y = (x - M) / 12 + Y0 + 127
	l = (ceil(12 * S1 * (n + 1) + ALPHA) == x)
	return (Y, M, l)

# to_month_count(year, month, is_leap_month)
#
# This is the reverse of from_month_count(): from a Tibetan year, month number
# and leap month indicator, calculates the "month count" based on the epoch.
def to_month_count(Y, M, l):
	Y-=127		# the formulas on Svante's paper use western year numbers
	l = int(l)
	return floor((12 * (Y - Y0) + M - ALPHA - (1 - 12 * S1) * l) / (12 * S1))

# =head2 has_leap_month(year, month)
# Calculates whether a given Tibetan year and month number is duplicated, i.e
# is preceded by a leap month.
# =cut
def _has_leap_month(Y, M):
	Mp = 12 * (Y - 127 - Y0) + M
	return ((2 * Mp) % 65 == BETA % 65) or ((2 * Mp) % 65 == (BETA + 1) % 65)

# =head2 tib_to_julian(year, month, is_leap_month, day)
# Gives the Julian date for a Tibetan year, month number (leap or not) and
# Tibetan day.  
# Does not check that the tibetan day actually exists: 
#  - If given the date of a skipped day, will return the same Julian date as the
#    day before.  
#  - If given the date of a duplicate day, returns the Julian date of the second
#    of the two.
def tib_to_julian(Y, M, l, d):
  n = to_month_count(Y, M, l)
  return floor(_true_date(d, n))

# tib_to_western(year, month, leap_month, day, leap_day)
# Calculates full information for a given Tibetan date, given by Tibetan
# year number (ex. 2135), month number (1 to 12), leap month (boolean),
# day number, and leap day (boolean).
# For duplicated days, just as with duplicated months, the "main" day or month is
# the second, and the "leap" day or month is the first.
# Returns a hashref with the following fields:
#   year           - a hashref as returned by rabjung_year and similar functions above

#   month_no       - tibetan month number (as passed)
#   is_leap_month  - boolean, whether this is a leap month (this is the same as the
# 		   passed "leap month" boolean, except if you try to get dates
# 		   within a non-existing leap month, in which case is_leap_month
# 		   is returned as false
#   has_leap_month - boolean, whether this year and month is duplicated (regardless
# 		   of whether the date is calculated within the leap or the main month)

#   day_no	 - the day number within the Tibetan month, as passed
#   skipped_day	 - whether this is a skipped day, which does not figure in the 
# 		   Tibetan calendar
#   is_leap_day    - boolean, whether this is a leap day (same as the passed leap_day
#                    value, except if you request a leap day when there isn't one)
#   has_leap_day   - whether this is a duplicated day (regardless of whether we are
#                    calculating info about the main or the leap day)
#   western_date	 - the Western date ("YYYY-MM-DD") corresponding to the Tibetan day.
#   weekday        - weekday ("Sun", "Mon", etc) of the western_date
#   julian_date    - the Julian day number for this Western date
def tib_to_western(Y, M, l, d, ld):
  jd = tib_to_julian(Y, M, l, d)

  # also calculate the Julian date of the previous Tib. day
  n = to_month_count(Y, M, l)
  b_jd = floor(_true_date(*_day_before(d, n)))

  # figure out leap months, leap days & skipped days
  has_leap_month = _has_leap_month(Y, M)
  has_leap_day = (jd == b_jd + 2)
  skipped_day = (jd == b_jd)
  ld = ld and has_leap_day

  # figure out western date info for the main or leap day
  if ld:
  	jd -= 1
  (w_y, w_m, w_d) = inverse_julian_day(jd)

  day = {
    "year":		 		tibetan_year(Y),
    "month_no":		 	M,
    "is_leap_month":	(l and has_leap_month),
    "has_leap_month":	has_leap_month,

    "day_no":		 d,
    "skipped_day":	 skipped_day,
    "is_leap_day":	 ld,
    "has_leap_day":	 has_leap_day,

    "western_date":	 "%.4d-%.2d-%.2d" % (w_y, w_m, w_d),
    "julian_date":	 jd,
    "weekday":		 weekday(jd),
  }
  return day


# to calculate Tibetan dates from western ones, we use a binary search algorithm
# within a span of 2 years.  for this we use a variant of true_date which takes
# a linear "tibetan day number", defined as day_no + 30 * month_no.
def tib_day_to_julian(d):
	n = floor((d - 1) / 30)
	d = d % 30
	if d == 0:
		d = 30
	return floor(_true_date(d, n))

# =head2 western_to_tib(western_year, month, day)
# Calculates a Tibetan date for a given western date.  This does a binary search,
# and is therefore much slower than tib_to_western().
# Returns: (tib_year, tib_month, leap_month, tib_day, leap_day)
# The algorithm could be much improved by using the reverse of mean_date()
# to start with, and then using the fact that julian dates and "tibetan day
# numbers" have a quasi-linear relation.
def western_to_tib(w_y, w_m, w_d):
  jd = julian_day(w_y, w_m, w_d)

  tib_year1 = w_y + 126
  tib_year2 = w_y + 128

  n1 = to_month_count(tib_year1, 1, 1)
  n2 = to_month_count(tib_year2, 1, 1)

  dn1 = 1 + 30 * n1
  dn2 = 1 + 30 * n2

  jd1 = tib_day_to_julian(dn1)
  jd2 = tib_day_to_julian(dn2)
  if jd1 > jd or jd > jd2:
	raise Exception("Binary search algo is wrong")

  while dn1 < dn2 - 1 and jd1 < jd2 - 1:
    ndn = floor(((dn1 + dn2) * 1.0) / 2)
    njd = tib_day_to_julian(ndn)
    if (njd < jd):
      dn1 = ndn
      jd1 = njd
    else:
      dn2 = ndn
      jd2 = njd

  # so we found it put it in dn2 & jd2.  
  # if the western date is the 1st of a duplicated tib. day, then jd1 == jd - 1 and
  #   jd2 == jd + 1, and the corresponding tib. day number is the one from jd2.
  if jd1 == jd:
    jd2 = jd1
    dn2 = dn1

  # figure out the real tib. date: year, month, leap month, day number, leap day.
  leap_day = (jd2 > jd)
  n = floor((1.0 * dn2 - 1) / 30)
  dn2 = (dn2 % 30)
  if dn2 == 0:
  	dn2 = 30
  (Y, M, l) = from_month_count(n)
  return (Y, M, l, dn2, leap_day)



# =head2 losar(tib_year)
# Calculates the Western date for Losar (Tibetan new year) of a given Tibetan
# year number (ex. 2137).
# Returns: "YYYY-MM-DD" string.
def losar(Y):
  jd = 1 + tib_to_julian(Y - 1, 12, 0, 30)
  (w_y, w_m, w_d) = inverse_julian_day(jd)
  return "%.4d-%.2d-%.2d" % (w_y, w_m, w_d)

# =head2 tibetan_month(year, month, leap_month)
# Calculates full information about a Tibetan month: whether it is
# duplicated or not, and the western start and end date for it.
# Returns a hashref with the following fields:
#   year           - a hashref as returned by rabjung_year and similar functions above
#   month_no       - tibetan month number (as passed)
#   is_leap_month  - boolean, whether this is a leap month (this is the same as the
# 		   passed "leap month" boolean, except if you try to get dates
# 		   within a non-existing leap month, in which case is_leap_month
# 		   is returned as false
#   has_leap_month - boolean, whether this year and month is duplicated (regardless
# 		   of whether the date is calculated within the leap or the main month)
#   start_date     - Western date of the 1st of the month (or 2nd if the 1st is skipped),
# 		   in "YYYY-MM-DD" format
#   end_date       - Western date of the 30th of the Tib. month.

# The start_date and end_date correspond to the leap month if leap_month is passed,
# otherwise to the main month (i.e the second of the two).
def tibetan_month(Y, M, l):
  has_leap = _has_leap_month(Y, M)
  l = l and has_leap
  # calculate the Julian date 1st and last of the month
  n = to_month_count(Y, M, l)
  jd1 = 1 + floor(_true_date(30, n - 1))
  jd2 = floor(_true_date(30, n))

  month = {
    "year":		 tibetan_year(Y),
    "month_no":		 M,
    "is_leap_month":	 l,
    "has_leap_month":	 has_leap,
    "start_date":		 "%.4d-%.2d-%.2d" % inverse_julian_day(jd1),
    "end_date":		 "%.4d-%.2d-%.2d" % inverse_julian_day(jd2),
  }
  return month

# =head2 year_calendar(tib_year)
# Generate a calendar for a whole Tibetan year, given by Tib. year number.
# Returns: a hashref containing the year's info, including each of the months
# in succession within year->{months}.  Each month includes all the days in
# succession within month->{days}.
def year_calendar(Y):
  year = tibetan_year(Y)

  # loop over the months, inserting leap months before the main ones
  months = []
  for M in range(1,13):
    if _has_leap_month(Y, M):
    	months.append(generate_month(Y, M, 1))

    months.append(generate_month(Y, M, False))

  months[0]['days'][0]['special_day'] = 'Losar'
  year['months'] = months
  return year


SPECIAL_DAYS = {
	8	: "Medicine Buddha & Tara Day",
	10	: "Guru Rinpoche Day",
	15	: "Amitabha Buddha Day Full Moon",
	25	: "Dakini Day",
	29	: "Dharmapala Day",
	30	: "Shakyamuni Buddha Day New Moon",
	}

# figure out if a day is special if it is skipped, return its speciality so it can be
# applied to the next day.  on dup days, the special one is the 1st.
def special_day(no, day, carry_special):

  # if we are carrying over a special feature from the day before, apply it
  if carry_special:
    day['special_day'] = carry_special + ' (carried over)' 
  if no not in SPECIAL_DAYS:
  	return None
  if day['skipped_day']:
  	return SPECIAL_DAYS[no]
  if day['has_leap_day'] and not day['is_leap_day']:
  	return None

  # carried over special features can overlap with the ones for the day itself!
  if 'special_day' in day:
    day['special_day'] +=  ' ' + SPECIAL_DAYS[no]
  else:
    day['special_day'] = SPECIAL_DAYS[no]
  return None

# generate a month with all its days
def generate_month(Y, M, l):
  month = tibetan_month(Y, M, l)
  carry_special = False

  # loop over the days, taking care of dup and missing days
  days = []
  for d in range(1, 31):
    day = tib_to_western(Y, M, l, d, False)

    # insert leap days before their main day
    if day['has_leap_day']:
      day2 = tib_to_western(Y, M, l, d, 1)
      carry_special = special_day(d, day2, carry_special)
      days.append(day2)

    carry_special = special_day(d, day, carry_special)
    if day['skipped_day']:
    	continue
    days.append(day)
  # print len(days)
  month['days'] = days
  return month

