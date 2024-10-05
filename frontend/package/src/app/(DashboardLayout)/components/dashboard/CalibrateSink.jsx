// MUI Imports
import DashboardCard from '@/app/(DashboardLayout)/components/shared/DashboardCard';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Image from 'next/image';
import { useState } from 'react'; // Import useState

const CalibrateSink = () => {
    const [feedback, setFeedback] = useState(''); // State for feedback message

    // Function to handle the button click
    const handleButtonClick = async () => {
        try {
            const response = await fetch('http://localhost:8080/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ roommates }), // Send roommates data if needed
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('Response from backend:', data);
            // Set success feedback
            setFeedback('Sink calibrated successfully!');

        } catch (error) {
            console.error('Error hitting the sink endpoint:', error);
            // Set error feedback
            setFeedback('Failed to calibrate sink. Please try again. ' + error.message);
        }
    };

    return (
        <DashboardCard>
            <Box sx={{ padding: 2, textAlign: 'center' }}>
                <Typography variant="h6">Calibrate Sink</Typography>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleButtonClick}
                    sx={{ marginY: 2 }}
                >
                    Hit Sink Endpoint
                </Button>
                {feedback && ( // Conditionally render feedback
                    <Typography variant="body1" sx={{ marginTop: 2, color: feedback.includes('Failed') ? 'red' : 'green' }}>
                        {feedback}
                    </Typography>
                )}
            </Box>
        </DashboardCard>
    );
};

export default CalibrateSink;
