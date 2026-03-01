FROM python:3.12-bookworm

WORKDIR /app

# Install required OS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft GPG key (Bookworm-safe method)
RUN curl https://packages.microsoft.com/keys/microsoft.asc \
      | gpg --dearmor \
      | tee /usr/share/keyrings/microsoft-prod.gpg > /dev/null

# Add Microsoft SQL Server repository (Bookworm-safe)
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] \
      https://packages.microsoft.com/debian/12/prod bookworm main" \
      > /etc/apt/sources.list.d/microsoft-prod.list

# Install ODBC Driver 18
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

EXPOSE 8000

CMD ["./start.sh"]