import React, { useState } from 'react';
import {Alert} from 'antd';


const Message = ({msg}) =>{
    const [visible, setVisible] = useState(true);

    const handleClose = () => {
      setVisible(false);
    };
    return(
        <React.Fragment>
            <div>
                {visible ? (
                    <Alert className="success-alert" message="Incorrect password or phone number" type="warning" closable afterClose={handleClose} > </Alert>
                ) : null}
            </div>
        </React.Fragment>
    );
}

export default Message;