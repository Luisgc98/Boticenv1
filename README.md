# 🤖 Botic
### ¿Qué es Botic?
```
  Botic es una aplicación donde podemos hacer la calendarización de un Bot para realizar 
  procesos automatizados. Estos bots están programados en Automagica y para usar 
  este aplicativo se necesitan tener ciertos prerequisitos instalados.
```
#### Prerequisitos
```
  Para tener la aplicación de Botic instalada de manera local y corriendo de manera adecuada en nuestro
  ordenador, primero necesitamos tener instalados ciertos prerequisitos:
```
### - Tener instalado Python en su versión 3.7.4
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
