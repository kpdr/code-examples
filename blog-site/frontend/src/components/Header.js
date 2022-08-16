import React from "react"
import {useCookies} from "react-cookie";
import Login from "./Login";
import Logout from "./Logout";

const Header = () => {
    const [cookies] = useCookies(['logged-in-user']);
    return (
        <div className="container">
            <header className="float-end">
                {cookies["logged-in-user"] !== undefined ? <Logout /> : <Login />}
            </header>
            <header className="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
                <ul className="nav nav-pills">
                    <li className="nav-item"><a href="/" className="nav-link active" aria-current="page">Posts</a></li>
                    <li className="nav-item"><a href="/settings" className="nav-link">Settings</a></li>
                    <li className="nav-item"><a href="/about" className="nav-link">About</a></li>
                </ul>
            </header>
        </div>
    )
}

export default Header
