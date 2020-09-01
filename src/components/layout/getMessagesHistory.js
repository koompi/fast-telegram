import React, { useEffect, useState } from "react";
import { Layout } from "antd";
import UserHeader from "./header";
import axios from "axios";

const { Content } = Layout;
const getToken = localStorage.getItem("token");

const GetMessagesHistory = ({ peer_id, access_hash }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    axios({
      method: "POST",
      url: "http://127.0.0.1:8000/api/get_messages",
      headers: {
        "Content-Type": "application/json",
        Authorization: `jwt ` + getToken,
      },
      data: {
        limit: 20,
        entity:467551940,
        access_hash: -1690262821289062472,
      },
    }).then((res) => {
      console.log("data", res.data);
      setUsers(res.data);
      setTimeout(() => {
        setLoading(false);
      }, 1000);
    });
  }, []);

  const GetMessages = () => {
    return users.map((msg) => {
      console.log(msg);
      if (msg.id % 2 === 0) {
        return (
          <div className="get-message-container">
            <div className="get-message">
              <p className="get-text-message">{msg.message.text}</p>
            </div>
            <div>
              <p className="get-message-times">{msg.date}</p>
            </div>
          </div>
        );
      }
    });
  };

  return (
    <React.Fragment>
      <Layout>
        {/* <UserHeader /> */}
        {/* <Content className="site-layout-content">
                <div className="get-message-container">
                    <div className="get-message">
                        <p className="get-text-message">
                            hey you i hate you so much. Let's break I don't wanna think about it again and
                            y you i hate you so much. Let's break I don't wanna think about it again and
                            y you i hate you so much. Let's break I don't wanna think about it again and 
                            hey you i hate you so much. Let's break I don't wanna think about it again a
                        </p>
                    </div>
                    <div>
                        <p className="get-message-times">6:12 am</p>
                    </div>
                 </div>
                <div className="send-message-container">
                    <p className="send-text-message">
                        hey you i hate you so much. Let's break I don't wanna think about it again and again
                        hey you i hate you so much. Let's break I don't wanna think about it again a
                        y you i hate you so much. Let's break I don't wanna think about it again and
                        y you i hate you so much. Let's break I don't wanna think about it again and                       
                    </p>
                    <div>
                        <p className="send-message-times">6:12 am</p>
                    </div>
                </div>
            </Content> */}
        <GetMessages />
      </Layout>
    </React.Fragment>
  );
};
export default GetMessagesHistory;
