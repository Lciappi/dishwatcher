import { io } from 'socket.io-client';

// "undefined" means the URL will be computed from the `window.location` object
const URL =  'https://yeojunh-service1--5000.prod1a.defang.dev/';

export const socket = io(URL);