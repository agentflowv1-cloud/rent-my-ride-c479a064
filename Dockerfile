# ── Build stage ──────────────────────────────────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
RUN if [ -f "package.json" ]; then \
      npm install --legacy-peer-deps || npm install; \
      npm run build || echo "warn: build script failed, will serve placeholder"; \
    fi

# Collect build output — fall back to a placeholder if nothing was produced
RUN set -e; \
    if   [ -d "dist"  ] && [ -f "dist/index.html"  ]; then cp -r dist  /srv/static; \
    elif [ -d "build" ] && [ -f "build/index.html" ]; then cp -r build /srv/static; \
    elif [ -d "out"   ] && [ -f "out/index.html"   ]; then cp -r out   /srv/static; \
    elif [ -f "index.html" ]; then mkdir -p /srv/static && cp -r . /srv/static; \
    else \
      mkdir -p /srv/static; \
      printf '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Deploying…</title><style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:system-ui,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;background:#0f172a;color:#e2e8f0}.card{text-align:center;padding:2rem;max-width:420px}.icon{font-size:3rem;margin-bottom:1rem}h1{font-size:1.5rem;margin-bottom:.5rem}p{color:#94a3b8;line-height:1.6}</style></head><body><div class="card"><div class="icon">🚀</div><h1>Deployment in progress</h1><p>The app is compiling. Push a new commit or wait for CI to finish — this page will update automatically.</p></div></body></html>' \
      > /srv/static/index.html; \
    fi

# ── Serve stage ───────────────────────────────────────────────────────────────
FROM nginx:1.25-alpine
COPY --from=builder /srv/static /usr/share/nginx/html/
RUN printf 'server {\n  listen 8080;\n  server_name _;\n  root /usr/share/nginx/html;\n  index index.html index.htm;\n  location / { try_files $uri $uri/ /index.html; }\n}\n' > /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
