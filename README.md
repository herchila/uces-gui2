# GUI 2

## Docker

**Construir la Imagen**
```bash
docker build -t postgres-gui2-crud .
```

**Ejecutar un Contenedor desde la Imagen**
```bash
docker run -d --name postgres-container -p 5432:5432 postgres-gui2-crud
```

* `-d`: Ejecuta el contenedor en segundo plano.
* `--name postgres-container`: Le da un nombre al contenedor (puedes cambiarlo).
* `-p 5432:5432`: Mapea el puerto 5432 del contenedor al puerto 5432 de tu máquina local.
* `postgres-gui2-crud`: Es el nombre de la imagen que construiste.

**Verifica que el Contenedor Está Corriendo**
```bash
docker ps

CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS         PORTS                    NAMES
abcd1234       postgres-gui2-crud  "docker-entrypoint.s…"   5 seconds ago   Up 5 seconds   0.0.0.0:5432->5432/tcp   postgres-container
```

**Conéctate a PostgreSQL**
```bash
psql -U postgres -d gui2_crud -h localhost
```

**Desde Django**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gui2_crud',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Parar o Reiniciar el Contenedor**
```bash
docker stop postgres-container
docker start postgres-container
```

**Eliminar el Contenedor**
```bash
docker rm postgres-container
```

**Eliminar la Imagen**
```bash
docker rmi postgres-gui2-crud
```
