#!/bin/awk -f
BEGIN {
    print $0
}

{
    myArr[$3][$2]++
}

END {
    for(x in myArr) {
	print myArr[x]
	for(y in x) {
	    print myArr[x][y]
	}
	print "\n"
    }
}