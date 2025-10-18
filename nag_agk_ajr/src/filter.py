# filter.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2 as pc2

class LidarHeightFilter(Node):
    def __init__(self):
        super().__init__('filter')
        self.declare_parameter('input_topic', '/lexus3/os_center/points')
        self.declare_parameter('output_topic', '/lexus3/os_center/filtered_points')
        self.declare_parameter('min_z', 0.2)
        self.declare_parameter('max_z', 4)

        self.sub = self.create_subscription(
            PointCloud2,
            self.get_parameter('input_topic').value,
            self.cb,
            10)
        self.pub = self.create_publisher(
            PointCloud2,
            self.get_parameter('output_topic').value,
            10)

        self.min_z = float(self.get_parameter('min_z').value)
        self.max_z = float(self.get_parameter('max_z').value)

    def cb(self, msg: PointCloud2):
        pts = [
            (x, y, z)
            for x, y, z in pc2.read_points(msg, field_names=('x','y','z'), skip_nans=True)
            if self.min_z <= z <= self.max_z
        ]
        self.pub.publish(pc2.create_cloud_xyz32(msg.header, pts))
        self.get_logger().info(f'kept={len(pts)}', throttle_duration_sec=1.0)

def main():
    rclpy.init()
    rclpy.spin(LidarHeightFilter())
    rclpy.shutdown()
