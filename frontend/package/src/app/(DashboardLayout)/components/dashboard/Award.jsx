// MUI Imports
import DashboardCard from '@/app/(DashboardLayout)/components/shared/DashboardCard'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Image from 'next/image'

const roommates = [
    {
        id: "1",
        name: "Leo Ciappi",
        logs: [
            {
                id: "event",
                image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
                time: "1:32 PM",
                event: "Cleaned"
            },
            {
                id: "event",
                image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
                time: "2:00 AM",
                event: "Contaminated"
            },
            {
                id: "event",
                image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
                time: "0:00 PM",
                event: "Contaminate"
            },
        ]
    },

    {
        id: "2",
        name: "Yeojun Han",
        logs: [
            {
                id: "event",
                image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
                time: "1:54 AM",
                event: "Contaminated"
            },
            {
                id: "event",
                image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
                time: "5:21 PM",
                event: "Contaminate"
            },
        ]
    },
];

// Function to find the best cleaner
const findBestCleaner = (roommates) => {
    return roommates.reduce((bestCleaner, roommate) => {
        // Count the number of 'Cleaned' events
        const cleanedCount = roommate.logs.filter(log => log.event === 'Cleaned').length;

        // Determine if this roommate has more cleaned events than the current best
        if (cleanedCount > (bestCleaner.cleanCount || 0)) {
            return { name: roommate.name, cleanCount: cleanedCount };
        }
        return bestCleaner;
    }, {});
};

const Award = () => {
    const bestCleaner = findBestCleaner(roommates);

    return (
        <DashboardCard>
            <Box sx={{overflow: 'auto', width: {xs: '280px', sm: 'auto'}}}>
                <center>
                    <div>
                        <Typography variant='h5'>Congratulations {bestCleaner.name || 'John'}! 🎉</Typography>
                        <Typography>Best cleaner of the month</Typography>
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
