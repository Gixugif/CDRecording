NOW=$(date -d "1 day ago" +"%b%d%y")
CurrentMonth=$(date -d "1 day ago" +"%B")
CurrentDay=$(date -d "1 day ago" +"%-d")
CurrentYear=$(date -d "1 day ago" +"%Y")

cd "/mnt/share/COMMON FILES/STAFF FOLDERS/Jeffrey Zic/CDRHourly"

curl -H 'content-type: application/json' "192.168.0.199/gui/cdr/cdr?__auth_user=admin&__auth_pass=c^c\$g%o)d&sortby=end_timestamp&sortorder=desc&since=RANGE&rows=2000&between=${CurrentMonth}+${CurrentDay}%2C+${CurrentYear}&between=${CurrentMonth}+${CurrentDay}%2C+${CurrentYear}&show_outbound=0" > "/mnt/share/COMMON FILES/STAFF FOLDERS/Jeffrey Zic/CDRHourly/CDR/$NOW"

echo "/mnt/share/COMMON FILES/STAFF FOLDERS/Jeffrey Zic/CDRHourly/CDR/$NOW" | python "/mnt/share/COMMON FILES/STAFF FOLDERS/Jeffrey Zic/CDRHourly/hourlycdr.py" 