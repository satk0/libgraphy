#!/usr/bin/env sh

echo '*** Libgraphy ***'
for i in {100000..1000000..100000}
do
  python lg_cpu_mem_bench.py $i
done
echo '*** NetworkX ***'
for i in {100000..1000000..100000}
do
  python nx_cpu_mem_bench.py $i
done
echo '*** SciPy Graph ***'
for i in {100000..1000000..100000}
do
  python scg_cpu_mem_bench.py $i
done
