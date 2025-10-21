import rclpy
from rclpy.node import Node
# from std_msgs.msg import String
from slampibot_interfaces.msg import String


class TopicPublisher(Node):

    def __init__(self):
        super().__init__("topic_publisher")
        self.pub_ = self.create_publisher(String, "message", 10)
        self.counter_ = 0
        self.frequency_ = 1.0
        self.get_logger().info("Publishing at %d Hz" % self.frequency_)        
        self.timer_ = self.create_timer(self.frequency_, self.timerCallback)

    def timerCallback(self):
        msg = String()
        # msg.data = "Topic message counter: %d" % self.counter_
        msg.text = "Topic message counter: %d" % self.counter_
        self.pub_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        self.get_logger().info('Publishing: "%s"' % msg.text)
        self.counter_ += 1

def main():
    rclpy.init()
    topic_publisher = TopicPublisher()
    rclpy.spin(topic_publisher)    
    topic_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
