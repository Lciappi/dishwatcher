import { useEffect, useState } from "react";
import { Grid, Typography } from "@mui/material";
import { socket } from "@/socket";

const Health = () => {
    const [status, setStatus] = useState("");

    const [socketData, setSocketData] = useState("")

    socket.on("hello", (arg) => {
        console.log(arg); // world
        setSocketData(arg)
    });



    useEffect(() => {
        const checkHealth = async () => {
            try {
                const response = await fetch("http://localhost:8080");
                if (response.ok) {
                    const data = await response.json(); // Assuming the server returns JSON
                    setStatus(data.message || "OK");
                } else {
                    setStatus("Error: " + response.statusText);
                }
            } catch (error) {
                setStatus("Error: " + error.message);
            }
        };

        checkHealth();
    }, []);

    return (
        <Grid container spacing={3}>
            <Grid item xs={12}>
                <Typography variant="h4">Health Status</Typography>
                <Typography variant="body1">{status}</Typography>
                <Typography variant="body1"> SOCKET MESSAGE: {socketData}</Typography>
            </Grid>
        </Grid>
    );
};

export default Health;
