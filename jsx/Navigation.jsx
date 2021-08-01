import React, {useContext} from "react";
import {Link, useLocation} from "react-router-dom";
import {AppContext} from "./context";
import {Nav, Navbar} from "react-bootstrap";

export const Navigation = (props) => {
    const location = useLocation();
    const context = useContext(AppContext);

    return (
        <Navbar expand="lg">
            <Navbar.Brand><Link to="/">Flask Next</Link></Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav"/>
            <Navbar.Collapse id="navbar">
                <Nav className="mr-auto">
                </Nav>
            </Navbar.Collapse>
        </Navbar>

    )
}
