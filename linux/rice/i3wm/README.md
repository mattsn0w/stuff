# Notes

```

# See the list at https://github.com/ryanoasis/nerd-fonts/releases
for fontname in SourceCodePro MartianMono Meslo UbuntuMono ; do
    mkdir -p ~/.local/share/fonts/$fontname 
    pushd ~/.local/share/fonts/$fontname 
    wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/${fontname}.zip
    unzip ${fontname}.zip
    popd
done

# To populate font cache run:
fc-cache -f -v
# Verify the fonts are cached with:
fc-list | grep -i nerd

```


## Packages installed
apt install -y i3 i3-wm i3status rofi alacritty kitty fluxbox chromium npm neovim python3-venv python3-pip \
    picom polybar curl ca-certificates zsh zsh-common zsh-doc

## Docker Install
```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## References
* https://www.youtube.com/watch?v=wXZgUudR41I
* https://github.com/typecraft-dev/dotfiles
* https://askubuntu.com/questions/3697/how-do-i-install-fonts
* https://www.nerdfonts.com/#home
* https://github.com/Powerlevel9k/powerlevel9k/
* https://github.com/romkatv/powerlevel10k
* 
