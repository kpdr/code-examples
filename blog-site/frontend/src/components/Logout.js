import React, {Component} from "react";
import {Button} from "react-bootstrap";
import {withCookies} from "react-cookie";

class Logout extends Component {
    logout() {
        console.log("logging out");
        const { cookies } = this.props;
        console.log(cookies.cookies);
        cookies.remove("logged-in-user", { path: '/' } );
        console.log(cookies.cookies);
    }
    render() {
        const { cookies } = this.props;
        const { email } = cookies.get("logged-in-user");
        return (
            <Button variant="light" onClick={() => this.logout()}>
                <i className="bi bi-google"></i> Log Out
                <p><small className="text-muted">{email}</small></p>
            </Button>
        )
    }
}

export default withCookies(Logout)
