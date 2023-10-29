import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function Login() {
    const [form, setForm] = useState({
        username: "",
        password: ""
    });

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const logincred = await fetch(`http://localhost:5000/user/login`, {
                mode: "cors",
                method: 'POST',
                body: JSON.stringify(form),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (logincred.status === 200) {
                console.log('Login successful');
            } else if (logincred.status === 400) {
                console.log('Username or password is empty');
            }
        } catch (error) {
            console.error('Error during fetch:', error);
        }
    };



    const handleInputChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setForm({ ...form, [name]: value });
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" name="username" value={form.username} onChange={handleInputChange} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" name="password" value={form.password} onChange={handleInputChange} />
            </Form.Group>
            <Button variant="primary" type="submit">
                Submit
            </Button>
        </Form>
    );
}

export default Login;
