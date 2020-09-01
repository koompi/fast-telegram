import React, { useState } from "react";
import { Helmet } from "react-helmet";
import { GiMissileLauncher } from "react-icons/gi";
import Message from './Messages/Message';
import SuccessMessage from './Messages/successfulMessage';
import { Form, Input, Button, Card } from 'antd';
import { PhoneOutlined, LockOutlined } from '@ant-design/icons';
import { Link } from "react-router-dom";

const TITTLE = "Fast telegram | Login";


const Login = () =>{
    const [message, setMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const onSubmit = (data) =>{
        fetch("http://127.0.0.1:8000/api/users/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                // Accept: 'application/json',
            },  
            body: JSON.stringify({
                phone: data.Phone,
                password: data.Password,
                // force_sms: true
            }),
        })
        .then((res) => res.json())
        .then((data) => {
            localStorage.setItem("token", data.token);
            // console.log(data.token);
            // localStorage.getItem("token", data.token);
            console.log(data.token);
            if (data.token) {
            setLoading(true);   
            setTimeout(() => {
                setLoading(false);
            }, 3000);
            setSuccessMessage("Successful");
            setTimeout(() =>{
                setSuccessMessage(window.location.replace("/channel"));
            }, 3000);

            } else {
            setMessage(data.errors);
            setTimeout(() => {
                setMessage();
            }, 3000);
            }
        })
        .catch((err) => {
            alert(err);
        });
    }

    return(
        <React.Fragment>
            <Helmet>
                <title>{TITTLE}</title>
            </Helmet>   
            <div className="container-login">
                <div className="background-login">
                    <img className="login-background" src="img/telegram.svg" alt="login"/>
                </div>
                <Card  hoverable  className="login-form">
                    {message ? <Message msg={message} /> : null}
                    {successMessage ? <SuccessMessage msg={successMessage} /> : null}
                    <Form onFinish={onSubmit}>
                        <div className="login-header">                            
                            <p>Login</p>
                            <GiMissileLauncher/>
                        </div>                        
                        <Form.Item  name="Phone" 
                            rules={[
                            {
                                required: true,
                                message: 'Please input your phone number!',
                            },
                            ]}
                        >
                            <Input size="large" prefix={<PhoneOutlined/>}placeholder="Phone number" />
                        </Form.Item>
                        <Form.Item  name="Password"
                            rules={[
                            {
                                required: true,
                                message: 'Please input your password!',
                            },
                            ]}
                        >
                            <Input.Password size="large" prefix={<LockOutlined/>} type="password" placeholder="Password" minLength="8"/>                    
                        </Form.Item>
                        <Form.Item className="forgot-label">
                            <Button size="large" shape="round" className="button-submit" type="primary" htmlType="submit">
                                Sign In
                            </Button>
                            <a className="forgot-password">
                                Forgot password
                            </a>
                        </Form.Item>
                        <Form.Item>
                            <p className="create-account-label">Did you have account yet?</p>
                            <Link to="/register">
                                <Button shape="round" size="large" className="create-new">
                                    Create account
                                </Button>
                            </Link>
                            <p className="term-label">Terms & condition</p>
                        </Form.Item>
                    </Form>
                </Card>
            </div>
        </React.Fragment>
    );
}

export default Login;