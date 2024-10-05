'use client'
import { Grid, Box } from '@mui/material';
import PageContainer from '@/app/(DashboardLayout)/components/container/PageContainer';
// components
import RecentActivity from '@/app/(DashboardLayout)/components/dashboard/RecentActivity';
import RoomateBlame from '@/app/(DashboardLayout)/components/dashboard/RoomateBlame';
import Award from "@/app/(DashboardLayout)/components/dashboard/Award";
import NotificationComponent from "@/app/(DashboardLayout)/components/notifications/notification";
import Unaward from "@/app/(DashboardLayout)/components/dashboard/Unaward";


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
        time: "1:54 AM",
        event: "Contaminated"
      },
      {
        id: "event",
        image: "https://as2.ftcdn.net/v2/jpg/01/75/93/51/1000_F_175935137_aPD2ZOgBiey7Tlqz5PTXPqtmJnX9ZYU0.jpg",
        time: "1:54 AM",
        event: "Contaminated"
      },
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

const Dashboard = () => {
  return (
    <PageContainer title="Dashboard" description="this is Dashboard">
      <NotificationComponent />
      <Box>
        <Grid container spacing={3}>
          <Grid item xs={12} lg={8}>
            <RecentActivity />
          </Grid>
          <Grid item xs={12} lg={4}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Award roommates={roommates} />
              </Grid>
              <Grid item xs={12}>
                <Unaward roommates={roommates} />
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={12} lg={12}>
            <RoomateBlame roommates={roommates} />
          </Grid>
        </Grid>
      </Box>
    </PageContainer>
  )
}

export default Dashboard;
