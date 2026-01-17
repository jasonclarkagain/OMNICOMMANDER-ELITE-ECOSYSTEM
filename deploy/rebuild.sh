#!/bin/bash
export SDKMAN_DIR="$HOME/.sdkman"
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk use java 17.0.10-tem
export JAVA_HOME="$HOME/.sdkman/candidates/java/current"
export PATH="$JAVA_HOME/bin:$PATH"
source ~/omnicommander_elite/venv/bin/activate
rm -rf .buildozer/android/platform/build-arm64-v8a/build/other_builds/kivy
export CPATH=""
export C_INCLUDE_PATH=""
export CPLUS_INCLUDE_PATH=""
export PYTHONHOME=""
export PYTHONPATH=""
buildozer -v android debug
