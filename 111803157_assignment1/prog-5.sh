#!/bin/bash
echo -n "Enter marks of subject1: " 
read m1
echo -n "Enter marks of subject2: "
read m2
echo -n "Enter marks of subject3: "
read m3
echo -n "Enter marks of subject4: "
read m4
echo -n "Enter marks of subject5: "
read m5

tot=$(expr $m1 + $m2 + $m3 + $m4 + $m5) 

per=$((100*$tot/500))


echo "You got $per%"

if [ $per -ge 75 ]
then 
	 echo "Result : Pass"
	 echo "Grade : I Division"
elif [ $per -ge 55 ] && [ $per -lt 75 ] 
then 
	echo "Result : Pass"
	echo "Grade : I Division"
elif [ $per -ge 35 ] && [ $per -lt 55 ]
then 
	echo "Result : Pass"
        echo "Grade : III Division"  
else 
        echo "Result : Fail"
fi

