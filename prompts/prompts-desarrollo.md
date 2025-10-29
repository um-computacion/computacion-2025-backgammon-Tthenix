## Prompt

@docker-compose-simple.yml @docker-compose.yml @Dockerfile
"viendo cómo lo usaste, el Dockerfile es innecesario, te alcanza con una buena configuración del compose,\n\nme diho ese comentario mi profesor, podes mejorar mi docker?"

## Respuesta generada

Se consolidó la configuración Docker eliminando la necesidad de `Dockerfile` y del archivo duplicado `docker-compose-simple.yml`. Ahora `docker-compose.yml` usa la imagen oficial `redis:7-alpine` con una configuración simple y efectiva por línea de comandos: `appendonly yes`, `maxmemory 256mb` y política `allkeys-lru`. Se mantuvieron `volumes`, `restart`, `healthcheck` y `networks` para un servicio robusto y fácil de ejecutar.

Cambios aplicados:

- Eliminado `Dockerfile` innecesario.
- Eliminado `docker-compose-simple.yml` para evitar duplicación.
- Actualizado `docker-compose.yml` para usar `image: redis:7-alpine` y `command` con flags de configuración.

Cómo ejecutar:

1. `docker compose down --remove-orphans` (para detener y limpiar servicios previos).
2. `docker compose up -d` (levanta Redis con la nueva configuración).
