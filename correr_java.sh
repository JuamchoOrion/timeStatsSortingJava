#!/usr/bin/env bash
# Desde la raíz del repo: bash correr_java.sh
set -e
mkdir -p java/out
javac -d java/out java/*.java
for alg in insertion dualpivot merge heap; do
  for var in aleatorio asc desc; do
    java -cp java/out EjecutarComparativos "$alg" "$var"
  done
done
