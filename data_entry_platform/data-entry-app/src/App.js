import React, { useState, useEffect, useCallback } from 'react';
import { Button, TextField, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import './App.css';

function App() {
  const titleRef = React.useRef(null);
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [rating, setRating] = useState('');

  const handleSubmit = useCallback(() => {
    fetch('http://localhost:5000/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            body: body,
            rating: rating
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    setTitle('');
    setBody('');
    titleRef.current.focus();
  }, [title, body, rating]);


  useEffect(() => {
    const handleKeyDown = (event) => {
        if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
            handleSubmit();
        }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
        window.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleSubmit]);

  return (
    <div className="App">
      <h1>Data Entry Page</h1>
      <div>
        <TextField 
          ref={titleRef}
          label="News Title" 
          variant="outlined"
          multiline
          rows={2}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </div>
      <div>
        <TextField 
          label="News Body" 
          variant="outlined" 
          multiline 
          rows={8}
          value={body}
          onChange={(e) => setBody(e.target.value)}
        />
      </div>
      <div>
        <FormControl variant="outlined">
          <InputLabel id="rating-label">Rating</InputLabel>
          <Select
            labelId="rating-label"
            id="rating-select"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            label="Type"
          >
            <MenuItem value={"outrageous"}>Outrageous</MenuItem>
            <MenuItem value={"false"}>False</MenuItem>
            <MenuItem value={"misleading"}>Misleading</MenuItem>
            <MenuItem value={"almosttrue"}>Almost True</MenuItem>
            <MenuItem value={"true"}>True</MenuItem>
          </Select>
        </FormControl>
      </div>
      <div>
        <Button variant="contained" color="primary" onClick={handleSubmit}>
          Submit
        </Button>
      </div>
    </div>
  );
}

export default App;
