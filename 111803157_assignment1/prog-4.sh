#!/bin/bash
echo -n "Enter the radius of circle: "
read r
pi=3.14
circumference=$(echo "2*$r*$pi"|bc)
area=$(echo "$pi*$r*$r"|bc)
echo "The Area of the circle is $area"
echo "The Circumference of the circle is $circumference"

