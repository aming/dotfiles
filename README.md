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

## Create Symbolic links of the configurations to the dotfiles

We use GNU Stow as the symlink farm manager to create symlink between the dotfiles and system configuration

To install NeoVim configuration files, run following under the dotfiles root directory

```
stow --dotfiles nvim vim zsh
```

To remove the configuration from the system by adding **-D** flag.

```
stow -D nvim vim zsh
```

## Initial Neovim plugins

During the first time starting the Neovim, it will automatically download the _Lazy.nvim_ to the _.config/_ folder.
After the _Lazy.nvim_ installed and Neovim started. Run `:Lazy` to start the Lazy console in Neovim.
And then `I` to install all plugins.

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

## Vim

1. To add a new plugin, create a new Lazy spec file under _nvim/lua/plugins_. And run the `:Lazy` to start the Lazy
Console to install the plugins list. And remember to check in  _nvim/lazy-lock.json_ for locked plugin versions.

