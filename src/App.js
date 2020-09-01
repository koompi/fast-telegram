import React from 'react';
import './App.css';
import 'antd/dist/antd.css';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { PublicRoute } from "react-private-public-route";
import Login from './components/login';
import Channel from './components/channels';
import SignUp from './components/signUp';
import VerifyCode from './components/verify';
import NoConversation from './components/conversations/no-conversation';
import Logout from './components/logout';

function App() {
  return (
    <React.Fragment>
      <Router>
        <Switch>
        <Route exact path="/" component={Login}/>
        <PublicRoute exact path="/login" component={Login} />
        <PublicRoute exact path="/logout" component={Logout} />
        <Route exact path="/channel" component={Channel}/>
        <Route exact path="/register" component={SignUp}/>
        <Route exact path="/verify" component={VerifyCode}/>
        <Route exact path="/no" component={NoConversation}/>
        </Switch>
      </Router>
    </React.Fragment>
  );
}

export default App;
