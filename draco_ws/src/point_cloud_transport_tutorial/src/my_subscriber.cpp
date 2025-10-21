// Copyright (c) 2023, Czech Technical University in Prague
// Copyright (c) 2023, Open Source Robotics Foundation, Inc. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//    * Redistributions of source code must retain the above copyright
//      notice, this list of conditions and the following disclaimer.
//
//    * Redistributions in binary form must reproduce the above copyright
//      notice, this list of conditions and the following disclaimer in the
//      documentation and/or other materials provided with the distribution.
//
//    * Neither the name of the Willow Garage nor the names of its
//      contributors may be used to endorse or promote products derived from
//      this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

#include <point_cloud_transport/point_cloud_transport.hpp>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <point_cloud_transport/transport_hints.hpp>

// 콜백 함수: PointCloud2를 로그로 확인하고, RViz2용으로 publish
void pointCloudCallback(
  const sensor_msgs::msg::PointCloud2::ConstSharedPtr & msg,
  rclcpp::Logger logger,
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pub)
{
    // 포인트 수 로그 출력
    RCLCPP_INFO_STREAM(logger, "Message received, number of points is: " << msg->width * msg->height);

    // RViz2에서 구독할 수 있는 새 토픽으로 publish
    pub->publish(*msg);
}

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("point_cloud_subscriber");

    // PointCloudTransport 초기화
    point_cloud_transport::PointCloudTransport pct(node);

    // Draco transport 명시
    const point_cloud_transport::TransportHints hints("draco");

    // 🚨 RViz2용 publisher 추가
    auto pub = node->create_publisher<sensor_msgs::msg::PointCloud2>("/out/draco/decompressed", 5);

    // subscriber 생성, 콜백에서 publisher 전달
    point_cloud_transport::Subscriber pct_sub = pct.subscribe(
        "/out", 10,
        std::bind(pointCloudCallback, std::placeholders::_1, node->get_logger(), pub),
        nullptr,
        &hints
    );

    RCLCPP_INFO_STREAM(node->get_logger(), "Waiting for point_cloud message...");

    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}

