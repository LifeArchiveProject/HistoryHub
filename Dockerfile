FROM oven/bun:1 AS base
WORKDIR /app

FROM base AS install
COPY package.json bun.lock .
RUN bun install

FROM base AS build
ARG BACKEND_URL_ARG=http://localhost:8899
ENV VITE_DEFAULT_BACKEND_URL=${BACKEND_URL_ARG}
COPY . .
COPY --from=install /app/node_modules node_modules
RUN bun run build

FROM caddy:2-alpine AS release
COPY --from=build /app/dist /app
COPY deploy/Caddyfile /etc/caddy

EXPOSE 80
