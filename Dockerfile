# =========================================================
# Stage 1 — Build des assets front (Tailwind CSS)
# =========================================================
FROM node:20-alpine AS css-builder

WORKDIR /build

COPY package.json package-lock.json ./
RUN npm ci

COPY tailwind.config.js ./
COPY static ./static
COPY home ./home
COPY jobs ./jobs

RUN npm run build:css

# =========================================================
# Stage 2 — Application Django
# =========================================================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --retries 5 --timeout 120 -r requirements.txt

COPY . .

# On récupère le CSS compilé du stage précédent
COPY --from=css-builder /build/static/dist /app/static/dist

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
