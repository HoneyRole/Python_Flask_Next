import React, {useContext, useState} from "react";
import {useHistory} from "react-router-dom";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import {AppContext} from "../context";

export function Login(props) {
    const [username, setUsername] = useState("");

    const context = useContext(AppContext)
    const history = useHistory();

    function handleSubmit(event) {
        event.preventDefault();
        const csrf_token = $("input[name=csrf_token]").val();
        const data = {csrf_token, ...Object.fromEntries(new FormData(event.target))};
        return $.ajax({
                url: `/api/login`,
                type: 'POST',
                data: data
            }
        ).then(result => {
                $.getJSON('/g').then(g => window.g_json = g
                );
                history.push('/');
            }
        ).fail((xhr, textStatus, errorThrown) =>
            context.setErrorMessage(`Error login: ${xhr.responseText} - ${errorThrown}`))
    }

    return (
        <div className="Login">
            <Form onSubmit={handleSubmit}>
                <Form.Group size="lg" controlId="email">
                    <Form.Label>User Name</Form.Label>
                    <Form.Control
                        autoFocus
                        name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </Form.Group>
                <Button block size="lg" type="submit">
                    Login
                </Button>
            </Form>
        </div>
    );
}
