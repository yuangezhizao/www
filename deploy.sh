#!/bin/bash
set -ev

git clone "https://yuangezhizao:${CodingToken}@${CD_REF}" coding_public

mv ./coding_public/.git/ ./public/

cd ./public

git config user.name "yuangezhizao"
git config user.email "root@yuangezhizao.cn"

git add .
git commit -m "Travis CI Auto Builder at `date +"%Y-%m-%d %H:%M:%S"`"

git push --force --quiet "https://yuangezhizao:${CodingToken}@${CD_REF}" master:master
