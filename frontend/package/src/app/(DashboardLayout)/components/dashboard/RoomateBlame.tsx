
import {
    Box,
} from '@mui/material';
import DashboardCard from '@/app/(DashboardLayout)//components/shared/DashboardCard';
import RoomateLogCard from "@/app/(DashboardLayout)/components/dashboard/RoomateLogCard";


// @ts-ignore
const RoomateBlame = ( {roommates} ) => {
    return (
        <DashboardCard title="Roomate Blame Log">
            <Box sx={{ overflow: 'auto', width: { xs: '280px', sm: 'auto' } }}>
                {roommates.map((culprit: any) => (
                    <RoomateLogCard key={culprit.id} roommate={culprit} />
                ))}
            </Box>
        </DashboardCard>
    );
};

export default RoomateBlame;
