
import {
    Box,
} from '@mui/material';
import DashboardCard from '@/app/(DashboardLayout)//components/shared/DashboardCard';
import RoomateLogCard from "@/app/(DashboardLayout)/components/dashboard/RoomateLogCard";

const roomates = [
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


const RoomateBlame = () => {
    return (

        <DashboardCard title="Roomate Blame Log">
            <Box sx={{ overflow: 'auto', width: { xs: '280px', sm: 'auto' } }}>
                {roomates.map((culprit) => (
                    <RoomateLogCard key={culprit.id} roommate={culprit} />
                ))}
            </Box>
        </DashboardCard>
    );
};

export default RoomateBlame;
