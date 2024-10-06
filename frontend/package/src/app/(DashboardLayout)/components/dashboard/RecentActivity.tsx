import DashboardCard from '@/app/(DashboardLayout)/components/shared/DashboardCard';
import {
    Timeline,
    TimelineItem,
    TimelineOppositeContent,
    TimelineSeparator,
    TimelineDot,
    TimelineConnector,
    TimelineContent,
    timelineOppositeContentClasses,
} from '@mui/lab';
import {Box} from "@mui/material";
import {useEffect, useState} from "react";
import {socket} from "@/socket";

// Message constant to hold the activity data
const message: any[] = [
    {
        user: 'Leo Ciappi',
        action: 'cleaned',
        time: '09:30 am',
        color: 'primary',
        variant: 'outlined',
    },
    {
        user: 'Yeojun Han',
        action: 'contaminated',
        time: '09:40 am',
        color: 'warning',
        variant: 'outlined',
    },
    {
        user: 'Yeojun Han',
        action: 'cleaned',
        time: '09:43 am',
        color: 'primary',
        variant: 'outlined',
    },
    {
        user: 'Leo Ciappi',
        action: 'contaminated',
        time: '09:50 am',
        color: 'warning',
        variant: 'outlined',
    },
].map(activity => ({
    ...activity,
    content: <span>{activity.user} {activity.action}</span> // Create content for each activity
}));

interface Activity {
    user: string;
    action: string;
    time: string;
    color: 'primary' | 'warning';
    variant: 'outlined';
    content: JSX.Element;
}


function RecentActivity() {

    const [message, setMessage] = useState<any[]>([]);

    useEffect(() => {
        // @ts-ignore
        socket.on('activity', (payload: Activity[]) => {
            setMessage((prev) => payload.map(activity => ({
                ...activity,
                content: <span>{activity.user} {activity.action}</span> // Create content for each activity
            })));
        });

        return () => {
            // @ts-ignore
            socket.off('activity');
        };
    }, []);

    return (
        <DashboardCard title="Recent Activity">
            <Box sx={{overflow: 'auto', height:382}}>
                <Timeline
                    className="theme-timeline"
                    nonce={undefined}
                    onResize={undefined}
                    onResizeCapture={undefined}
                    sx={{
                        p: 0,
                        mb: '-40px',
                        '& .MuiTimelineConnector-root': {
                            width: '1px',
                            backgroundColor: '#efefef',
                        },
                        [`& .${timelineOppositeContentClasses.root}`]: {
                            flex: 0.5,
                            paddingLeft: 0,
                        },
                    }}
                >
                    {message.map((activity, index) => (
                        <TimelineItem key={index}>
                            <TimelineOppositeContent>{activity.time}</TimelineOppositeContent>
                            <TimelineSeparator>
                                <TimelineDot color={activity.color} variant={activity.variant} />
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent>{activity.content}</TimelineContent>
                        </TimelineItem>
                    ))}
                </Timeline>
            </Box>
        </DashboardCard>
    );
};

export default RecentActivity;
