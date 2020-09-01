import React, { useState } from 'react';
import {Alert} from 'antd';

const SuccessMessage = ({msg}) =>{
    const [visible, setVisible] = useState(true);

    const handleClose = () => {
      setVisible(false);
    };
    return(
        <React.Fragment>
            <div>
                {visible ? (
                    <Alert message="Successful" className="success-alert" type="success" closable afterClose={handleClose} />
                ) : null}
            </div>
        </React.Fragment>
    );
}

export default SuccessMessage;