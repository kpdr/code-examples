import React from "react";

const About = () => {
    return (
        <div className="container">
            <div className="row g-5">
                <div className="col-md-8">
                    <p>This site is a simple, dummy site meant for teaching/demonstration purposes and is not meant to exemplify production quality code, but more show working examples of different usage patterns.
                    <br/>It covers:</p>
                    <ul>
                        <li>A React frontend</li>
                        <li>A Flask backend</li>
                        <li>A MySQL database</li>
                    </ul>
                    <p>The React frontend shows:</p>
                    <ul>
                        <li>Utilizing bootstrap</li>
                        <li>Logging in via Google Oauth</li>
                        <li>CRUD functionality on a couple of business objects</li>
                    </ul>
                    <p>The Flask backend shows:</p>
                    <ul>
                        <li>Using blueprints for route organization</li>
                        <li>SQLAlchemy for an ORM</li>
                        <li>Database migrations and backup/restore</li>
                        <li>Unit testing</li>
                        <li>Verifying Oauth tokens via Google API</li>
                    </ul>
                </div>
            </div>
        </div>
    )
}
export default About
