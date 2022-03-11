import React from "react";
// import socketio from "socket.io-client";
import { io } from "socket.io-client";
const SOCKET_URL = 'http://localhost:5000';
export const SocketContext = React.createContext();

// export const socket = socketio.connect(SOCKET_URL);
export const socket = io(SOCKET_URL);


// client-side
socket.on("connect", () => {
    console.log("connected to server");
    console.log("socket.id:",socket.id); // x8WIv7-mJelg7on_ALbx
});

socket.on("disconnect", () => {
    console.log("Disconected. socket.id:",socket.id); // undefined
});

socket.on("connect_error", (err) => {
    console.log('connect_error');
});

