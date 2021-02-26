#!/bin/bash

cg='zero_freakin_ram'
cgfs='/sys/fs/cgroup/memory'

echo $$ > ${cgfs}/${cg}/tasks

if [ ! -e ${cgfs}/${cg} ]; then
    mkdir ${cgfs}/${cg}
fi

echo 1G > ${cgfs}/${cg}/memory.limit_in_bytes

function getMemLimit() {
    echo "mem limit: $(cat ${cgfs}/${cg}/memory.limit_in_bytes)"
}

function getMemUsage() {
     echo "mem usage: $(cat ${cgfs}/${cg}/memory.usage_in_bytes)"
}

function eatMoreRam() {
    cat <( </dev/zero head -c 2G) <(sleep 100) | tail
}

function humaniec() {
    numfmt --to iec $1
}
for i in {0..120}; do
    echo "mem limit: $(humaniec $(getMemLimit | cut -d: -f2) )"
    echo "mem usage: $(humaniec $(getMemUsage | cut -d: -f2) )"
    eatMoreRam &
    sleep 1
done
