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
Còdigo correspondiente a "lab3.m":
```matlab
rosinit; %Conexión con nodo maestro
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); 
velMsg = rosmessage(velPub); %cramos el mensaje
velMsg.Linear.X = 1; %
send(velPub,velMsg); %nviamos el mensaje
pause(1)
``` 
Còdigo de "script3.m":
```matlab
%Nos suscribimos al tema de turtle1
poseSubscriber = rossubscriber('/turtle1/pose');

pause(1); 
% Mensaje con datos de a pose
latestPose = receive(poseSubscriber, 1); % Se hace una pausa hasta recibir un mensaje

% Mostrar la posición y orientación de la tortuga
disp('Última pose de Turtle1:');
disp(['Posición (x, y): ', num2str(latestPose.X), ', ', num2str(latestPose.Y)]);
disp(['Orientación (z): ', num2str(latestPose.Theta)]);
teleportClient = rossvcclient('/turtle1/teleport_absolute');
req = rosmessage(teleportClient);

% Ponemos una posiciòn random en la tortuga para ver que se mueva
req.X = 5; 
req.Y = 5; 
req.Theta = pi/2; % en rads
resp = call(teleportClient, req);
% Finalizamos nodo maestro de ROS
rosshutdown;
```

Esto nos mostrarà la coordenadas de la tortuguita.
## Conexiòn entre Python y Ros
![Captura de pantalla de 2024-04-14 14-47-24](https://github.com/MarcosAlferoFierroSarriamfierros/Lab3_for_Rootics/assets/73545192/a2c5d669-bac3-4a00-931a-758531b1d14d)

A diferencia de la guìa de laboratorio, lo que hicimos fue realizar el script en python para mover la tortuga en el turtlesim. Posteriormente abrimos 3 terminales:
- En la primera terminal se ejecuta "roscore".
- En la segunda se ejecuta "rosrun turtlesim turtlesim_node"
- Finalmente, en la tercera buscamos el archivo de python con el nombre myTeleopKey.py y lo ejecutamos
Una vez hecho esto se podrà mover la tortuga con las teclas como se pide en la guìa.
El còdigo es el que se muestra:
```python

import rospy
import sys
import tty
import termios
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative
KEY_W = 119
KEY_S = 115
KEY_A = 97
KEY_D = 100
KEY_R = 114
KEY_SPACE = 32

# val_velocities
LINEAR_VEL = 1.0
ANGULAR_VEL = 1.0

# Funkziu to read board
def get_key():
    tty.setraw(sys.stdin.fileno())
    key = ord(sys.stdin.read(1))
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
    return key

# adelante
def move_forward(pub):
    twist = Twist()
    twist.linear.x = LINEAR_VEL
    pub.publish(twist)

# back
def move_backward(pub):
    twist = Twist()
    twist.linear.x = -LINEAR_VEL
    pub.publish(twist)

# girar horario
def turn_clockwise(pub):
    twist = Twist()
    twist.angular.z = -ANGULAR_VEL
    pub.publish(twist)

# girar antihorario
def turn_counterclockwise(pub):
    twist = Twist()
    twist.angular.z = ANGULAR_VEL
    pub.publish(twist)

# resetear posiciòn
def reset_position():
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleport_absolute = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        teleport_absolute(5.54, 5.54, 0.0)
    except rospy.ServiceException as e:
        print("Service call failed:", e)

def rotate_180_degrees():
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        teleport_relative = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        teleport_relative(0.0, 0.0, 3.14159)
    except rospy.ServiceException as e:
        print("Service call failed:", e)

# main
def main():
    rospy.init_node('myTeleopKey', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    try:
        while not rospy.is_shutdown():
            key = get_key()
            if key == KEY_W:
                move_forward(pub)
            elif key == KEY_S:
                move_backward(pub)
            elif key == KEY_A:
                turn_counterclockwise(pub)
            elif key == KEY_D:
                turn_clockwise(pub)
            elif key == KEY_R:
                reset_position()
            elif key == KEY_SPACE:
                rotate_180_degrees()
            else:
                pass
    except Exception as e:
        print(e)
    finally:
        twist = Twist()
        pub.publish(twist)

if __name__ == '__main__':
    main()
```
