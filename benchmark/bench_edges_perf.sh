#!/usr/bin/env sh

bench() {
    script="$1"
    fname="$2"

    touch "$fname"
    echo "**** Script: $script ****"
    tmp=50
    while IFS= read -r edge; do
        res="$(perf stat -e instructions,cycles -x \  poetry run python "$script" "$edge" 2>&1)"
        ins=$(echo "$res" | grep -oP '\d+(?=[ ]*instructions)')
        cycles=$(echo "$res" | grep -oP '\d+(?=[ ]*cycles)')
        echo "num of edges - ${tmp}:"
        echo "$ins,$cycles"
        echo "$ins,$cycles" >> "$fname"

        tmp=$((tmp+50))
    done < $edges_file
}

echo 'Reset edges...'
rm res/edges_perf/*

#edges_file='generated/example_edges.txt'
edges_file='generated/edges_50.txt'

for i in $(seq 0 9);
do
    echo "--- ITERATION $i ---"
    bench lg_create_edges.py "res/edges_perf/lg_edges_50_${i}.txt"
    bench nx_create_edges.py "res/edges_perf/nx_edges_50_${i}.txt"
    bench scg_create_edges.py "res/edges_perf/scg_edges_50_${i}.txt"
done

