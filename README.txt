# Caso “Club Videojuegos”

¡¡en proceso de modificaciones!! por lo que los pasos para ejecutar el proyecto podrian variar y no ser los mismo indicados...


Creado por Lilyana Orellana Saavedra para certificación fullstack python





Paso para ejecutar el proyecto:
-------------------------------


1) Crear un ambiente virtual, activarla e instalar las dependencias usando:

    >    pip install -r requirements.txt


2) Crear una base de datos en Postgres llamada: 
    > club_videojuegos  

3) Cambiarse a la carpeta club_videojuegos


4) Ejecutar las migraciones:

    > python3 manage.py makemigrations
    >
    > python3 manage.py migrate



5) Ejecutar el proyecto:

    > python manage.py runserver



Datos de usuarios:
------------------

a) Super Usuario:


   admin                    contraseña:admin   



b) Usuarios: 

pablo@gmail.com           contraseña: 12345678     
diana18@gmail.com         contraseña: 12345678       
lorena12@gmail.com        contraseña: 12345678             
liilyth2575@gmail.com     contraseña: 12345678   


Consideraciones

#La vista de resumen de las multas generadas la inclui en la misma vista de reporte de arriendos, quedo inconclusa pues no me dio tiempo de hacer que las multas quedaran en el diccionario y por lo tanto sean vistas en la pantalla.
