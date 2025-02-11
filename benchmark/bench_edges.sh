#!/usr/bin/env sh

# no_of_cores=$(nproc --all)

bench() {
    script="$1"
    fname="$2"

    touch "$fname"
    echo "**** Script: $script ****"
    tmp=50
    while IFS= read -r edge; do
        res="$(command time -v poetry run python "$script" "${edge}" 2>&1)"
        mem=$(echo "$res" | grep -oP 'Maximum resident set size \(kbytes\): \K\d+')
        cpu=$(echo "$res" | grep -oP 'Percent of CPU this job got: \K\d+')
        tm=$(echo "$res" | grep -oP 'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): \K[0-9.:]+')
        echo "num of edges - ${tmp}:"
        echo "$mem,$cpu,$tm"
        echo "$mem,$cpu,$tm" >> "$fname"

        tmp=$((tmp+50))
    done < $edges_file
}

echo 'Reset edges...'
rm res/edges/*

#edges_file='generated/example_edges.txt'
edges_file='generated/edges_50.txt'

for i in $(seq 0 9);
do
    echo "--- ITERATION $i ---"
    bench lg_create_edges.py "res/edges/lg_edges_50_${i}.txt"
    bench nx_create_edges.py "res/edges/nx_edges_50_${i}.txt"
    bench scg_create_edges.py "res/edges/scg_edges_50_${i}.txt"
done

