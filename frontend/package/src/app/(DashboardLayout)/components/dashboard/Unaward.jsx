// MUI Imports
import DashboardCard from '@/app/(DashboardLayout)/components/shared/DashboardCard'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Image from 'next/image'

const findDirtiestRoomate = (roommates) => {
    return roommates.reduce((bestCleaner, roommate) => {
        const cleanedCount = roommate.logs.filter(log => log.event === 'Contaminated').length;

        if (cleanedCount > (bestCleaner.cleanCount || 0)) {
            return { name: roommate.name, cleanCount: cleanedCount };
        }
        return bestCleaner;
    }, {});
};

const Unaward = ( {roommates} ) => {
    const wrostCleaner = findDirtiestRoomate(roommates);

    return (
        <DashboardCard>
            <Box sx={{overflow: 'auto', width: {xs: '280px', sm: 'auto'}}}>
                <center>
                    <div>
                        <Typography variant='h5'>{wrostCleaner.name || 'XXX'} polluted the most ☢️</Typography>
                        <Typography>Added the most dirty dishes this month.</Typography>
                    </div>
                    <br/>
                    <Image
                        src='/images/pages/untrophy.png'
                        alt='trophy image'
                        height={102}
                        width={80}
                    />
                </center>
            </Box>
        </DashboardCard>
    )
}

export default Unaward;
