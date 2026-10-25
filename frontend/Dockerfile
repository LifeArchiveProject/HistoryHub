FROM node:20-alpine AS base
WORKDIR /app

FROM base AS install
COPY package.json package-lock.json ./
RUN npm ci --include=optional --no-fund --no-audit

FROM base AS build
ARG BACKEND_URL_ARG=http://localhost:8899
ENV VITE_DEFAULT_BACKEND_URL=${BACKEND_URL_ARG}
COPY . .
COPY --from=install /app/node_modules node_modules
RUN npm run build

FROM caddy:2-alpine AS release
COPY --from=build /app/dist /app
COPY deploy/Caddyfile /etc/caddy

EXPOSE 80
