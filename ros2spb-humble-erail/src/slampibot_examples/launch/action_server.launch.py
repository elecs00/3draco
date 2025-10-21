from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    action_server_cmd = Node(
        package="slampibot_examples",
        executable="action_server",
        name='action_server',
        output='screen'
    )

    return LaunchDescription([
        action_server_cmd,
    ])

