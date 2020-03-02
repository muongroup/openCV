#!/bin/sh

unzip image_comp.zip

for i in $(seq 1 30); do
  unzip image_comp\ \($i\).zip
  rm image_comp\ \($i\).zip
done

rm *.zip