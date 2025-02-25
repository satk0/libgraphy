#!/usr/bin/env sh

bench() {
    script="$1"
    fname="$2"

    touch "$fname"
    echo "**** Script: $script ****"
    for v in $(seq 5 5 100);
    do
        res="$(perf stat -e instructions,cycles -x \  poetry run python "$script" "$v" 2>&1)"
        ins=$(echo "$res" | grep -oP '\d+(?=[ ]*instructions)')
        cycles=$(echo "$res" | grep -oP '\d+(?=[ ]*cycles)')
        echo "num of vertices - ${v}:"
        echo "$ins,$cycles"
        echo "$ins,$cycles" >> "$fname"
    done
}

echo 'Reset vertices...'
rm res/vertices_perf/*

for i in $(seq 0 9);
do
    echo "--- ITERATION $i ---"
    bench lg_create_vertices.py "res/vertices_perf/lg_vertices_${i}.txt"
    bench nx_create_vertices.py "res/vertices_perf/nx_vertices_${i}.txt"
    bench scg_create_vertices.py "res/vertices_perf/scg_vertices_${i}.txt"
done

