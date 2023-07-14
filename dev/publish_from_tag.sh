#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

if [ $# -eq 0 ]; then
    cat<<EOF
Usage:
  $0 \$VERSION
Example:
  $0 0.8.0rc2
where 0.8.0rc2 is the version and v0.8.0rc2 is the corresponding tag.
EOF
    exit 0
fi


version="$1"
tag="v${version}"
tar_gz="https://github.com/spdx/tools-python/releases/download/${tag}/spdx_tools_dist.tar.gz"
tag_dir="dist-${tag}"

cd -- "$(dirname "$0")/.."

if ! command -v twine &> /dev/null; then
    echo "twine could not be found"
    echo "maybe load venv with"
    echo "  . ./venv/bin/activate"
    echo "  . ./venv/bin/activate.fish"
    echo

    if [[ -d ./venv/bin/ ]]; then
        echo "will try to activate ./venv ..."

        source ./venv/bin/activate

        if ! command -v twine &> /dev/null; then
            echo "twine still could not be found"
            exit 1
        fi
    else
        exit 1
    fi
fi


if [[ -d "$tag_dir" ]]; then
    echo "the dir \"$tag_dir\" already exists, exiting for safety"
    exit 1
fi

mkdir -p "$tag_dir"
(cd "$tag_dir" && wget -c "$tar_gz" -O - | tar --strip-components=1 -xz)

twine check "${tag_dir}/spdx-tools-${version}.tar.gz"  "${tag_dir}/spdx_tools-${version}-py3-none-any.whl"
read -r -p "Do you want to upload? [y/N] " response
case "$response" in
    [yY][eE][sS]|[yY])
        twine upload -r pypi "${tag_dir}/spdx-tools-${version}.tar.gz"  "${tag_dir}/spdx_tools-${version}-py3-none-any.whl"
        ;;
esac
