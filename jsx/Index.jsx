import React from "react";
import ReactDOM from 'react-dom'
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import {AppContext, useContextState} from './context'

import Home from "./Home";
import {Navigation} from "./Navigation";
import {Login} from "./auth/Login";


export function Index() {
    const contextState = useContextState();
    return (<AppContext.Provider value={contextState}>
        <Router>
            <Navigation/>
            <div className={"container-fluid"}>
                <Switch>
                    <Route exact path="/">
                        <Home/>
                    </Route>
                    <Route exact path="/login/" component={Login}/>
                    {/*<Route exact path="/logout/" component={Logout}/>*/}
                </Switch>
            </div>
        </Router>
    </AppContext.Provider>)
}

ReactDOM.render(<Index/>, document.getElementById('jsx_content'));
