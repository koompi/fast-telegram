import React from 'react';
import {Result} from 'antd';



const NoConversation = ()=>{

    return(
        <React.Fragment>
            <Result className="container-noconversation"
                status="404"
                title="Please select your message account."
                subTitle="Sorry, the page you visited does not exist."
            />
        </React.Fragment>
    );
}

export default NoConversation;