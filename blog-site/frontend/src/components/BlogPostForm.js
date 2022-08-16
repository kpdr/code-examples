import {Component} from "react";
import {withCookies} from "react-cookie";

class BlogPostForm extends Component {
    state = {
        id: 0,
        title: "",
        content: "",
    }
    componentDidMount() {
        const { postId } = this.props.match.params;
        console.log(this.props.match);
        if (postId  === undefined) {
            return;
        }

        fetch(`http://127.0.0.1:4000/posts/${postId}`)
            .then(res => res.json())
            .then((data) => {
                this.setState( data )
            })
            .catch(console.log)
    }
    onChange = e => {
        this.setState({
            [e.target.name]: e.target.value,
        })
    }
    isUpdate() {
        return this.state.id > 0;
    }
    handleSubmit = async e => {
        e.preventDefault();
        const { cookies } = this.props;
        const user = cookies.get("logged-in-user");
        console.log(this.state);
        try {
            fetch("http://127.0.0.1:4000/posts" + (this.isUpdate() ? `/${this.state.id}`  : ""), {
                method: this.isUpdate() ? "PUT" : "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${user.jwt}`
                },
                body: JSON.stringify({
                    title: this.state.title,
                    content: this.state.content,
                }),
            }).then(response =>
                response.json().then(data => ({
                        data: data,
                        status: response.status
                    })
                ).then(res => {
                    console.log(res.status, res.data);
                    this.props.history.push(`/posts/${res.data.id}`);
                }));
        } catch (err) {
            console.log(err);
        }
    };
    render() {
        return (
            <div className="container">

            <form onSubmit={this.handleSubmit} className="needs-validation">
                <div className="col-sm-6">
                    <label htmlFor="title" className="form-label">Title</label>

                    <input
                        type="text"
                        placeholder="title goes here"
                        className="form-control"
                        value={this.state.title}
                        name="title"
                        onChange={this.onChange}
                    />
                </div>
                <div className="col-sm-10">
                    <label htmlFor="content" className="form-label">Content</label>
                    <textarea
                        placeholder="content here"
                        className="form-control"
                        value={this.state.content}
                        name="content"
                        onChange={this.onChange}
                    />
                </div>
                <hr className="my-4"/>
                <button className="btn btn-primary btn-md px-4 gap-3">Publish Post</button>
            </form>
            </div>
        )
    }

}

export default withCookies(BlogPostForm)
