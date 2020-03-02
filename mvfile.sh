#!/bin/bash

array=("0208" "0209")
for i in ${array[@]};do
  mkdir $i
  mv image_2020$i* $i
done
