#!/bin/bash

GH_USER="CAS-14"
MODULES_DIR="/home/cas/code/WWWModules"

echo "Repo name: "
read repo_name
echo "Internal blueprint name: "
read bp_name
echo "Domain name: "
read domain_name

cd $MODULES_DIR
cp -r www_template $repo_name
py_file="$repo_name/$repo_name.py"
mv "$repo_name/template.py" $py_file

sed -i -e "s/BP_NAME/$bp_name/g" $py_file
sed -i -e "s/REPO_NAME/$repo_name/g" $py_file
sed -i -e "s/DOMAIN/$domain_name/g" $py_file

rm "$repo_name/gen_template.sh"

echo "Successfully created $repo_name ($bp_name) for $domain_name!"
echo "Creating git repo and adding to GitHub..."

cd $repo_name
git init -b main
git add .
git commit -m "first commit"
gh repo create --source . --public --push

echo "# $repo_name\n\nWebserver module $repo_name ($bp_name)" > README.md

cd ..
echo "All done!"