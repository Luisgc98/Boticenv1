# 🤖 Botic
## ¿Qué es Botic?
```
  Botic es una aplicación donde podemos hacer la calendarización de un Bot para que 
  realice procesos automatizados. Estos bots están programados en Automagica y para 
  usar este aplicativo se necesitan tener ciertos prerequisitos instalados.
```
### Prerequisitos
```
  Para tener la aplicación de Botic instalada de manera local y corriendo de manera 
  adecuada en nuestro ordenador, primero necesitamos tener instalados ciertos prerequisitos:
```
#### 1.- Tener instalado Python en su versión 3.7.4
  - <h4>Instalación en Windows: </h4>
  
    - Para realizar la instalación en su ordenador con Windows, nos dirigimos a la [página oficial de Python](https://www.python.org/downloads/release/python-374/) 
      donde descargaremos el archivo de Python 3.7.4 correspondiente a las especificaciones para su ordenador.
    
    ![imagen windows1](https://miro.medium.com/max/2732/1*b5SZWxlBXkkhmAXjZgUWWg.png)
    
    
    - Una vez descargado este archivo, nos dirigimos a la carpeta donde se ha guardado el archivo,
      y ejecutamos el instalador.
    
    - Nos aparecerá una pantalla como la siguiente: 
    ![imagen windows2](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/images/python/pythonsetup.jpg)

    - Marcamos la casilla que dice "Add Python 3.7 to PATH", esto agregará la ruta de instalación de Python
      a sus variables de entorno. Hacemos click en "Install now" y empezará a instalar el paquete.
      
    - Te aparecerá una pantalla con una barra de progreso como la siguiente:
    
    ![imagen windows3](https://i.ytimg.com/vi/Wx8XU2L2k6Q/maxresdefault.jpg)
    
    - Una vez acabando la instalación presionamos en el botón de "Close", y listo! Ya tendremos Python en su
      versión 3.7.4 instalado en nuestro ordenador.
      
    - Para verificarlo, abra su CMD y escriba el siguiente comando:
    
    ```cmd
        >python -V
    ```
    - Resultado:
    ```cmd
        Python 3.7.4
    ```
    
  - <h4>Instalación en Linux</h4>
  
    - Antes de realizar la instalación en su ordenador, debemos instalar algunos paquetes necesarios para ejecutar
      Python desde la fuente. Sólo copie los siguientes comandos:
      
    ```bash
        $ sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
        $ sudo apt update
    ```
      
    - Después de haber instalado estos paquetes, ahora debemos descargar el código fuente de
      la versión 3.7.4 de la [página oficial de Python](https://www.python.org/downloads/release/python-374/) con el comando wget:
      
    ```bash
        $ wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz
    ```
    
    - Al terminar descargaremos un archivo comprimido "Python-3.7.4.tar.xz". Descomprimimos este archivo con el siguiente comando:
    ```bash
        $ tar -xf Python-3.7.4.tar.xz
    ```
    
    - Nos aparecerá la carpeta del archivo comprimido llamada "Python-3.7.4", entramos a ella, ejecutamos el siguiente comando para
      configurar todo lo necesario, y listo! Ya tenemos Python3.7.4 disponible en su ordenador Linux, sólo falta realizar
      el proceso de construcción en el sistema y guardar los cambios para poder utilizarlo de manera global.
    ```bash
        $ cd Python-3.7.4
        $ sudo ./configure --enable-optimizations --enable-loadable-sqlite-extensions
    ```
    
    - A continuación, inicie el proceso de construcción usando el comando make -j 1. Reemplace el # 1 con la cantidad de núcleos de CPU en su sistema para un tiempo de construcción más rápido. Para saber cuántos nucleos tiene su CPU consulte el comando "nproc".
    ```bash
        $ make -j 1
    ```
    
    - Ahora ejecute el siguiente comando para que haga todos los cambios de la instalación sin sobreescribir otras versiones de Python que tenga instalado.
    ```bash
        $ make altinstall
    ```
    
    - Ya tendrá python3.7 disponible desde cualquier directorio. Para verificarlo escriba el siguiente comando:
    ```bash
        $ python3.7 --version
    ```
    - Resultado:
    ```bash
        $ Python 3.7.4
    ```

#### 2.- Tener una cuenta en GitHub y tener Git instalado en nuestro ordenador.
  - <h4>Registro en GitHub</h4>
  
    - Para registrarnos vamos [a la página de GitHub](https://github.com) donde sólo llenamos el formulario de 
      registro.
      ![github_registro](https://cdn.kastatic.org/ka-perseus-images/b96521d07ec01801331b4eec8d399c84f2131050.png)
     
    - Confirmamos nuestro correo, y listo! ya tendremos nuestro usuario de GitHub.
    
    
  - <h4>Instalación Git en Windows</h4>
  
    - Para instalar Git en nuestro ordenador con  Windows,  ingresar a la liga  https://gitforwindows.org y hacer clic en download,  seguir el proceso de instalación. (en la instalación dar a todo siguiente como viene por defecto).
    ![install_windows](https://scontent.fmex25-1.fna.fbcdn.net/v/t1.15752-9/124402478_3738900932841178_1399512574307556546_n.png?_nc_cat=102&ccb=2&_nc_sid=ae9488&_nc_eui2=AeEImJmYB8cwzYpNqWt-iTw86i94bWmP96nqL3htaY_3qXiRg9ZopWK3KgNkcmQ4C9IDztROUub42GdDNk6XMChR&_nc_ohc=u2mXMp1gmZkAX8XKg0w&_nc_ht=scontent.fmex25-1.fna&oh=2de555a0ea553b47e5a64b14f7f37f74&oe=5FD15A5B)
    
    
  - <h4>Instalación Git en Linux</h4>
    - Para realizar la instalación en nuestro ordenador con Linux, haremos uso de nuestra línea de comandos. 
      Escribimos el siguiente comando para instalar git:
      ```bash
        $ sudo apt-get install git
      ```
    - Y listo! Ya tendremos git instalado en nuestro ordenador, para verificarlo escriba el comando $ git --version.
      Sólo hace falta realizar la configuración inicial.
    
    - Para esta configuración haremos uso del Nombre de Usuario y Correo de nuestra cuenta de GitHub.
      Escriba los siguientes comandos reemplazando los datos de "name" & "email" por sus datos correspondientes.
      ```bash
        $ git config --global user.name "tu_nombre_de_usuario"
        $ git config --global user.email "tu_correo@example.com"
      ```
    - Con esto ya tendremos git configurado y listo para usarlo posteriormente. Para ver los datos de su cuenta de git 
      puede usar el siguiente comando:
      ```bash
        $ git config --global -l
      ```
    - Resultado
      ```bash
        user.name=tu_nombre_de_usuario
        user.email=tu_correo@example.com
      ```
#### 3.- Tener una cuenta en GitLab-git2-condor.
  - Para este paso debemos tener [acceso](https://git2-condor.ddns.net/users/sign_in) de parte del equipo de Condor, de no ser así ponserse en contacto con Condor Consulting.


###### Si ha llegado hasta este punto, ya está listo para instalar Botic en su ordenador, sigas las siguientes instrucciones.


### Instalación de Botic de manera local.
  - <h4>Descarga del repositorio botic-app</h4>
  
    - Para descargar este repositorio haremos uso de los comandos de git, en caso de Windows usa la línea de comandos de git.
      Descargaremos este repositorio de la rama autov3:
    ```bash
        $ git clone -b autov3 https://git2-condor.ddns.net/botic/botic-app.git
    ```
    
    - Se descargará un directorio llamado botic-app, donde se encontrará alojado toda la configuración de la aplicación de Botic.
      Es en este directorio en donde vamos a estar trabajando.
      
  - <h4>Crear el ambiente virtual en botic-app e instalación de la app.</h4>
    
    - Para crear estos ambientes haremos uso de nuestra línea de comandos, en caso de Windows usaremos PowerShell, y en Linux nuestra terminal de siempre. Antes de crear nuestro ambiente virtual nos tenemos que posicionar en la carpeta de botic-app, una vez ahí proseguimos con el
      siguiente paso.
    
    - Para crear ambientes virtuales con Python 3.7.4, usamos el siguiente comando, reemplazando "tu_ambiente_virtual" por el nombre
      que le quieras poner a tu ambiente. En caso de der usuario Windows, basta con poner el comando único "python" sin el numero de la verisón:
    ```bash
        $ # Linux
        $ python3.7 -m venv tu_ambiente_virtual
    ```
    ```cmd
        > # Windows
        > python -m venv tu_ambiente_virtual
    ```
    
    - Terminando el proceso, nos aparecerá una carpeta con el nombre que le hayamos puesto a nuestro ambiente virtual.
      Para activarlo usamos el siguiente comando:
    ```bash
        $ source tu_ambiente_virtual/bin/activate
    ```
    - En caso de ser usuario Windows con el siguiente comando:
    ```cmd
           nombre_de_ambiente\Scripts\activate
    ```
    
    - Al activarlo nos marcará entre parentesis el nombre de nuestro ambiente:
    ```bash
        (tu_ambiente_virtual) $ 
    ```
    
    - Una vez activado nuestro ambiente, proseguimos con la instalación de los requerimientos de la aplicación, aquí usaremos 
      el siguiente comando de pip, y el archivo requirements.txt que se encuentra en el directorio app. En caso de der usuario Windows, basta con poner el comando único "python" sin el numero de la verisón::
    ```bash
        (tu_ambiente_virtual) $ # Linux
        (tu_ambiente_virtual) $ python3.7 -m pip install -r app/requirements.txt
    ```
    ```cmd
        (tu_ambiente_virtual) > # Windows
        (tu_ambiente_virtual) > python -m pip install -r app/requirements.txt
    ```
    
    - Terminando la instalación de los requerimientos, proseguimos a la actualización de la base de datos usando el siguiente comando:
    ```bash
        (tu_ambiente_virtual) $ flask db upgrade
    ```
    - Nos devolverá el siguiente resultado, que nos indica que se hizo la actualización de manera correcta:
    ```bash
        INFO [alembic.runtime.migration] Context impl SQLiteImpl.
        INFO [alembic.runtime.migration] Will assume non-transactional DDL.
    ```
    - Ahora proseguimos a levantar nuestra aplicación de Botic con el siguiente comando:
    ```bash
        (tu_ambiente_virtual) $ flask run
    ```
    
    - Este comando nos devolverá el siguiente resultado, que nos indica que el servidor de nuestra aplicación ya se desplegó, y también nos devuelve la URL donde se encuentra alojada nuestra aplicación:
    ```bash
         * Serving Flask app "botic-app.py" (lazy loading)
         * Environment: production
           WARNING: This is a development server. Do not use it in a production deployment.
           Use a production WSGI server instead.
         * Debug mode: on
         * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
         * Restarting with stat
         * Debugger is active!
         * Debugger PIN: 464-007-621
    ```
    
    - Copiamos la URL que nos devuelve, la pegamos en nuestro navegador. Y listo! Ya tendremos desplegado Botic en nuestro ordenador de manera local. Para parar el sevidor presionamos Ctrl+C.
    
    ![botic_login](https://lh3.googleusercontent.com/-yR_kOgYz4nM/X63GCRVWOvI/AAAAAAAAFVM/vEXDMn0OVIcaGjHZbZL-usHJ7RgjRPmOgCK8BGAsYHg/s0/Captura%2Bde%2Bpantalla%2Bde%2B2020-11-12%2B17-29-07.png)
    
    - Si deseamos volver a levantar el servidor, ya no es necesario hacer todos los pasos anteriores, basta activar nuestro ambiente virtual y con correr nuestra aplicación con "flask run".
    
    
  - <h4>Despliegue de los servicios Rest</h4>
    
    - Para desplegar los servicios Rest de nuestra aplicación, nos posicionamos en la la carpeta de botic-app, activamos nuestro ambiente virtual, y ya no es necesario hacer los pasos anteriores, sólo hay que declarar nuestra variable de entorno FLASK_APP con la variable botic-api y desplegar nuestra aplicación en el puerto 5002, de la siguiente manera:
    ```bash
         (tu_ambiente_virtual) $ export FLASK_APP=botic-api
         (tu_ambiente_virtual) $ flask run --port=5002
    ```
    - En caso de ser usuario Windows, es de la siguiente manera: 
    ```cmd
         (tu_ambiente_virtual) > set FLASK_APP=botic-api
         (tu_ambiente_virtual) > flask run --port=5002
    ```
    
    - Esto nos devolverá una URL similar a la URL donde se aloja nuestra aplicación, cambiando el numero del puerto por el 5002: http://127.0.0.1:5002/
    
    - Si copiamos esta URL agregándole al final la palabra "api" (http://127.0.0.1:5002/api) y pegamos en nuestro navegador, esto nos deplegará una página con todos los servicios Rest de nuestra aplicación, lo que nos indicará que se desplegaron de manera correcta:

    ![api_services](https://lh3.googleusercontent.com/-x-uT9I1ibuE/X7LlC7U0MRI/AAAAAAAAFZI/SJBnJ8iQgLgplSDzvhEwCESA6v5a7kHLwCK8BGAsYHg/s0/Captura%2Bde%2Bpantalla%2Bde%2B2020-11-16%2B14-45-18.png)


###### Si ha llegado hasta este punto, ¡Felicidades! Ya tiene instalado Botic en su ordenador. Para poder desplegar nuevamente el servidor de nuestra aplicación, tendremos que abrir dos terminales, en una correr nuestra aplicación con "flask run", y en otra desplegar nuestros servicios Rest igual que el paso anterior. Ahora puede continuar con la [guía de instalación de Botic Cliente](https://github.com/Luisgc98/Autoenv1).
