FROM docker.io/mambaorg/micromamba:1.5.5-bookworm-slim AS micromamba
FROM micromamba AS builder

RUN \
    --mount=type=cache,sharing=private,target=/home/mambauser/.mamba/pkgs,uid=57439,gid=57439 \
    --mount=type=cache,sharing=private,target=/opt/conda/pkgs,uid=57439,gid=57439 \
    micromamba -y -n base install -c conda-forge python=3.12.1 nibabel=5.2.0 numpy=1.26.3 tqdm=4.66.1 pydantic=2.6.0

ARG SRCDIR=/home/mambauser/pl-visual-dataset
RUN mkdir "${SRCDIR}"
WORKDIR ${SRCDIR}

COPY requirements.txt .
ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN pip install -r requirements.txt

COPY --chown=mambauser:mambauser . .
ARG extras_require=none
RUN pip install ".[${extras_require}]" && cd / && rm -rf ${SRCDIR}
WORKDIR /

CMD ["visualdataset"]

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="Create ChRIS Visual Dataset" \
      org.opencontainers.image.description="Prepare a dataset for visualization with ChRIS_ui"
