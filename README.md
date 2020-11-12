# 🤖 Botic
## ¿Qué es Botic?
```
  Botic es una aplicación donde podemos hacer la calendarización de un Bot para realizar 
  procesos automatizados. Estos bots están programados en Automagica y para usar 
  este aplicativo se necesitan tener ciertos prerequisitos instalados.
```
### Prerequisitos
```
  Para tener la aplicación de Botic instalada de manera local y corriendo de manera 
  adecuada en nuestro ordenador, primero necesitamos tener instalados ciertos prerequisitos:
```
#### - Tener instalado Python en su versión 3.7.4
  - Instalación en Windows:
  
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
    
  - Instalación en Linux
  
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
        $ ./configure --enable-optimizations
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

#### - Tener una cuenta en GitHub y tener Git instalado en nuestro ordenador.
  - Registro en GitHub
    - Para registrarnos vamos [a la página de GitHub](https://github.com) donde sólo llenamos el formulario de 
      registro.
      ![github_registro](https://cdn.kastatic.org/ka-perseus-images/b96521d07ec01801331b4eec8d399c84f2131050.png)
     
    - Confirmamos nuestro correo, y listo! ya tendremos nuestro usuario de GitHub.
    
    
  - Instalación Git en Windows
    - Para instalar Git en nuestro ordenador con  Windows,  ingresar a la liga  https://gitforwindows.org y hacer clic en download,  seguir el proceso de instalación. (en la instalación dar a todo siguiente como viene por defecto).
    ![install_windows](https://scontent.fmex25-1.fna.fbcdn.net/v/t1.15752-9/124402478_3738900932841178_1399512574307556546_n.png?_nc_cat=102&ccb=2&_nc_sid=ae9488&_nc_eui2=AeEImJmYB8cwzYpNqWt-iTw86i94bWmP96nqL3htaY_3qXiRg9ZopWK3KgNkcmQ4C9IDztROUub42GdDNk6XMChR&_nc_ohc=u2mXMp1gmZkAX8XKg0w&_nc_ht=scontent.fmex25-1.fna&oh=2de555a0ea553b47e5a64b14f7f37f74&oe=5FD15A5B)
    
    
  - Instalación Git en Linux
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
#### - Tener una cuenta en GitLab-git2-condor.
  - Para este paso debemos tener [acceso](https://git2-condor.ddns.net/users/sign_in) departe del equipo de Condor, de no ser así ponserse en contacto con Condor Consulting.


###### Si ha llegado hasta este punto, ya está listo para instalar Botic en su ordenador, sigas las siguientes instrucciones.


### Instalación de Botic de manera local.
  - Descarga del repositorio botic-app
  
    - Para descargar este repositorio haremos uso de los comandos de git, en caso de Windows usa la línea de comandos de git.
      Descargaremos este repositorio de la rama autov3:
    ```bash
        $ git clone -b autov3 https://git2-condor.ddns.net/botic/botic-app.git
    ```
    
    - Se descargará un directorio llamado botic-app, donde se encontrará alojado toda la configiración de la aplicación de Botic.
      Es en este directorio en donde vamos a estar trabajando.
      
  - Crear el ambiente virtual en botic-app
    
    - Antes de crear nuestro ambiente virtual nos tenemos que posicionar en la carpeta de botic-app, una vez ahí proseguimos con el
      siguiente paso.
    
    - Para crear ambientes virtuales con Python 3.7.4, usamos el siguiente comando, reemplazando "tu_ambiente_virtual" por el nombre
      que le quieras poner a tu ambiente virtual:
    ```bash
        $ python3.7 -m venv tu_ambiente_virtual
    ```
    
    - Terminando el proceso, nos aparecerá una carpeta con el nombre que le hayamos puesto a nuestro ambiente virtual.
      Para activarlo usamos el siguiente comando:
    ```bash
        $ source tu_ambiente_virtual/bin/activate
    ```
    - Al activarlo nos marcará entre parentesis el nombre de nuestro ambiente virtual:
    ```bash
        (tu_ambiente_virtual) $ 
    ```
    
    - Una vez activado nuestro ambiente, proseguimos con la instalación de los requerimientos de la aplicación, aquí usaremos 
      el siguiente comando de pip, y el archivo requirements.txt que se encuentra en el directorio de app:
    ```bash
        (tu_ambiente_virtual) $ python3.7 -m pip install -r app/requirements.txt
    ```
