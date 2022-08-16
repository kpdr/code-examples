import React, {Component} from "react";
import {Route, Switch} from "react-router-dom";
import About from "../pages/About";
import NotFound from "../pages/NotFound";
import BlogPost from "./BlogPost";
import BlogPostForm from "./BlogPostForm";
import BlogPostsList from "./BlogPostsList";
import Footer from "./Footer";
import Header from "./Header";
import UserSettings from "./UserSettings";
import { GoogleOAuthProvider } from '@react-oauth/google';
import { CookiesProvider } from 'react-cookie';


class Main extends Component {

    render() {
        return (
            <CookiesProvider>
                <GoogleOAuthProvider clientId="362134854545-t9ni0g6vtl1igvv2gmk8ehjk5tr315p4.apps.googleusercontent.com">
                    <Header/>
                    <Switch>
                        <Route path="/" exact>
                            <BlogPostsList/>
                        </Route>
                        <Route path="/posts/:postId" component={BlogPost}/>
                        <Route path={["/post-form/:postId", "/post-form"]} component={BlogPostForm}/>
                        <Route path="/settings">
                            <UserSettings/>
                        </Route>
                        <Route path="/about">
                            <About/>
                        </Route>
                        <Route path="*">
                            <NotFound/>
                        </Route>
                    </Switch>
                    <Footer/>
                </GoogleOAuthProvider>
            </CookiesProvider>)
    }
}

export default Main;
