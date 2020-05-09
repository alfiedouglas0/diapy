#!/usr/bin/env bash

# sqlcipher if is not already installed 
if [ -x "$(sqlcipher --version >/dev/null 2>&1)" ]; then
    echo "sqlcipher is not installed"

    echo "Terminating..."; exit
    # read -r -p "Would you like to install? (Requires sudo) [Y/n] " yn_responce
    # if [[ ! "$yn_responce" =~ ^(Y|y)$ ]]; then
    #     echo "Installation terminating..."
    #     exit
    # fi

    # TODO sqlcipher installation!
fi

pip3 install -e .
