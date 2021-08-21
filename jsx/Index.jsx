import React, {useEffect} from "react";
import ReactDOM from 'react-dom'
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import {AppContext, ContextErrorMessage, ContextMessage, useContextState} from './context'

import Home from "./Home";
import {Navigation} from "./Navigation";
import {Login} from "./auth/Login";


export function Index() {
    const contextState = useContextState();

    useEffect(() => $.getJSON('/g').then(g => window.g_json = g), []);

    return (<AppContext.Provider value={contextState}>
        <Router>
            <Navigation/>
            <ContextMessage message={contextState.message}/>
            <ContextErrorMessage message={contextState.errorMessage}/>
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
