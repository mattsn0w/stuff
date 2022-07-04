#!/bin/bash
# Originally posted at https://snipplr.com/view/60879/monitoring-network-microbursts
# Author: Matt Snow 

function nets {
    TX_TOTAL=0
    RX_TOTAL=0
    TX_GAUGE="B"   # Bytes
    RX_GAUGE="B"   # Bytes
    INTERFACE="enp1s0"
    for ((i=0;i<10;i++)); do    
        RX_BYTES=$(cat /sys/class/net/${INTERFACE}/statistics/rx_bytes)
        TX_BYTES=$(cat /sys/class/net/${INTERFACE}/statistics/tx_bytes)
        LAST_RX_BYTES=${RX_BYTES}
        LAST_TX_BYTES=${TX_BYTES}
        sleep .10
        RX_BYTES=$(cat /sys/class/net/${INTERFACE}/statistics/rx_bytes)
        TX_BYTES=$(cat /sys/class/net/${INTERFACE}/statistics/tx_bytes)
        TX_DIFF=$[ ${TX_BYTES} - ${LAST_TX_BYTES} ]
        RX_DIFF=$[ ${RX_BYTES} - ${LAST_RX_BYTES} ]
        TX_TOTAL=$[ ${TX_TOTAL} + ${TX_DIFF} ]
        RX_TOTAL=$[ ${RX_TOTAL} + ${RX_DIFF} ]
        if [ ${RX_DIFF} -gt 1024 ]; then
            RX_GAUGE="KB"
            RX_DIFF=$[ ${RX_DIFF} / 1024 ]
            if [ ${RX_DIFF} -gt 1024 ]; then
                RX_GAUGE="MB"
                RX_DIFF=$[ ${RX_DIFF} / 1024 ]
            fi
        fi
        if [ ${TX_DIFF} -gt 1024 ]; then
            TX_GAUGE="KB"
            TX_DIFF=$[ ${TX_DIFF} / 1024 ]
            if [ ${TX_DIFF} -gt 1024 ]; then
                TX_GAUGE="MB"
                TX_DIFF=$[ ${TX_DIFF} / 1024 ]
            fi
        fi    
        if [[ ${TX_DIFF} -gt 0 || ${RX_DIFF} -gt 0 ]]; then
            printf "${i}00ms  - TX: ${TX_DIFF}${TX_GAUGE}\tRX: ${RX_DIFF}${TX_GAUGE}\n"
        fi
    done
    if [ ${RX_TOTAL} -gt 1024 ]; then
        RX_GAUGE="KB"
        RX_TOTAL=$[ ${RX_TOTAL} / 1024 ]
        if [ ${RX_TOTAL} -gt 1024 ]; then
            RX_GAUGE="MB"
            RX_TOTAL=$[ ${RX_TOTAL} / 1024 ]
        fi
    fi
    if [ ${TX_TOTAL} -gt 1024 ]; then
        TX_GAUGE="KB"
        TX_TOTAL=$[ ${TX_TOTAL} / 1024 ]
        if [ ${TX_TOTAL} -gt 1024 ]; then
            TX_GAUGE="MB"
            TX_TOTAL=$[ ${TX_TOTAL} / 1024 ]
        fi
    fi 
    printf "1000ms - TX: ${TX_TOTAL}${TX_GAUGE}\tRX: ${RX_TOTAL}${RX_GAUGE}\n"
}

while :; do nets && date "+%S"; done
