#!/usr/bin/env bash

set -euo pipefail


# ============================================================
# Python
# ============================================================

PYTHON_VERSION="3.10.12"

echo "Setting up Python environment..."


# ------------------------------------------------------------
# Move to repository root
# ------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"


# ------------------------------------------------------------
# Check whether a virtual environment is already active
# ------------------------------------------------------------

USE_CURRENT_VENV=false

if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    echo
    echo "A virtual environment is already active:"
    echo "    $VIRTUAL_ENV"
    echo

    read -r -p "Install ModelBridge dependencies into this environment? [y/N] " answer

    case "$answer" in
        [yY]|[yY][eE][sS])
            USE_CURRENT_VENV=true
            ;;
        *)
            echo "A separate ModelBridge .venv will be used."
            ;;
    esac
fi


# ------------------------------------------------------------
# Install uv if necessary
# ------------------------------------------------------------

if command -v uv >/dev/null 2>&1; then

    UV_CMD="$(command -v uv)"

elif [[ -x "$SCRIPT_DIR/.uv-bin/uv" ]]; then

    UV_CMD="$SCRIPT_DIR/.uv-bin/uv"

else

    echo
    echo "uv not found. Installing uv..."

    UV_DIR="$SCRIPT_DIR/.uv-bin"
    mkdir -p "$UV_DIR"

    if command -v curl >/dev/null 2>&1; then

        curl -LsSf https://astral.sh/uv/install.sh \
            | env UV_UNMANAGED_INSTALL="$UV_DIR" sh

    elif command -v wget >/dev/null 2>&1; then

        wget -qO- https://astral.sh/uv/install.sh \
            | env UV_UNMANAGED_INSTALL="$UV_DIR" sh

    else

        echo "ERROR: Neither curl nor wget is available."
        exit 1

    fi

    UV_CMD="$UV_DIR/uv"

fi


echo
echo "Using uv:"
"$UV_CMD" --version


# ------------------------------------------------------------
# Choose Python environment
# ------------------------------------------------------------

if [[ "$USE_CURRENT_VENV" == true ]]; then

    # User explicitly chose the currently active environment
    TARGET_PYTHON="$(command -v python)"

    echo
    echo "Using existing virtual environment:"
    echo "    $VIRTUAL_ENV"

    echo "Using Python:"
    "$TARGET_PYTHON" --version
    echo "    $TARGET_PYTHON"

    CURRENT_VERSION="$("$TARGET_PYTHON" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"

    if [[ "$CURRENT_VERSION" != "$PYTHON_VERSION" ]]; then
        echo
        echo "NOTE: This environment uses Python $CURRENT_VERSION."
        echo "ModelBridge's tested Python version is $PYTHON_VERSION."
        echo "Continuing because you chose to use the current environment."
    fi

else

    # --------------------------------------------------------
    # Create/reuse ModelBridge .venv with Python 3.10.12
    # --------------------------------------------------------

    RECREATE_VENV=false

    if [[ -x ".venv/bin/python" ]]; then

        EXISTING_VERSION="$(".venv/bin/python" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"

        if [[ "$EXISTING_VERSION" == "$PYTHON_VERSION" ]]; then

            echo
            echo "Existing .venv found with Python $PYTHON_VERSION."

        else

            echo
            echo "Existing .venv uses Python $EXISTING_VERSION."
            echo "Recreating it with Python $PYTHON_VERSION."

            RECREATE_VENV=true

        fi

    else

        RECREATE_VENV=true

    fi


    if [[ "$RECREATE_VENV" == true ]]; then

        echo
        echo "Creating .venv with Python $PYTHON_VERSION..."

        "$UV_CMD" venv \
            --python "$PYTHON_VERSION" \
            --clear \
            .venv

    fi


    TARGET_PYTHON="$SCRIPT_DIR/.venv/bin/python"

    echo
    echo "Using Python:"
    "$TARGET_PYTHON" --version
    echo "    $TARGET_PYTHON"

fi


# ------------------------------------------------------------
# Install Python dependencies
# ------------------------------------------------------------

echo
echo "Installing Python dependencies..."

"$UV_CMD" pip install \
    --python "$TARGET_PYTHON" \
    numpy==1.23.3 \
    scipy==1.9.1 \
    pandas==1.5.3 \
    matplotlib==3.6.0


# ------------------------------------------------------------
# Verify
# ------------------------------------------------------------

echo
echo "Verifying Python dependencies..."

"$TARGET_PYTHON" -c "
import numpy
import scipy
import pandas
import matplotlib

print('numpy:      ', numpy.__version__)
print('scipy:      ', scipy.__version__)
print('pandas:     ', pandas.__version__)
print('matplotlib: ', matplotlib.__version__)
"


# ------------------------------------------------------------
# Done
# ------------------------------------------------------------

echo
echo "Python environment setup complete."

if [[ "$USE_CURRENT_VENV" == false ]]; then
    echo
    echo "Activate it with:"
    echo "    source .venv/bin/activate"
fi


# ============================================================
# Julia
# ============================================================

# Julia dependencies will be added here later.
#
# Example:
#
# julia -e '
# using Pkg
# Pkg.activate(".julia_env")
#
# Pkg.add([
#     "ITensors",
#     "ITensorMPS",
# ])
#
# Pkg.precompile()
# '


# ============================================================
# Done
# ============================================================

echo
echo "Environment setup complete."
echo
echo "Activate Python with:"
echo "    source .venv/bin/activate"