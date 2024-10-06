// Import necessary hooks and libraries
import { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { socket } from "@/socket"; // Assuming you're correctly importing the socket instance

const NotificationComponent = () => {

    useEffect(() => {
        // Listen for the 'notification' event and show a toast with the payload content
        socket.on("notifications", (payload) => {
            console.log("notif", payload); // logs the payload to console
            const notificationMessage = payload.user + " " + payload.action;

            // Display toast with the message from the server (payload)
            toast.info(notificationMessage, {
                position: "top-right",
                autoClose: 10000, // Close after 5 seconds
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
            });
        });

        // Clean up the socket listener when component unmounts
        return () => {
            socket.off("notifications");
        };
    }, []);

    return (
        <div>
            {/* Toast container where notifications will appear */}
            <ToastContainer />
        </div>
    );
};

export default NotificationComponent;
