import moment from "moment";
import React, {Component, Fragment} from "react";
import {withCookies} from "react-cookie";
import {Link} from "react-router-dom";
import Comment, {CommentModal} from "./Comment";

class BlogPost extends Component {
    state = {
        post: {
            user: {},
            comments: {}
        }
    }
    componentDidMount() {
        const { postId } = this.props.match.params
        fetch(`http://127.0.0.1:4000/posts/${postId}`)
            .then(res => res.json())
            .then((data) => {
                const commentsById = new Map(
                    data.comments.map(object => {
                        return [object.id, object];
                    }),
                );
                data.comments = commentsById;
                this.setState({post: data})
            })
            .catch(console.log)
    }
    receiveComment = (comment) => {
        console.log("received comment: ", comment);
        let {post} = this.state;
        const existingComment = post.comments.get(comment.id);
        if (existingComment !== undefined && existingComment === comment) {
            // delete case
            post.comments.delete(comment.id);
        } else {
            post.comments.set(comment.id, comment);
        }
        this.setState({
            post: post
        })
    }
    deleteBlogPost() {
        const { cookies } = this.props;
        const user = cookies.get("logged-in-user");
        try {
            const { postId } = this.props.match.params;
            fetch(`http://127.0.0.1:4000/posts/${postId}`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${user.jwt}`
                },
            }).then(response => response.text())
                .then(data => {
                    console.log(data);
                    this.props.history.push("/");
                })
        } catch (err) {
            console.log(err);
        }
    }
    render() {
        const { cookies } = this.props;
        const loggedInUser = cookies.get("logged-in-user");
        const name = this.state.post.user.name;
        return (
            <Fragment>
                <div className="container">
                <div className="row g-5">
                    <div className="col-md-8">
                        <article className="blog-post">
                            <h2 className="blog-post-title mb-1">{this.state.post.title}</h2>
                            <p className="blog-post-meta">{moment.utc(this.state.post.created).format("LLLL")} by {name} </p>

                            <p><span style={{"whiteSpace": "pre-line"}}>{this.state.post.content}</span></p>
                        </article>
                    </div>
                </div>
                {loggedInUser?.id === this.state.post.user.id ? (
                    <>
                        <Link to={`/post-form/${this.state.post.id}`}>
                            <button type="button" className="btn btn-primary btn-lg px-4 gap-3">Edit</button>
                        </Link>
                        <button type="button" className="btn btn-lg px-4 gap-3 btn-danger m-2" onClick={() => this.deleteBlogPost()}>
                            <i className="bi bi-trash"/> Delete
                        </button>
                    </>
                ) : null
                }
                    <hr />

                    {this.state.post.comments.size > 0 ? (
                            <h3>Article Comments</h3>
                        ) : (
                            <h5 className="font-italic">no comments yet</h5>
                        )}
                    <CommentModal key={this.state.post.id} postId={this.state.post.id} parentHook={this.receiveComment} />

                    {Array.from(this.state.post.comments).map(([id, comment]) => (
                        <Comment key={id} comment={comment} postId={this.state.post.id} parentHook={this.receiveComment}/>
                    ))}
                </div>
            </Fragment>
        );
    }
}

export default withCookies(BlogPost)
