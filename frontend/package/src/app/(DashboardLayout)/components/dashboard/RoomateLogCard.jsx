import {
    Chip, Box,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    Avatar
} from '@mui/material';
import DashboardCard from '@/app/(DashboardLayout)//components/shared/DashboardCard';
import CleanHandsOutlinedIcon from '@mui/icons-material/CleanHandsOutlined';
import SentimentVeryDissatisfiedOutlinedIcon from '@mui/icons-material/SentimentVeryDissatisfiedOutlined';

const RoommateLogCard = ({ roommate }) => {
    return (
        <DashboardCard title={`${roommate.name}'s Logs`}>
            <Box sx={{ overflow: 'auto', width: { xs: '280px', sm: 'auto' } }}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Image</TableCell>
                            <TableCell>Time</TableCell>
                            <TableCell>Event</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {roommate.logs.map((log) => (
                            <TableRow key={log.id}>
                                <TableCell>
                                    <Avatar
                                        src={log.image}
                                        alt={log.event}
                                        sx={{ width: 132, height: 132, borderRadius: '4px',}}
                                    />
                                </TableCell>
                                <TableCell>{log.time}</TableCell>
                                <TableCell>
                                    <Chip
                                        label={log.event}
                                        icon={
                                            log.event === 'Cleaned' ?
                                                <CleanHandsOutlinedIcon/> : <SentimentVeryDissatisfiedOutlinedIcon/>}
                                        sx={{
                                            backgroundColor: log.event === 'Cleaned' ? 'lightgreen' : '#FA896B',
                                            color: 'black'
                                        }}
                                    />
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Box>
        </DashboardCard>
    );
};

export default RoommateLogCard;
