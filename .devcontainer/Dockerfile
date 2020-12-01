FROM python:3.9

ARG PACKAGE_LIST="\
    apt-transport-https \
    apt-utils \
    ca-certificates \
    curl \
    dialog \
    git \
    gnupg2 \
    iproute2 \
    jq \
    less \
    libc6 \
    libgcc1 \
    libgssapi-krb5-2 \
    libicu[0-9][0-9] \
    liblttng-ust0 \
    libssl1.1 \
    libstdc++6 \
    lldb \
    locales \
    lsb-release \
    lsof \
    man-db \
    openssh-client \
    procps \
    sudo \
    unzip \
    vim \
    wget \
    zlib1g"

# Install packages
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends ${PACKAGE_LIST}


ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create user
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd -s /bin/bash --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}

# Give user sudo permissions
RUN echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# Locale generation
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen


ARG PYTHON_PACKAGE_LIST="\
    pylint \
    flake8 \
    autopep8 \
    black \
    yapf \
    mypy \
    pydocstyle \
    pycodestyle \
    bandit \
    pipenv \
    virtualenv"

# Install Python packages
RUN pip3 install ${PYTHON_PACKAGE_LIST}
