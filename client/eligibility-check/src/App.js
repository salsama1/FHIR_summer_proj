import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

const App = () => {
    const [Pidvalue, setPidvalue] = useState('');
    const [Iidvalue, setIidvalue] = useState('');
    const [responseData, setResponseData] = useState(null);

    const handlePidChange = (event) => {
        if (isNumeric(event)) {
            setPidvalue(event.target.value);
        } else {
            alert("Please enter a numeric value for Pid");
        }
    };

    const handleIidChange = (event) => {
        if (isNumeric(event)) {
            setIidvalue(event.target.value);
        } else {
            alert("Please enter a numeric value for Iid");
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        console.log('Pidvalue:', Pidvalue, 'Iidvalue:', Iidvalue);
        try {
            const response = await axios.post('http://localhost:5000/eligibility', {
                patient_id: Pidvalue,
                insurer_id: Iidvalue
            });
            console.log('Response:', response.data);
            setResponseData(response.data);
            alert("Form submitted successfully");
        } catch (error) {
            console.error("There was an error!", error);
            if (error.response) {
                console.log('Error Response:', error.response.data);
                setResponseData(error.response.data);
            } else if (error.request) {
                setResponseData({ error: "No response received from the server." });
            } else {
                setResponseData({ error: `Error: ${error.message}` });
            }
        }
    };

    const isNumeric = (event) => {
        const regex = /^[0-9]*$/;
        return regex.test(event.target.value);
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Please enter the patient's Id & insurer's Id</h1>
                <form onSubmit={handleSubmit} className='form-container'>
                    <input
                        type="text"
                        value={Pidvalue}
                        onChange={handlePidChange}
                        placeholder="Type Pid..."
                        className='form-input'
                    />
                    <input
                        type="text"
                        value={Iidvalue}
                        onChange={handleIidChange}
                        placeholder="Type Iid..."
                        className='form-input'
                    />
                    <button type="submit" className='form-button'>Submit</button>
                </form>
                {responseData && (
                    <div className="response-data">
                        <h2>Response Data:</h2>
                        <pre>{JSON.stringify(responseData, null, 2)}</pre>
                    </div>
                )}
            </header>
        </div>
    );
};

export default App;
