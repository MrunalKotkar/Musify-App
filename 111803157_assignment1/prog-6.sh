#!/bin/bash
echo -n "Enter operand 1: "
read num1
echo -n "Enter operand 2: "
read num2
echo -e "Enter operator choice: \n1 : +\n2 : -\n3 : *\n4 : /\n"
read op

if [ $op -eq 1 ]
then
	sum=`expr $num1 + $num2`
	echo "Sum of two numbers $num1 and $num2 is $sum"
elif [ $op -eq 2 ]
then
	diff=`expr $num1 - $num2`
	echo "Difference of two numbers $num1 and $num2 is $diff"
elif [ $op -eq 3 ]
then
	mul=`expr $num1 \* $num2`
	echo "Product of two numbers $num1 and $num2 is $mul"
else
	quotient=`expr $num1 / $num2`
	remainder=`expr $num1 % $num2`
	echo "Division of two numbers $num1 and $num2 is quotient = $quotient and rem = $remainder"
fi


