// MUI Imports
import DashboardCard from '@/app/(DashboardLayout)/components/shared/DashboardCard'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Image from 'next/image'
import {useEffect, useState} from "react";
import {socket} from "@/socket";

// Function to find the best cleaner
const findBestCleaner = (roommates) => {
    return roommates?.reduce((bestCleaner, roommate) => {
        const cleanedCount = roommate.logs.filter(log => log.event === 'Cleaned').length;

        if (cleanedCount > (bestCleaner.cleanCount || 0)) {
            return { name: roommate.name, cleanCount: cleanedCount };
        }
        return bestCleaner;
    }, {});
};

const Award = ( {roommates} ) => {
    const bestCleaner = findBestCleaner(roommates);

    return (
        <DashboardCard>
            <Box sx={{overflow: 'auto', width: {xs: '280px', sm: 'auto'}}}>
                <center>
                    <div>
                        <Typography variant='h5'>Congratulations {bestCleaner?.name || 'XXX'}! 🎉</Typography>
                        <Typography>Cleaned the most this month</Typography>
                    </div>
                    <br/>
                    <Image
                        src='/images/pages/trophy.png'
                        alt='trophy image'
                        height={102}
                        width={80}
                    />
                </center>
            </Box>
        </DashboardCard>
    )
}

export default Award;
