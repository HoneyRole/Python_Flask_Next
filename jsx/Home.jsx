import React, {useContext, useEffect, useState} from "react";
import {NavLink, useHistory} from "react-router-dom";
import {AppContext} from './context';
import LoginRequired from "./LoginRequired";

export default function Home(props) {
    const context = useContext(AppContext);
    const history = useHistory();

    useEffect(() => {
        // find if server refresh needs history
        const $request_path = $('input[name=request_path]');
        const requestPathValue = $request_path.val();

        if (requestPathValue) {
            $request_path.val("");
            history.push(requestPathValue);
        }
    }, []);

    useEffect(() => {
    }, [context.anon])

    if (!context.authenticated) {
        return <LoginRequired/>
    }

    return (<div>Welcome to flask-next
    </div>)
}
