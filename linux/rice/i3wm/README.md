# Notes

```
cd ~/Downloads && mkdir fonts
wget https://objects.githubusercontent.com/github-production-release-asset-2e65be/27574418/3bb14dd5-6762-4d60-b480-a4c6f484d3c9?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20240901%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240901T205957Z&X-Amz-Expires=300&X-Amz-Signature=eaedea97468331d0251fb26aa1f61a2aede5d07c97b11a5e20ab7da06bd03cf9&X-Amz-SignedHeaders=host&actor_id=814696&key_id=0&repo_id=27574418&response-content-disposition=attachment%3B%20filename%3DSourceCodePro.zip&response-content-type=application%2Foctet-stream
wget https://objects.githubusercontent.com/github-production-release-asset-2e65be/27574418/f65d13f2-5f07-4167-8c91-41226769d00b?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20240901%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240901T205922Z&X-Amz-Expires=300&X-Amz-Signature=9db094823522e96a166c05880945c41cd9d76e498b0acc6a06de48ab06e4d496&X-Amz-SignedHeaders=host&actor_id=814696&key_id=0&repo_id=27574418&response-content-disposition=attachment%3B%20filename%3DMartianMono.zip&response-content-type=application%2Foctet-stream
wget https://objects.githubusercontent.com/github-production-release-asset-2e65be/27574418/5c372df6-5404-410a-bd48-5172d2d5048d?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20240901%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240901T205746Z&X-Amz-Expires=300&X-Amz-Signature=e7f5786ea90076e5e706b1b240f9ea72f94540a4287f480057208c77ea746e7f&X-Amz-SignedHeaders=host&actor_id=814696&key_id=0&repo_id=27574418&response-content-disposition=attachment%3B%20filename%3DMeslo.zip&response-content-type=application%2Foctet-stream

mkdir -p ~/.local/share/fonts/Meslo ~/.local/share/fonts/MartianMono ~/.local/share/fonts/SauceCodePro
# unzip font files into each rewspective directory
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
