FROM oven/bun:1 AS base
WORKDIR /app

FROM base AS install
COPY package.json bun.lock .
RUN bun install --frozen-lockfile

FROM base AS build
COPY . .
COPY --from=install /app/node_modules node_modules
RUN bun run build

FROM caddy:2-alpine AS release
COPY --from=build /app/dist /app
COPY deploy/Caddyfile /etc/caddy

EXPOSE 80
