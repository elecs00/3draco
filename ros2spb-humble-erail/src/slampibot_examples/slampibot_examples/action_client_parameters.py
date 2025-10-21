import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from slampibot_interfaces.action import Fibonacci

class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__("fibonacci_action_client")

        self.declare_parameter("goal_order", 10)

        self.Fibonacci_action_client = ActionClient(self, Fibonacci, "fibonacci")
        self.goal = Fibonacci.Goal()
        # self.goal.order = 10
        self.goal.order = self.get_parameter("goal_order").get_parameter_value().integer_value

        self.Fibonacci_action_client.wait_for_server()
        self.future = self.Fibonacci_action_client.send_goal_async(
            self.goal, feedback_callback=self.feedbackCallback
        )
        self.future.add_done_callback(self.responseCallback)

    def responseCallback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self.future = goal_handle.get_result_async()
        self.future.add_done_callback(self.resultCallback)

    def resultCallback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.sequence))
        rclpy.shutdown()

    def feedbackCallback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.partial_sequence))

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_client = FibonacciActionClient()
    rclpy.spin(fibonacci_action_client)

if __name__ == '__main__':
    main()