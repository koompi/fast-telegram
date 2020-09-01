import React, { useState, useEffect } from "react";
import {
  Drawer,
  Button,
  Switch,
  Input,
  Layout,
  Menu,
  Avatar,
  Row,
  Col,
  Badge,
  Popover,
} from "antd";
import {
  SettingOutlined,
  TeamOutlined,
  UserOutlined,
  BarsOutlined,
  FileTextOutlined,
  VideoCameraAddOutlined,
  LinkOutlined,
  LogoutOutlined,  
  PlusCircleOutlined,
  SendOutlined,
  MessageOutlined,
  PhoneOutlined,
  CameraOutlined,
  SyncOutlined
} from "@ant-design/icons";
import axios from "axios";
import { Helmet } from "react-helmet";
import { Link } from "react-router-dom";
import NoConversation from "./conversations/no-conversation";
import Loader from "./layout/loader";
// import Form from "antd/lib/form/Form";

const { Sider, Footer, Content, Header } = Layout;
const { Search } = Input;
const TITTLE = "Fast telegram | Channel";

const getToken = localStorage.getItem("token");

function Channel() {
  const [visible, setVisible] = useState(false);
  const [placement, setPlacement] = useState("left");
  const [theme, setTheme] = useState("light");
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [message, setGetmessage] = useState([]);
  const [color, setColor] = useState([]);

  const randomChangeColors = () => {
    const ColorList = [
      "#f56a00",
      "#7265e6",  
      "#ffbf00",
      "#00a2ae",
      "#eb2f96",
      "#95de64",
      "#613400",
    ];
    const randomColors =
      ColorList[Math.floor(Math.random() * ColorList.length)];
    setColor(randomColors);
  };

  const [state, setstate] = useState({
    visible: false,
  });
  const hide = () => {
    setstate({
      visible: false,
    });
  };
  const handleVisibleChange = (visible) => {
    setstate({ visible });
  };

  const showDrawer = () => {
    setVisible(true);
  };

  const onClose = () => {
    setVisible(false);
  };

  const changeTheme = (value) => {
    setTheme(value ? "dark" : "light");
  };

  useEffect(() => {
    setLoading(true);
    axios({
      method: "POST",
      url: "http://127.0.0.1:8000/api/get_dialogs",
      headers: {
        "Content-Type": "application/json",
        Authorization: `jwt ` + getToken,
      },
      data: {
        limit: 20,
      },
    })
      .then((res) => {
        setUsers(res.data);
        console.log("datasss", res.data);
        setTimeout(() => {
          setLoading(false);
        }, 1000);
        Loader();
        randomChangeColors();
      })
      .catch((err) => console.log(err));
  }, []);


  // useEffect(() => {
  //   axios({
  //     method: "POST",
  //     url: "http://127.0.0.1:8000/api/get_messages",
  //     headers: {
  //       "Content-Type": "application/json",
  //       Authorization: `jwt ` + getToken,
  //     },
  //     data: {
  //       entity: 467551940,
  //       access_hash: -1690262821289062400,
  //       limit: 15,
  //     },
  //   }).then((res) => {
  //     console.log("message", res.data);
  //     setGetmessage(res.data);
  //   });
  // }, []);

  const SelectedUser = () => {
    const handleSelectedUser = {
      entity: 1159756398,
      access_hash: -8845448756285871438,
    };
    axios.post("http://127.0.0.1:8000/api/get_messages", handleSelectedUser,{
      headers: {
              "Content-Type": "application/json",
              Authorization: `jwt ` + getToken,
          }, 
      data: {
        limit: 10,        
      }
    }).then((res) =>{
      console.log("message", res.data);
      setGetmessage(res.data);
    }).catch((err)=> console.log(err));
  }

  const onSendMessage = () =>{
    fetch("http://127.0.0.1:8000/api/send_message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `jwt ` + getToken,
      },
      data:{
        entity: 467551940,
        access_hash: -1690262821289062400,
        message: "sad"
      },
    }).then ((res) => res.json())
      .then((data) => {
        console.log(data);
      }).catch((err)=> console.log(err));
  }

  const GetMessages = () => {
    return message.map((msg) => {
      const d = new Date(msg.date);
      // console.log(msg);
      if (getToken && msg.message !== null) {
        if (msg.message.text) {
          return (
            <div className="get-message-container">
              <div className="get-message">
                <p className="get-text-message">{msg.message.text}</p>
              </div>
              <div>
                <p className="get-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if (msg.message.file) {
          return (
            <div className="get-message-container">
              <div className="get-message">
                <p className="get-text-message">{msg.message.file}</p>
              </div>
              <div>
                <p className="get-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if (msg.message.voice) {
          console.log(msg.message.voice);
          return (
            <div className="get-message-container">
              <div className="get-message">
                {/* <audio className="get-text-message" controls type="audio/ogg" src={msg.message.voice}/> */}
                <audio controls className="get-sound-message">
                  <source src={msg.message.voice} type="file/ogg"/>
                </audio>
              </div>
              <div>
                <p className="get-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if (msg.message.photo) {
          return (
            <div className="get-message-container">
              <div className="get-message">
                <img className="get-text-message" src={msg.message.photo}/>
              </div>
              <div>
                <p className="get-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if(msg.message.sticker){
          return(
            <div className="get-message-container">
              <div className="get-message">
                <img className="get-text-message" src={msg.message.sticker}/>
                </div>
              <div>
                <p className="get-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if (msg.message.url) {
          return (
            <div className="get-message-container">
              <div className="get-message">
                <a
                  href={msg.message.url}
                  target="_blank"
                  className="get-link-message"
                >
                  {msg.message.url}
                </a>
                <a
                  href={msg.message.url}
                  target="_blank"
                  style={{ display: "flex", marginTop: "20px", color:'white' }}
                >
                  {msg.message.site_name}
                </a>
                <h3 style={{color:'white'}}>{msg.message.title}</h3>
                <p>{msg.message.description.substring(0, 100)}...</p>
              </div>
              <div>
                <p className="get-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        } else {
          return (
            <div className="get-message-container">
              <div className="get-message">
                <a className="get-text-message">{msg.message.location}</a>
              </div>
              <div>
                <p className="get-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
      } else if (msg.id % 2 !== 0) {
        if (msg.message.text) {
          return (
            <div className="send-message-container">
              <div className="send-message">
                <p className="send-text-message">{msg.message.text}</p>
              </div>
              <div>
                <p className="send-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if (msg.message.file) {
          return (
            <div className="send-message-container">
              <div className="send-message">
                <div className="send-text-message">{msg.message.file}</div>
              </div>
              <div>
                <p className="send-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if (msg.message.voice) {
          return (
            <div className="send-message-container">
              <div className="send-message">
                {/* <audio className="send-sound-message" controls type="audio/ogg" src={msg.message.voice}/> */}
                <audio controls className="send-sound-message">
                  <source src={msg.message.voice} type="audio/ogg"/>
                </audio>
              </div>
              <div>
                <p className="send-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if (msg.message.photo) {
          return (
            <div className="send-message-container">
              <div className="send-message">
                <img className="send-text-message" src={msg.message.photo}/>
              </div>
              <div>
                <p className="send-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if(msg.message.sticker){
          return(
            <div className="send-message-container">
              <div className="send-message">
                <img className="send-text-message" src={msg.message.sticker}/>
                </div>
              <div>
                <p className="send-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        }
        if (msg.message.url) {
          return (
            <div className="send-message-container">
              <div className="send-message">
                <a
                  href={msg.message.url}
                  target="_blank"
                  className="send-link-message"
                >
                  {msg.message.url}
                </a>
                <a
                  href={msg.message.url}
                  target="_blank"
                  style={{ display: "flex", marginTop: "20px" }}
                >
                  {msg.message.site_name}
                </a>
                <h3>{msg.message.title}</h3>
                <p>{msg.message.description.substring(0, 100)}...</p>
              </div>
              <div>
                <p className="send-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div>
            </div>
          );
        } else {
          return (
            <div className="send-message-container">
              <div className="send-message">
                <a className="send-text-message">{msg.message.location}</a>
              </div>
              {/* <div>
                <p className="send-message-times">
                  {d.toLocaleTimeString("en-AU")}
                </p>
              </div> */}
            </div>
          );
        }
      }
    });
  };

  return (
    <React.Fragment>
      <Helmet>
        <title>{TITTLE}</title>
      </Helmet>
      <Layout>
        <Drawer
          theme="dark"
          title="Profile"
          placement={placement}
          closable={false}
          onClose={onClose}
          visible={visible}
          key={placement}
          style={{ position: "absolute", textAlign: "center" }}
        >
          <Menu
            mode="inline"
            //   theme={theme}
          >
            <div className="channel-menu">
              <UserOutlined /> Account
            </div>
            <div className="channel-menu">
              <SettingOutlined /> Setting
            </div>
            <div className="channel-menu">
              <TeamOutlined /> Create team
            </div>
            <div className="channel-menu">
              <Switch
                checkedChildren="Dark"
                unCheckedChildren="Light"
                onChange={changeTheme}
              />
            </div>
          </Menu>
        </Drawer>
      </Layout>
      <Row>
        <Col span={5}>
          <Layout>
            <Sider
              width={400}
              collapsedWidth={0}
              className="container-user-dialog"
            >
              <div className="channel-search">
                <Button
                  className="auto-slider-button"
                  size="large"
                  onClick={showDrawer}
                >
                  <BarsOutlined />
                </Button>
                <Search
                  onSearch={(value) => console.log(value)}
                  style={{ width: "100%" }}
                  size="large"
                />
              </div>
              <div className="channel-dialog">
                <Menu theme="dark" mode="inline">
                  {users.map((user) => (
                    <Menu.ItemGroup
                      className="profile-container-left"                      
                    >
                      <Menu.Item
                        className="chat-list-items" 
                        key={user.peer_id}                                               
                        onClick={SelectedUser}                      
                      >
                        <Badge className="chat-list">
                          {/* <Avatar
                            size={50}
                            alt={user.name}
                            src={user.profile}
                            src={require('../images/profiles2.png')}
                          />  */}
                          <Avatar
                            style={{
                              backgroundColor: color,
                              verticalAlign: "middle",
                              height: 50,
                              width: 50,
                            }}
                            className="profile-chat-list"
                          >
                            {user.name.slice(0, 1)}
                            {randomChangeColors}
                          </Avatar>
                        </Badge>
                          <p className="left-hand-name">{user.name}</p>
                      </Menu.Item>
                    </Menu.ItemGroup>
                  ))}
                  {loading ? <Loader /> : null}
                </Menu>
              </div>
            </Sider>
          </Layout>
        </Col>
        <Col span={14}>
          <Layout>
            <Header className="site-layout-header">
              {null ? SelectedUser() : <div className="header-name">hello</div>}                                           
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

            <Content className="site-layout-content">
              {loading ? <SyncOutlined spin className="loading-icons" /> : null}
              {/* {loading ? null  : <NoConversation/> } */}
              {<NoConversation/> ? <GetMessages/> : null}
            </Content>

            <Footer className="site-layout-footer">
              <button className="sending-button">
                <PlusCircleOutlined />
              </button>
              <Input 
                type="text"
                width={500}
                size="large"
                placeholder="Type a message ..."
                type="text"
                name="SendMessage"
                onSubmit={onSendMessage}
              />
              <button className="sending-button" type="submit" onSubmit={onSendMessage} >
                <SendOutlined />
              </button>
            </Footer>
          </Layout>
        </Col>
        <Col span={5}>
          <Sider
            width={400}
            collapsedWidth={0}
            style={{
              width: "40vh",
              overflow: "auto",
              height: "100vh",
              position: "fixed",
              right: "0",
            }}
          >
            <div className="profile-container">
              <Badge
                status="success"
                offset={[-20, 90]}
                style={{ width: "10px", height: "10px" }}
              >
                <Avatar size={100} src="img/hello.png" />
              </Badge>
              <p className="profile-name">Steven Hocking</p>
              <div className="profile-options">
                <Popover trigger="hover" content="Documents">
                  <FileTextOutlined className="options-profile-icon" />
                </Popover>
                <Popover trigger="hover" content="Videos">
                  <VideoCameraAddOutlined className="options-profile-icon" />
                </Popover>
                <Popover trigger="hover" content="Links sharing">
                  <LinkOutlined className="options-profile-icon" />
                </Popover>
                <Popover trigger="hover" content="Setting">
                  <SettingOutlined className="options-profile-icon" />
                </Popover>
                <Popover trigger="hover" content="Logout">
                  <Link to="/logout">
                    <LogoutOutlined className="options-profile-icon" />
                  </Link>
                </Popover>
              </div>
            </div>
          </Sider>
        </Col>
      </Row>
    </React.Fragment>
  );
}

export default Channel;
