#!/bin/bash
echo -n "Enter Number 1: "
read num1
echo -n "Enter Number 2: "
read num2
echo -n "Enter Number 3: "
read num3

if [ $num1 -gt $num2 ] && [ $num1 -gt $num3 ]
then
	echo "Greater Number is $num1"
elif [ $num2 -gt $num1 ] && [ $num2 -gt $num3 ]
then
	echo "Greater Number is $num2"
else
	echo "Greater Number is $num3"
fi

