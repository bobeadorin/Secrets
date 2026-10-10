hasZsh=$(which zsh)
secretsPath=$(pwd)/secrets.py

echo "Zsh located at: $hasZsh"
echo "Path to save: $secretsPath"

if [ -n "$hasZsh" ]; then 
    echo "alias secrets=\"python3 $secretsPath\"" >> ~/.zshrc
    echo "Successfully added alias to ~/.zshrc!"
fi
