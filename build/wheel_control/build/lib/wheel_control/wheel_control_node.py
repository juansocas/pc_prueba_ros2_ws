import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

class WheelControl(Node):
    def __init__(self):
        super().__init__('wheel_control')

        # Publicadores para cada rueda
        self.front_left_wheel_pub = self.create_publisher(Float64, 'drivewhl_fl_joint/command', 10)
        self.front_right_wheel_pub = self.create_publisher(Float64, 'drivewhl_fr_joint/command', 10)
        self.back_left_wheel_pub = self.create_publisher(Float64, 'drivewhl_bl_joint/command', 10)
        self.back_right_wheel_pub = self.create_publisher(Float64, 'drivewhl_br_joint/command', 10)

        # Suscribirse al tópico de comandos
        self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)

        # Velocidades actuales de las ruedas
        self.current_left_speed = 0.0
        self.current_right_speed = 0.0

    def cmd_vel_callback(self, msg):
        target_left_speed = msg.linear.x - msg.angular.z
        target_right_speed = msg.linear.x + msg.angular.z

        # Desacelerar suavemente
        if self.current_left_speed > target_left_speed:
            self.current_left_speed -= 0.1
        elif self.current_left_speed < target_left_speed:
            self.current_left_speed += 0.1

        if self.current_right_speed > target_right_speed:
            self.current_right_speed -= 0.1
        elif self.current_right_speed < target_right_speed:
            self.current_right_speed += 0.1

        # Publicar las velocidades
        self.front_left_wheel_pub.publish(Float64(data=self.current_left_speed))
        self.front_right_wheel_pub.publish(Float64(data=self.current_right_speed))
        self.back_left_wheel_pub.publish(Float64(data=self.current_left_speed))
        self.back_right_wheel_pub.publish(Float64(data=self.current_right_speed))

def main(args=None):
    rclpy.init(args=args)
    node = WheelControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
