#!/usr/bin/env sh

# no_of_cores=$(nproc --all)

bench() {
    script="$1"
    fname="$2"

    touch "$fname"
    echo "**** Script: $script ****"
    for v in $(seq 5 5 100);
    do
        res="$(command time -v poetry run python "$script" 2>&1)"
        mem=$(echo "$res" | grep -oP 'Maximum resident set size \(kbytes\): \K\d+')
        cpu=$(echo "$res" | grep -oP 'Percent of CPU this job got: \K\d+')
        tm=$(echo "$res" | grep -oP 'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): \K[0-9.:]+')
        echo "num of vertices - ${v}:"
        echo "$mem,$cpu,$tm"
        echo "$mem,$cpu,$tm" >> "$fname"
    done
}

echo 'Reset vertices...'
rm res/vertices/*

for i in $(seq 0 9);
do
    echo "--- ITERATION $i ---"
    bench lg_create_vertices.py "res/vertices/lg_vertices_${i}.txt"
    bench nx_create_vertices.py "res/vertices/nx_vertices_${i}.txt"
    bench scg_create_vertices.py "res/vertices/scg_vertices_${i}.txt"
done

