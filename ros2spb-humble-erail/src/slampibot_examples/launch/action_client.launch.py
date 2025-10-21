from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    action_client_cmd = Node(
        package="slampibot_examples",
        executable="action_client",
        name='action_client',
        output='screen'
    )

    return LaunchDescription([
        action_client_cmd,        
    ])

