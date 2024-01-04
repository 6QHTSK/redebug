repo_url="$1.git"
repo_name=$(basename $repo_url .git)
if [ -z "$2" ]; then
        echo "Cloning Master of $repo_name"
        git clone --depth=1 $1
else
        echo "Cloning Branch/Tag $2 of $repo_name"
        git clone --branch $2 --depth=1 $1
fi
start=$(date +%s%3N)
python redebug.py $repo_name
end=$(date +%s%3N)
duration=$((end-start))
printf "Execution time %d.%03ds\n" $((duration/1000)) $((duration%1000))
mv vul.log "$repo_name.$2.log"
rm -rf $repo_name
