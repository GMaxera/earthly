Summary: Build automation tool for the container era
Name: earthly
Version: __earthly_version__
Release: 1
License: Business Source License
URL: https://earthly.dev
Group: System
Packager: Earthly team
Requires: bash
BuildRoot: /work/rpmbuild/

%description
Build automation tool for the container era

%install
mkdir -p %{buildroot}/usr/bin/
cp /usr/local/bin/earthly %{buildroot}/usr/bin/earthly

%files
/usr/bin/earthly

%post
set -e
# install bash auto completion
BASH_COMPLETION_DIR="/usr/share/bash-completion/completions"
if [ -d "$BASH_COMPLETION_DIR" ]
then
    earthly bootstrap --source bash > "$BASH_COMPLETION_DIR/earthly"
fi

# install zsh auto completion
ZSH_COMPLETION_DIR="/usr/local/share/zsh/site-functions"
if [ -d "$ZSH_COMPLETION_DIR" ]
then
    earthly bootstrap --source zsh > "$ZSH_COMPLETION_DIR/_earthly"
fi

# skip bootstraping if docker isn't installed or running
if ! command -v docker &> /dev/null
then
    echo "docker was not found; skipping earthly bootstrap"
    exit
fi
if ! docker info 2>/dev/null >/dev/null

%postun
set -e

if [ "$1" -eq 0 ]; then
  # "$1" is set to the number of packages left after operation; should be 1 on upgrade, 0 on uninstall.
  UNABLE_TO_REMOVE="unable to remove earthly-related docker resources"

  rm -f /usr/share/bash-completion/completions/earthly
  rm -f /usr/local/share/zsh/site-functions/_earthly

  if ! command -v docker &> /dev/null
  then
      echo "docker was not found; $UNABLE_TO_REMOVE"
      exit
  fi

  if ! docker info 2>/dev/null >/dev/null
  then
      echo "unable to query docker daemon; $UNABLE_TO_REMOVE"
      exit
  fi

  echo "removing earthly-buildkitd docker container"
  docker rm --force earthly-buildkitd

  echo "removing earthly-cache docker volume"
  docker volume rm --force earthly-cache
fi

%changelog
* Thu Feb 25 2021 alex <alex@earthly.dev>
- initial poc
