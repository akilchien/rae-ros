#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.time import Time

from std_msgs.msg import ColorRGBA
from rae_msgs.msg import LEDControl
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist

blinking = True

class CarDemoNode(Node):

    def __init__(self):
        super().__init__('car_demo_node')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.publisher_led = self.create_publisher(LEDControl, 'leds', 10)

        self.bridge = CvBridge()

    def listener_callback(self, msg):
        global blinking
        linear_speed = msg.linear.x
        angular_speed = msg.angular.z


        # Set LEDs based on battery level
        # Define colors for LEDs
        colors = {
            "white": ColorRGBA(r=1.0, g=1.0, b=1.0, a=1.0),
            "yellow": ColorRGBA(r=1.0, g=1.0, b=0.0, a=1.0),
            "red": ColorRGBA(r=1.0, g=0.0, b=0.0, a=1.0),
            "blue": ColorRGBA(r=0.0, g=0.0, b=1.0, a=1.0)
        }



        # Create and publish LEDControl message for each LED
        led_msg = LEDControl()
        led_msg.header.stamp = self.get_clock().now().to_msg()
        led_msg.data = [ColorRGBA(r=0.0, g=0.0, b=0.0, a=0.0)]*40
        for i in range(39):
            led_msg.single_led_n = 0
            led_msg.control_type = 2 
            if i < 8:
                color = "white"
                led_msg.data[i]=(colors[color])
            if i >9 and i < 14 and angular_speed > 0.0 and blinking==True:
                color = "yellow"
                led_msg.data[i]=(colors[color])
            if i > 20 and i < 29 and linear_speed < 0.0:
                color = "red"
                led_msg.data[i]=(colors[color])
            if i> 34 and i < 39 and angular_speed < 0.0 and blinking==True:
                color = "yellow"
                led_msg.data[i]=(colors[color])

        blinking = not blinking
        self.publisher_led.publish(led_msg)


def main(args=None):
    rclpy.init(args=args)

    car_demo_node = CarDemoNode()

    rclpy.spin(car_demo_node)

    # Destroy the node explicitly
    car_demo_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()