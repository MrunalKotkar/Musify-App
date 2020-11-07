#!/bin/bash
echo -n "Enter an Integer: "
read num
if [ `expr $num % 2` -eq 0 ]
then
	echo "Number $num is Even"
else
	echo "Number $num is Odd"
fi

