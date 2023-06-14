for i in */; do mv -v "$i" "$(echo "$i" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"; done
mv "cap'n-proto" capn-proto
mv 'graphviz-(dot)' graphviz-dot