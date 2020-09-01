import React, {useState} from 'react';
import Helmet from 'react-helmet';
import { Form, Input, Button, Card } from 'antd';
import { PhoneOutlined, LockOutlined } from '@ant-design/icons';
import { GiMissileLauncher } from "react-icons/gi";
import Message from './Messages/Message';
import SuccessMessage from './Messages/successfulMessage';
import  {Link}  from 'react-router-dom';
import axios from "axios";

const TITTILE = "Fast telegram | Register";

const SignUp = () =>{

    const [message, setMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const setLoading = useState(false);   
    
      const onSubmit = (data) =>{
        const newUser = {
          phone: data.Phone,
          password: data.Password,
          force_sms: true
        };
        // console.log(newUser);
        axios.post("http://127.0.0.1:8000/api/users", newUser)
        .then((res) =>{
          localStorage.setItem("token", res.data.token);
          // console.log(res.data.token);
         if(res.data.token){
           setLoading(true);
           setTimeout(() =>{
             setLoading(false);
           }, 3000);
           setSuccessMessage("Successful");
           setTimeout(()=>{
            setSuccessMessage(window.location.replace("/verify"));
           },3000);
          } else{
            setMessage(res.data.errors);
            setTimeout(()=>{ 
              setMessage();
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
                    <img className="register-background" src="img/confirm.svg" alt="confirm"/>
                </div>
                <Card hoverable  className="register-form">
                    {message ? <Message msg={message} /> : null}
                    {successMessage ? <SuccessMessage msg={successMessage} /> : null}
                    <Form onFinish={onSubmit}>
                        <div className="login-header">                            
                            <p>Register</p>
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
                        <Form.Item  name="Confirm_Password"
                            rules={[
                            {
                                required: true,
                                message: 'Please match your confirm password!',
                            },
                            ]}
                        >
                            <Input.Password size="large" prefix={<LockOutlined/>} type="password" placeholder="Confirm Password" minLength="8"/>                    
                        </Form.Item>
                        <Form.Item className="forgot-label">
                            <Button size="large" shape="round" className="button-submit" type="primary" htmlType="submit">
                                Sign Up
                            </Button>                           
                        </Form.Item>
                        <Form.Item>
                            <p className="create-account-label">Already exist account</p>
                            <Link to="/login">
                                <Button shape="round" size="large" className="create-new">
                                    Login
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

export default SignUp;