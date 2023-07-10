
#!/bin/bash

for instances in 1 2 4 8; do
    echo "Executando $instances instância(s) do iperf..."
    
    for i in $(seq 0 $((instances - 1))); do
        iperf -c 192.168.1.15 -t 300 -i 1 -Z reno -p $((5000 + i)) &
    done

    for port in $(seq 5000 $((5000 + instances - 1))); do
        echo "Executando script para porta $port..."
        ./scrip2.sh "$port" >> "./exp5/saida $instances $port.txt" &
    done

    sleep 300
   
    pkill -f "iperf"
    pkill -f "coleta.sh"

    echo "Quantidade de processos: $instances"
    echo "Informações coletadas no arquivo 'saida.txt'"
    echo "----------------------------------------------"
done
