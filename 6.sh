#!bin/bash
sed -e 's/\([A-Z0-9][A-Z0-9]*\))\([A-Z0-9][A-Z0-9]*\)/orbit_direct(o_\L\1,o_\L\2)./' > 6.out.pl
cat 6.pl >> 6.out.pl
