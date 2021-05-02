# Installation

## Clone the repos

```bash
cd ~
git clone https://github.com/aming/dotfiles.git dotfiles
```

## Update all the submodules

You could update the submodules to the latest commit available from the remote

 ```bash
 git submodule update --init <submodules name>
 # For all repos
 git submodule update --init --recursive
 ```
 
## Install Homebrew and tools

Install the Homebrew tools
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install Batteries to executable included
``` bash
brew install aming/aming/Batteries
```

# How-to
## ZSH
### Install a new oh-my-zsh plugin
Install the plugin by adding a new submodule to this repos

1. Checkout the package to `$ZSH_CUSTOM/plugins` (`zsh/oh-my-zsh-plugins/plugins/`)

 ```bash
 git submodule add <repos> zsh/oh-my-zsh-plugins/plugins/<plugin_name>
 git submodule init
 ```

1. Enable it in the .zshrc

 ```
 plugins=(other-plugins <plugin_name>)
 ```

1. Check in the changes
 ```bash
 git add .gitmodules
 git commit
 ```

### Removing a plugin
1. Remove the plugin from plugins list in the zshrc

 ```
 plugins=(other-plugins)
 ```

1. Remove the submodules

 ```bash
 git submodule rm zsh/oh-my-zsh-plugins/plugins/<plugin_name>
 ```
