#!/usr/bin/env bash

input_file=access.log
output_file=result
jsonify=false


while (( ${#} > 0 )); do
  if [ "${1}" == "--json" ]; then
    jsonify=true 
  fi
  shift
done


total_requests=$(wc -l $input_file | awk '{print $1}')
total_methods=$(awk -F\" '{print $2}' $input_file | awk '$1 ~ /^(GET|POST|PUT|HEAD|DELETE|CONNECT|OPTIONS|TRACE|PATCH)$/ {print $1}' | sort | uniq -c | sort -rn)
top_requests=$(awk '{print $7}' $input_file | sort | uniq -c | sort -rn | head -n 10)
top_4xx_size=$(awk 'match($9, /4[0-9][0-9]/) {print $7, $9, $10, $1}' $input_file | sort -rnk3 | head -n 5)
top_5xx_ip=$(awk '($9 ~ /^5[0-9][0-9]$/) {print $1}' $input_file | sort | uniq -c | sort -rn | head -n 5)



if [ $jsonify = true ]; then
  JSON_RESULT=$(jq -n \
		--arg total_requests "$total_requests" \
		--argjson total_methods "$(jq -R '[splits(" +")] | map(select(. != "")) | {method: .[1], count: (.[0] | tonumber)}' <<< "$total_methods" | jq -s )" \
		--argjson top_requests "$(jq -R '[splits(" +")] | map(select(. != "")) | {url: .[1], count: (.[0] | tonumber)}' <<< "$top_requests" | jq -s )" \
		--argjson top_4xx_size "$(jq -R '[splits(" +")] | map(select(. != "")) | {url: .[0], statusCode: (.[1] | tonumber), size: (.[2] | tonumber), ip: .[3]}' <<< "$top_4xx_size" | jq -s )" \
		--argjson top_5xx_ip "$(jq -R '[splits(" +")] | map(select(. != "")) | {ip: .[1], count: (.[0] | tonumber)}' <<< "$top_5xx_ip" | jq -s )" \
		'{totalRequests: ($total_requests | tonumber), totalMethods: $total_methods, topRequests: $top_requests, topSize4xx: $top_4xx_size, topIp5xx: $top_5xx_ip}'
               )

  echo $JSON_RESULT > $output_file


else
  echo -e "Total requests:\n$total_requests\n" > $output_file
  echo -e "Total methods:\n$total_methods\n" >> $output_file
  echo -e "Top requests:\n$top_requests\n" >> $output_file
  echo -e "Top requests size 4xx:\n$top_4xx_size\n" >> $output_file
  echo -e "Top IP 5xx:\n$top_5xx_ip\n" >> $output_file
fi

