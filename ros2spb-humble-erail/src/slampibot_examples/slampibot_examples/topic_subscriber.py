import rclpy
from rclpy.node import Node
# from std_msgs.msg import String
from slampibot_interfaces.msg import String


class TopicSubscriber(Node):

    def __init__(self):
        super().__init__("topic_subscriber")
        self.sub_ = self.create_subscription(String, "message", self.msgCallback, 10)
        self.sub_

    def msgCallback(self, msg):
        # self.get_logger().info("I heard: %s" % msg.data)
        self.get_logger().info("I heard: %s" % msg.text)

def main():
    rclpy.init()
    topic_publisher = TopicSubscriber()
    rclpy.spin(topic_publisher)    
    topic_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
