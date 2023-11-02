import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function Login() {
    const [form, setForm] = useState({
        username: "",
        password: ""
    });

    const handleClick = async (event) => {
        event.preventDefault();

        const logincred = await fetch(`http://localhost:5000/user/login`, {
            mode: "cors",
            method: 'POST',
            body: JSON.stringify(form),
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(res => res.json())
            .catch((error) => console.log(error));
    }


    const handleInputChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setForm({ ...form, [name]: value });
    };

    return (
        <Form>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" name="username" value={form.username} onChange={handleInputChange} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" name="password" value={form.password} onChange={handleInputChange} />
            </Form.Group>
            <Button variant="primary" type="submit" onClick={handleClick}>
                Submit
            </Button>
        </Form>
    );
}
export default Login;