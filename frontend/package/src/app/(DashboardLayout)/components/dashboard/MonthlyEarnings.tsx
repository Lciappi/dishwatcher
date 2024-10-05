import dynamic from "next/dynamic";
const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });
import { useTheme } from '@mui/material/styles';
import { Stack, Typography, Fab } from '@mui/material';
import { IconTrash, IconCheck } from '@tabler/icons-react';
import { useState } from 'react';
import DashboardCard from '@/app/(DashboardLayout)/components/shared/DashboardCard';

const MonthlyEarnings = () => {
  // Chart color
  const theme = useTheme();
  const secondary = theme.palette.secondary.main;
  const secondaryLight = '#f5fcff';

  // State for dirty dishes count
  const [dirtyDishesCount, setDirtyDishesCount] = useState(0);

  // Chart configuration
  const optionsColumnChart = {
    chart: {
      type: 'area',
      fontFamily: "'Plus Jakarta Sans', sans-serif;",
      foreColor: '#adb0bb',
      toolbar: {
        show: false,
      },
      height: 60,
      sparkline: {
        enabled: true,
      },
      group: 'sparklines',
    },
    stroke: {
      curve: 'smooth',
      width: 2,
    },
    fill: {
      colors: [secondaryLight],
      type: 'solid',
      opacity: 0.05,
    },
    markers: {
      size: 0,
    },
    tooltip: {
      theme: theme.palette.mode === 'dark' ? 'dark' : 'light',
    },
  };

  const seriesColumnChart = [
    {
      name: 'Dirty Dishes',
      color: secondary,
      data: [dirtyDishesCount],
    },
  ];

  // Handlers for adding and cleaning dishes
  const handleAddDirtyDish = () => {
    setDirtyDishesCount(prevCount => prevCount + 1);
  };

  const handleCleanDishes = () => {
    setDirtyDishesCount(0);
  };

  // @ts-ignore
  // @ts-ignore
  return (
      <DashboardCard
          title="Monthly Dish Actions"
          action={
            <Stack direction="row" spacing={1}>
              <Fab color="secondary" size="medium" onClick={handleAddDirtyDish}>
                <IconTrash width={24} />
              </Fab>
              <Fab color="primary" size="medium" onClick={handleCleanDishes}>
                <IconCheck width={24} />
              </Fab>
            </Stack>
          }
          footer={
            //@ts-ignore
            <Chart options={optionsColumnChart} series={seriesColumnChart} type="area" height={60} width={"100%"} />
          }
      >
        <>
          <Typography variant="h3" fontWeight="700" mt="-20px">
            Total Dirty Dishes: {dirtyDishesCount}
          </Typography>
        </>
      </DashboardCard>
  );
};

export default MonthlyEarnings;
