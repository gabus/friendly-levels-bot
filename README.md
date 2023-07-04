### What's this?
Leveling bot for Discord. Meant to be flexible and rewarding 

## Project setup

```bash
cp .env.example .env
```

### Running project with docker compose (clean rebuild)
```bash
docker-compose up
```

### Running containers separately 
```bash
docker compose up postgres 
docker compose up bot 
```

### Rebuild images and containers
```bash
docker-compose down
docker compose up --build --force-recreate
or
docker compose up bot --build --force-recreate
docker compose up postgres --build --force-recreate
```


```complains
bugs with docker-compose
* there's no `docker compose project-name down` -- only docker compose down. 
But there's docker compose up project-name, which allows to build specific project.

* docker compose up doesn't have any way to pass arguments via CLI. `build` and `up --build` does

* `tty: true` is not set by default. This is obvious flag to have

* `depends_on` doesn't have anything to validate if dependency project is alive at all..   

* `depends_on` will build all dependency projects but won't tear them down when service is stopped. 
Leaving dead containers running  

* CMD vs ENTRYPOINT. "meant to be used this way" is not a reason to have both of them. Confusing

* exec vs run vs build  confusion
```