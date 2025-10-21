from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    param_goal_order = LaunchConfiguration('goal_order')
 
    dla_goal_order = DeclareLaunchArgument(
        'goal_order',
        # default_value='10',
        default_value='5',
        description='parameter value of goal order'
    )

    action_client_cmd = Node(
        package="slampibot_examples",
        executable="action_client_parameters",
        name='action_client_parameters',
        output='screen',
        parameters=[{'goal_order': param_goal_order}],
    )

    return LaunchDescription([
        dla_goal_order,
        action_client_cmd,        
    ])

