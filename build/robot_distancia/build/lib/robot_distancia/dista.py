#!/usr/bin/env python3

import serial
import serial.tools.list_ports
import crcmod.predefined
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class SensorDistanciaNode(Node):

    def __init__(self):
        super().__init__('sensor_distancia_node')
        self.publisher_ = self.create_publisher(Float32, 'distancia', 10)
        self.timer_ = self.create_timer(1.0, self.timer_callback)

        self.evo_port_ = self.find_evo()
        if self.evo_port_ == 'NULL':
            self.get_logger().info("Sorry couldn't find the Evo. Exiting.")
            rclpy.shutdown()
        else:
            self.evo_ = self.open_evo(self.evo_port_)
            self.counter_ = 0

    def find_evo(self):
        self.get_logger().info('Scanning all live ports on this PC')
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "5740" in p[2]:
                self.get_logger().info('Evo found on port ' + p[0])
                return p[0]
        return 'NULL'

    def open_evo(self, portname):
        self.get_logger().info('Attempting to open port: ' + portname)
        evo = serial.Serial(portname, baudrate=115200, timeout=2)
        set_bin = (0x00, 0x11, 0x02, 0x4C)
        evo.flushInput()
        evo.write(set_bin)
        evo.flushOutput()
        self.get_logger().info('Serial port opened')
        return evo

    def timer_callback(self):
        try:
            distance = self.get_evo_range(self.evo_)
            msg = Float32()
            msg.data = distance
            self.publisher_.publish(msg)
            self.counter_ += 1
        except serial.serialutil.SerialException:
            self.get_logger().info("Device disconnected (or multiple access on port). Exiting...")
            self.evo_.close()
            rclpy.shutdown()

    def get_evo_range(self, evo_serial):
        crc8_fn = crcmod.predefined.mkPredefinedCrcFun('crc-8')
        data = evo_serial.read(1)
        if data == b'T':
            frame = data + evo_serial.read(3)
            if frame[3] == crc8_fn(frame[0:3]):
                rng = frame[1] << 8
                rng = rng | (frame[2] & 0xFF)
            else:
                raise RuntimeError("CRC mismatch. Check connection or make sure only one program accesses the sensor port.")
        else:
            raise RuntimeError("Waiting for frame header")

        if rng == 65535:
            dec_out = float('inf')
        elif rng == 1:
            dec_out = float('nan')
        elif rng == 0:
            dec_out = -float('inf')
        else:
            dec_out = rng / 1000.0
        return dec_out

def main(args=None):
    rclpy.init(args=args)
    node = SensorDistanciaNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
