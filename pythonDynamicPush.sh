pytest

if [ $? -eq 0 ]; then
    git add *
    read -p "commit message: " commitMessage
    git commit -m "$commitMessage"
    git push
else
    echo "test failed"
fi