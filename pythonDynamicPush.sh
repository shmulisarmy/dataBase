pytest

if [ $? -eq 0 ]; then
    git add *
    commitMessage= read -p "commit message: "
    git commit -m "$commitMessage"
    git push
else
    echo "test failed"
fi