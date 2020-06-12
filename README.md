# Proyecto de Software: Venta de comida a domicilio

## UNAM, Facultad de Ciencias | Ingeniería de Software 2020-2

Repositorio para el proyecto del curso de ingeniería de software de Hanna Oktaba

### Instalar el proyecto

* Clona el repositorio

```command-line
git clone https://github.com/ramseslopez/Turing-s-Food.git
cd Turing-s-Food
```

* Crear un entorno virtual de la siguiete manera

OS X y Linux

```command-line
python3 -m venv env
```

Windows

```command-line
python -m venv env
```

* Activar el entorno virtual:

OS X y Linux

```command-line
source env/bin/activate
```

Windows:

```command-line
env\Scripts\activate
```

* Instalar dependencias de desarrollo

```command-line
pip install -r requirements/local.txt
```

* Crear un archivo llamado `.env` con todas las variables de entorno a utilizar en el proyecto (ver [.env.example](.env.example) para ver un ejemplo de este archivo)

* Ejecutar migraciones

```command-line
python manage.py migrate
```

> No olvides desactivar tu entorno virtual cada vez que terminas de trabajar en el proyecto con ´deactivate´

### Ejecutar el proyecto

* Activar el entorno virtual:

OS X y Linux

```command-line
source env/bin/activate
```

Windows:

```command-line
env\Scripts\activate
```

Correr el servidor

```command-line
python manage.py runserver
```

Desactivar entorno virtual al finalizar

```command-line
deactivate
```
