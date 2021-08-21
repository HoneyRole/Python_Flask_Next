import React, {useContext, useState} from "react";
import {useHistory} from "react-router-dom";
import Button from "react-bootstrap/Button";
import {AppContext,} from "../context";

export function Logout(props) {
    const [email, setEmail] = useState("");

    const context = useContext(AppContext)
    const history = useHistory();

    function clickLogout(event) {
        event.preventDefault();
        $.ajax.post('/api/logout').then(result => {
                $.getJSON('/g').then(g => window.g_json = g)
                history.push('/login');
            }
        ).fail((xhr, textStatus, errorThrown) =>
            context.setErrorMessage(`Error logout: ${xhr.responseText} - ${errorThrown}`))
    }

    return (
        <div className="Login">
            <h3>Confirm Logout</h3>
            <Button block size="lg" onClick={clickLogout}>
                Logout
            </Button>
        </div>
    );
}