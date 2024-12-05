ARG PY_VER
ARG PYTHON_ENV
ARG SETUP_FOLDER

# STAGE 1: Python
FROM python:${PY_VER:-3.12}-slim-bookworm AS stg1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-launchpadlib \
    nano \
    curl \
    wget \
    gdebi \
    xdg-utils \
    git \
    libgit2-dev \
    gcc \
    gfortran \
    libglpk40 \
    htop \
    jq \
    libxtst6 \
    libxt6 \
    xdg-utils \
    tar \
    bzip2 \
    unzip \
    openssh-server \
    build-essential \
    libedit-dev \
    && rm -rf /var/lib/apt/lists/*

ARG PYTHON_ENV
ENV PYTHON_ENV=${PYTHON_ENV}

ARG SETUP_FOLDER
ENV SETUP_FOLDER=${SETUP_FOLDER}

ENV PATH="/opt/${PYTHON_ENV}/bin:$PATH"

# copy files
RUN mkdir ${SETUP_FOLDER}
COPY pypkgs.txt /${SETUP_FOLDER}/

# activate python environment
RUN python3 -m venv /opt/${PYTHON_ENV}

# install uv globally
RUN pip install uv

# install python packages in virtual env
RUN uv pip install --no-cache -r ./${SETUP_FOLDER}/pypkgs.txt

# STAGE 2: final build
FROM python:${PY_VER:-3.12}-slim-bookworm

ARG PYTHON_ENV
ENV PYTHON_ENV=${PYTHON_ENV}

COPY --from=stg1 /opt/${PYTHON_ENV} /opt/${PYTHON_ENV}

# expose port
EXPOSE 8888
ENV PATH="/opt/${PYTHON_ENV}/bin:$PATH"