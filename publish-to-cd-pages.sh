#!/bin/bash
set -ev

# get clone master
git clone https://git.coding.net/yuangezhizao/yuangezhizao.git .deploy_git
cd .deploy_git
git checkout master

cd ../
mv .deploy_git/.git/ ./public/

cd ./public

git config user.name "yuangezhizao"
git config user.email "root@yuangezhizao.cn"

# add commit timestamp
git add .
git commit -m "Travis CI Auto Builder at `date +"%Y-%m-%d %H:%M:%S"`"

# Github Pages
#git push --force --quiet "https://${TravisCIToken}@${GH_REF}" master:master

# Coding Pages
git push --force --quiet "https://yuangezhizao:${CodingToken}@${CD_REF}" master:master
