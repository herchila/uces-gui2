# Usa la imagen oficial de PostgreSQL
FROM postgres:latest

# Configura las variables de entorno para PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=your_password
ENV POSTGRES_DB=gui2_crud

# Exponer el puerto de PostgreSQL
EXPOSE 5432

# Copia el archivo de configuración opcionalmente (si necesitas modificar la configuración predeterminada de PostgreSQL)
# COPY path/to/your/custom/postgresql.conf /etc/postgresql/postgresql.conf

# Comando de inicio
CMD ["postgres"]
