'use client';

import { ChangeEvent, FormEvent, useState } from 'react';
import { Box, TextField } from '@mui/material';
import { Link } from '@/components/Link';

import '@/scss/login.scss';

export default function Signup() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const [inputValues, setInputValues] = useState({
    'username': '',
    'client_id': ''
  });

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;

    setInputValues((prevValues) => {
      return {...prevValues, [name]: value}
    });
  };

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    fetch(`${apiUrl}api/set-client-id`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({'user_name': inputValues['username'], 'client_id': inputValues['client_id']})
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      })
      .then(() => {
        if (inputValues['username'] && inputValues.client_id) {
          sessionStorage.setItem("username", inputValues['username']);
          window.location.href = `https://oauth.groupme.com/oauth/authorize?client_id=${inputValues.client_id}`;
        }
      })
      .catch((error) => console.error("Error fetching client ID:", error));
  }
  
  return (
    <>
      <div className="signup-container">
        <div className="signup-box">
          <h2 className="title">Signup with GroupMe</h2>
          <p className="description">Authenticate to use the bot</p>

          <Box component="form" onSubmit={onSubmit} className='signup-form'>
            <TextField
                id="username"
                name='username'
                label="Username"
                value={inputValues['username']}
                variant='outlined'
                className="input-item"
                onChange={handleChange}
                required/>
            <TextField
                id="client_id"
                name='client_id'
                label="Client ID"
                value={inputValues['client_id']}
                variant='outlined'
                className="input-item"
                onChange={handleChange}
                required/>
            <button className="signup-button" id="signupButton">
              Signup with GroupMe
            </button>
            <Link link={{url: `/login/`, is_external_link: false}} className='signup-link'>
              Already have a username. Login to use.
            </Link>
          </Box>
        </div>
      </div>
    </>
  )
}