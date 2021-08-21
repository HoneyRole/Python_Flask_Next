import React, {useContext} from "react";
import {Link, useLocation} from "react-router-dom";
import {AppContext} from "./context";
import {Nav, Navbar, NavDropdown} from "react-bootstrap";

export const Navigation = (props) => {
    const location = useLocation();
    const context = useContext(AppContext);

    const profileLinks =
        <NavDropdown title="Profile" id="profile-dropdown">
            {!context.authenticated && <NavDropdown.Item><Link to={`/login/`}>Login</Link></NavDropdown.Item>}
            {context.authenticated && <NavDropdown.Item><Link to={`/logout/`}>Logout</Link></NavDropdown.Item>}
        </NavDropdown>;

    return (
        <Navbar expand="lg">
            <Navbar.Brand><Link to="/">Flask Next</Link></Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav"/>
            <Navbar.Collapse id="navbar">
                <Nav className="mr-auto">
                </Nav>
                {profileLinks}
            </Navbar.Collapse>
        </Navbar>

    )
}
