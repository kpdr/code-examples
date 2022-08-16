import {Component} from "react";
import { GoogleLogin } from '@react-oauth/google';
import jwt_decode from "jwt-decode";
import {withCookies} from "react-cookie";


class Login extends Component {
    resolveToken(token) {
        return fetch('http://127.0.0.1:4000/users', {
            method: "POST",
                headers: {
                "Authorization": `Bearer ${token}`
            }
        })
            .then(res => res.json())
            .then((data) => {
                console.log(data);
                return data.user;
            })
            .catch(console.log)
    }
    render() {
        return (
            <GoogleLogin
                onSuccess={credentialResponse => {
                    const decoded = jwt_decode(credentialResponse.credential);
                    const { cookies } = this.props;
                    this.resolveToken(credentialResponse.credential).then(user => {
                        let cookieValue = {
                            "id": user.id, "name": decoded.name, "email": decoded.email, "jwt": credentialResponse.credential
                        }
                        cookies.set(
                            "logged-in-user",
                            cookieValue,
                            { path: "/", expires: new Date(decoded.exp * 1000) });

                        console.log("setting cookie: ", cookieValue);
                    });
                }}
                onError={() => {
                    console.log('Login Failed');
                }}
            />
        )
    }
}

export default withCookies(Login)
