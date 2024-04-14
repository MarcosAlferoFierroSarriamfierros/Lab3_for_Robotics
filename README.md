# Lab3_for_Rootics
Elaborado por Marcos Alfredo Fierro Sarria y Andrès Camilo Apraez Zamora
A continuaciòn se presenta el desarrollo del taller.
Para llevar a cabo la actividad, es necesario hacer uso de ROS (Robot Operating System), y Matlab. En este caso hemos usado Matlab 2024a. 
Ros trabaja a partir de un sistema de nodos que son independientes entre si que trabajan conjuntamente, y es posible ver como funciona con la herramienta turtlesim, el cual en principio bàsicamente es un simulador de movimientos en 2D. 
## Conexiòn entre Matlab y Ros:
![Captura de pantalla de 2024-04-13 19-47-34](https://github.com/MarcosAlferoFierroSarriamfierros/Lab3_for_Rootics/assets/73545192/4d90fb66-aaf4-45b2-a2d2-065078005dc3)
Se abren dos terminales y se incia el comando "roscore" en una de ellas.
En la otra terminal se ejecuta el comando "rosrun turtlesim turtlesim_node"
Al seguir los pasos anteriores abriremos la ventana de Turtlesim y observaremos una tortuga sobre un fondo azul. Para trabajar con la tortuga desde Matlab, hemos hecho dos scripts, uno que se conecta con el nodo maestro es decir "lab3.m" y otro que realiza la lectura de la posiciòn de la lectura despuès de haberla desplazado, es decir "script3.m".
```matlab
rosinit; %Conexión con nodo maestro
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Creación publicador
velMsg = rosmessage(velPub); %Creación de mensaje
velMsg.Linear.X = 1; %Valor del mensaje
send(velPub,velMsg); %Envío
pause(1)
