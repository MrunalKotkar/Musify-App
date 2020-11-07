#!/bin/bash
echo -n "Enter the cost price: " 
read cost_price
echo -n "Enter the selling price: "
read selling_price

dif=`expr $selling_price - $cost_price`

if [ $dif -lt 0 ]
then
	echo "Loss incurred of Rs ${dif#-}"
else
	echo "Profit made of Rs $dif"
fi
