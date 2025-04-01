'use client';

import { ChangeEvent, FormEvent, useState } from 'react';
import { Box, TextField } from '@mui/material';
import { Link } from '@/components/Link';
import '@/scss/login.scss';

export default function Login() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const [username, setUsername] = useState('');

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { value } = event.target;

    setUsername(value);
  };

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    fetch(`${apiUrl}api/get-client-id/${username}`, {
      method: "GET"
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json()
      })
      .then(fetchedData => {
        if (fetchedData.client_id) {
          sessionStorage.setItem("username", username);
          window.location.href = `https://oauth.groupme.com/oauth/authorize?client_id=${fetchedData.client_id}`;
        }
      })
      .catch((error) => console.error("Error fetching client ID:", error));
  }
  
  return (
    <>
      <div className="login-container">
        <div className="login-box">
          <h2 className="title">Login with GroupMe</h2>
          <p className="description">Authenticate to use the bot</p>

          <Box component="form" onSubmit={onSubmit} className='login-form'>
            <TextField
                id="username"
                name='username'
                label="Username"
                value={username}
                variant='outlined'
                className="input-item"
                onChange={handleChange}
                required/>
            <button className="login-button" id="loginButton">
              Login with GroupMe
            </button>
            <Link link={{url: `/signup/`, is_external_link: false}} className='signup-link'>
              {"Don't have a username. Create a new one."}
            </Link>
          </Box>
        </div>
      </div>
    </>
  )
}