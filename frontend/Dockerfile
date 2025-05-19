FROM node:16-alpine

WORKDIR /app

# 1) Skopiuj package.json (i – jeśli masz – package-lock.json)
COPY package.json ./
# jeśli masz lockfile, lepiej:
# COPY package.json package-lock.json ./

# 2) Zainstaluj zależności
#    - jeśli masz lockfile: RUN npm ci --silent
#    - jeśli nie masz:     RUN npm install --silent
RUN npm install --silent

# 3) Skopiuj resztę kodu
COPY . .

EXPOSE 3000
CMD ["npm", "run", "serve"]