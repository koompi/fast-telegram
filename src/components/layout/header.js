import React from "react";
import { Layout, Popover } from "antd";
import {
  MessageOutlined,
  PhoneOutlined,
  CameraOutlined,
  SettingOutlined,
} from "@ant-design/icons";

const { Header } = Layout;

function UserHeader(user) {
  // console.log("bind id", user.peer_id);
  return (
    <React.Fragment>
      <Header className="site-layout-header">
        <div className="header-name">Hello</div>
        <div className="header-options">
          <Popover content="messages" trigger="hover">
            <MessageOutlined className="options-header-icon" />
          </Popover>
          <Popover content="out going" trigger="hover">
            <PhoneOutlined className="options-header-icon" />
          </Popover>
          <Popover content="photo" trigger="hover">
            <CameraOutlined className="options-header-icon" />
          </Popover>
          <Popover content="settting" trigger="hover">
            <SettingOutlined className="options-header-icon" />
          </Popover>
        </div>
      </Header>
    </React.Fragment>
  );
}

export default UserHeader;
