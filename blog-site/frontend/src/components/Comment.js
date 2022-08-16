import moment from "moment";
import React, {Component, Fragment} from "react";
import {Button, Form, Modal} from "react-bootstrap";
import {withCookies} from "react-cookie";

class Comment extends Component {
    constructor(props){
        super(props);
        this.state = {
            postId: this.props.postId,
            comment: this.props.comment,
            parentHook: this.props.parentHook
        }
    }
    deleteComment() {
        console.log("deleting comment");
        const { cookies } = this.props;
        const user = cookies.get("logged-in-user");
        try {
            fetch(`http://127.0.0.1:4000/posts/${this.state.postId}/comments/${this.state.comment.id}`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${user.jwt}`
                },
            }).then(response => response.text())
                .then(data => {
                    console.log(data);
                    this.state.parentHook(this.state.comment);
                })
        } catch (err) {
            console.log(err);
        }
    }
    updateComment(commentText) {
        if (commentText === undefined || commentText === this.state.comment.content) {
            console.log("Ignoring update");
            return;
        }
        const { cookies } = this.props;
        const user = cookies.get("logged-in-user");
        try {
            fetch(`http://127.0.0.1:4000/posts/${this.state.postId}/comments/${this.state.comment.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${user.jwt}`
                },
                body: JSON.stringify({
                    content: commentText,
                }),
            }).then(response =>
                response.json().then(data => ({
                        data: data,
                        status: response.status
                    })
                ).then(res => {
                    console.log(res.status, res.data);
                    this.setState({comment: res.data})
                    this.toggleModal(false);
                    this.state.parentHook(this.state.comment);
                }));
        } catch (err) {
            console.log(err);
        }
    }
    toggleModal(flag) {
        this.setState({showModal: flag});
    }
    handleChange = (event) => {
        this.setState({[event.target.name]: event.target.value})
    }
    render() {
        const { cookies } = this.props;
        const loggedInUser = cookies.get("logged-in-user");
        const handleClose = () => this.toggleModal(false);
        const handleShow = () => this.toggleModal(true);
        return (
            <div className="card bg-light mb-3 ml-2 mt-4" key={this.state.comment.id} style={{"maxWidth": "35rem"}}>
                <div className="card-header">
                    {this.state.comment.user.name} @ {moment.utc(this.state.comment.created).format("LLLL")}
                </div>
                <div className="card-body">
                    <p className="card-text"><span style={{"whiteSpace": "pre-line"}}>{this.state.comment.content}</span></p>
                </div>
                <div>
                    {loggedInUser?.id === this.state.comment.user.id ? (
                        <>
                            <Button variant="secondary" onClick={handleShow} className="m-1" style={{"maxWidth": "8rem"}}>
                                Edit Comment
                            </Button>
                            <button onClick={() => this.deleteComment()} type="button" className="btn btn-danger m-1" style={{"maxWidth": "6rem"}}>
                                <i className="bi bi-trash"/> Delete</button>
                        </>
                    ) : null}
                </div>
                <Modal show={this.state.showModal} onHide={handleClose} centered>
                    <Modal.Header closeButton>
                        <Modal.Title>Edit Comment</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <Form.Group className="mb-3" controlId="updateForm.ControlTextarea1">
                                <Form.Label>Comment Content</Form.Label>
                                <Form.Control as="textarea" rows={5} name="commentText" onChange={this.handleChange} defaultValue={this.state.comment.content} autoFocus />
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}>
                            Close
                        </Button>
                        <Button variant="primary" onClick={() => this.updateComment(this.state.commentText)}>
                            Save Comment
                        </Button>
                    </Modal.Footer>
                </Modal>
            </div>
        )
    }
}

export class CommentModal extends Component {
    constructor(props){
        super(props);
        this.state = {
            postId: this.props.postId,
            parentHook: this.props.parentHook
        }
    }
    addComment(content) {
        const { cookies } = this.props;
        const user = cookies.get("logged-in-user");
        try {
            fetch(`http://127.0.0.1:4000/posts/${this.state.postId}/comments`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${user.jwt}`
                },
                body: JSON.stringify({
                    content: content,
                }),
            }).then(response =>
                response.json().then(data => ({
                        data: data,
                        status: response.status
                    })
                ).then(res => {
                    console.log(res.status, res.data);
                    this.toggleModal(false);
                    this.state.parentHook(res.data);
                }));
        } catch (err) {
            console.log(err);
        }
    }
    toggleModal(flag) {
        this.setState({showModal: flag});
    }
    handleChange = (event) => {
        this.setState({[event.target.name]: event.target.value})
    }
    render() {
        const { cookies } = this.props;
        const isLoggedIn = cookies.get("logged-in-user") !== undefined;
        const handleClose = () => this.toggleModal(false);
        const handleShow = () => this.toggleModal(true);
        return (
            <Fragment>
                {isLoggedIn ? (
                    <Button variant="secondary" onClick={handleShow}>
                        Add Comment
                    </Button>
                ) : (
                    <Button type="button" variant="secondary" disabled>Must login to add comments</Button>
                )}
                <Modal show={this.state.showModal} onHide={handleClose} centered>
                    <Modal.Header closeButton>
                        <Modal.Title>New Comment</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <Form.Group className="mb-3" controlId="addForm.ControlTextarea1">
                                <Form.Label>Comment Content</Form.Label>
                                <Form.Control as="textarea" rows={5} name="newComment" onChange={this.handleChange} autoFocus />
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}>
                            Close
                        </Button>
                        <Button variant="primary" onClick={() => this.addComment(this.state.newComment)}>
                            Save Comment
                        </Button>
                    </Modal.Footer>
                </Modal>
            </Fragment>
        )
    }
}

CommentModal = withCookies(CommentModal)
export default withCookies(Comment)
