import moment from "moment";
import React, {Component} from 'react'
import {withCookies} from "react-cookie";
import { Link } from "react-router-dom";


class BlogPostsList extends Component {
    state = {
        posts: []
    }
    componentDidMount() {
        fetch('http://127.0.0.1:4000/posts')
            .then(res => res.json())
            .then((data) => {
                this.setState({ posts: data })
            })
            .catch(console.log)
    }
    render() {
        const { cookies } = this.props.cookies;
        const isLoggedIn = cookies["logged-in-user"] !== undefined;
        return (
            <div>
                <div className="d-grid gap-2 d-sm-flex justify-content-sm-center">
                    {isLoggedIn ? (
                        <Link to="/post-form">
                            <button type="button" className="btn btn-primary btn-lg px-4 gap-3">Create New Post!</button>
                        </Link>
                    ) : (
                        <button type="button" className="btn btn-secondary btn-lg px-4 gap-3" disabled>Must login to create posts</button>
                    )}

                </div>

                <div className="list-group w-auto">
                {this.state.posts.map((post) => (
                    <div key={post.id}>
                    <a href={`/posts/${post.id}`} className="list-group-item list-group-item-action d-flex gap-3 py-3"
                       aria-current="true">
                            <div className="d-flex gap-2 w-100 justify-content-between">
                                <div>
                                    <h6 className="mb-0">{post.title}</h6>
                                </div>
                                <small className="opacity-50 text-nowrap">{moment.utc(post.created).fromNow()}</small>
                            </div>
                    </a>
                    </div>
                ))}
                    </div>
            </div>
        );
    }
}

export default withCookies(BlogPostsList)
