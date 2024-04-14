#!/usr/bin/env python

import rospy
import sys
import tty
import termios
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative

# Definir los valores de las teclas
KEY_W = 119
KEY_S = 115
KEY_A = 97
KEY_D = 100
KEY_R = 114
KEY_SPACE = 32

# Definir las velocidades lineal y angular
LINEAR_VEL = 1.0
ANGULAR_VEL = 1.0

# Función para leer la tecla presionada
def get_key():
    tty.setraw(sys.stdin.fileno())
    key = ord(sys.stdin.read(1))
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
    return key

# Función para mover la tortuga hacia adelante
def move_forward(pub):
    twist = Twist()
    twist.linear.x = LINEAR_VEL
    pub.publish(twist)

# Función para mover la tortuga hacia atrás
def move_backward(pub):
    twist = Twist()
    twist.linear.x = -LINEAR_VEL
    pub.publish(twist)

# Función para girar la tortuga en sentido horario
def turn_clockwise(pub):
    twist = Twist()
    twist.angular.z = -ANGULAR_VEL
    pub.publish(twist)

# Función para girar la tortuga en sentido antihorario
def turn_counterclockwise(pub):
    twist = Twist()
    twist.angular.z = ANGULAR_VEL
    pub.publish(twist)

# Función para teleportar la tortuga a su posición y orientación centrales
def reset_position():
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleport_absolute = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        teleport_absolute(5.54, 5.54, 0.0)
    except rospy.ServiceException as e:
        print("Service call failed:", e)

# Función para teleportar la tortuga relativa a su posición y orientación actuales
def rotate_180_degrees():
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        teleport_relative = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        teleport_relative(0.0, 0.0, 3.14159)
    except rospy.ServiceException as e:
        print("Service call failed:", e)

# Función principal
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
