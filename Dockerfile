# Independent recomputation image (RP Part VII; P5 gate; E-13).
#
# One command reproduces the reference computation from the committed tree:
#
#   docker build -t tly-recompute .
#   docker run --rm tly-recompute                       # default epoch
#   docker run --rm tly-recompute 2026-08-17T12:00:00+00:00 > print.json
#
# The container has NO network at compute time by construction of the code
# path (AC-1.5: the loader hash-verifies committed snapshots and computes
# offline); run with --network=none to enforce it at the container level
# too. Byte-identical output across hosts is the P5 property — see
# docs/REPRODUCE_FIXING.md for the comparison protocol.

FROM python:3.12-slim

WORKDIR /tly

# The compute path is stdlib-only; install only the package itself.
COPY pyproject.toml LICENSE README.md ./
COPY tly/ tly/
COPY data/ data/
COPY seed/ seed/
RUN pip install --no-cache-dir --no-deps .

ENTRYPOINT ["python", "-m", "tly.pipeline"]
CMD ["2026-08-17T12:00:00+00:00"]
