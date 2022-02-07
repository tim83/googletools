poetry init --python="^3.9" 

poetry add --dev flake8 flake8-bugbear black isort bandit safety

# download gitignore
curl https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore > .gitignore
curl https://raw.githubusercontent.com/github/gitignore/master/Global/JetBrains.gitignore >> .gitignore

git init
git add .
git commit -m "Init"

