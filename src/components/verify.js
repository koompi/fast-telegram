import React, {useState} from 'react';
import { Helmet } from "react-helmet";
import { GiMissileLauncher } from "react-icons/gi";
import axios from "axios";
import SuccessMessage from './Messages/successfulMessage';
import Message from './Messages/Message';
import { Form, Input, Button, Card } from 'antd';
import { CodeOutlined } from '@ant-design/icons';

const TITTILE ="Fast telegram | Verify";

const VerifyCode = ()=>{

    const message = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const setLoading = useState(false);

    const onSubmit = (data) => {
        const getToken = localStorage.getItem("token", data.token);
        fetch("http://127.0.0.1:8000/api/confirm", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'Accept': 'application/json',
            Authorization: `jwt ` + getToken,
          },
          body: JSON.stringify({  
              code: parseInt(data.Code)
          })      
        })
          .then((res) => res.json())
          .then((data) => {
            // console.log("data", data);
            if(data.confirm === "success"){
                setLoading(true);
                setTimeout(()=>{
                    setLoading(false);
                }, 3000);
                setSuccessMessage("successful");
                setTimeout(()=>{
                    setSuccessMessage(window.location.replace("/channel"));
                }, 3000);
            } else {
                setSuccessMessage(data.errors);           
                setTimeout(()=>{
                    setSuccessMessage();
                }, 3000);
            }       
          })
          .catch((err) => console.log(err));
      };

      const onResend = (data) => {
        const getToken = localStorage.getItem("token", data.token);
        // console.log(getToken);
        axios
          .get("http://127.0.0.1:8000/api/resend", {
            headers: {
              "Content-Type": "application/json",
              Authorization: `jwt ` + getToken,
            },
            body: JSON.stringify({
              phone: data.Phone,
              password: data.Pasword
            }),
          })
          .then((res) => {
            if(res.data.token){
              setLoading(true);
              setTimeout(()=>{
                setLoading(false);
              }, 2000);
              setSuccessMessage(res.data.message);
              setTimeout(()=>{
                setSuccessMessage();
              },3000);
            } else{
              setSuccessMessage(res.data.errors);
              setTimeout(()=>{
                setSuccessMessage();
              },3000);
            }
          })
          .catch((err) => console.log(err));
      };

    return(
        <React.Fragment>
            <Helmet>
                <title>{TITTILE}</title>
            </Helmet>
            <div className="container-register">
                <div className="background-register">
                    <img className="register-background" src="img/verify.svg" alt="sign up"/>
                </div>
                <Card hoverable  className="verify-form">
                    {message ? <Message msg={message} /> : null}
                    {successMessage ? <SuccessMessage msg={successMessage} /> : null}
                    <Form onFinish={onSubmit}>
                        <div className="login-header">                            
                            <p>Verify</p>
                            <GiMissileLauncher/>
                        </div>                        
                        <Form.Item  name="Code" 
                            rules={[
                            {
                                required: true,
                                message: 'Please input your code!',
                            },
                            ]}
                        >
                            <Input size="large" prefix={<CodeOutlined />} placeholder="Code" minLength="5" />
                        </Form.Item>                       
                        <Form.Item className="forgot-label">
                            <Button size="large" shape="round" className="button-submit" type="primary" htmlType="submit">
                                Submit
                            </Button>           
                            <a onClick={onResend} className="forgot-password">
                                Resend code
                            </a >                  
                        </Form.Item>
                        <Form.Item>           
                            <p className="term-label">Terms & condition</p>
                        </Form.Item>
                    </Form>
                </Card>
            </div>
        </React.Fragment>
    );
}

export default VerifyCode;
