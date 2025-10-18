from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nag_agk_ajr',
            executable='filter',
            name='filter',
            parameters=[{
                'input_topic': '/lexus3/os_center/points',
                'output_topic': '/lexus3/os_center/points_filtered',
                'min_z': 0.0,
                'max_z': 2.0
            }]
        )
    ])
