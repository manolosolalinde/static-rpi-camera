import React, { useContext, useEffect, useState } from 'react'
import CameraSettings from './camera_settings'
import { Nav } from 'react-bootstrap'
import { SocketContext } from '../context/socket'

// var cameras = ['asdf1235', 'asdfafvs']


export default function Settings() {

    const [cameras, setCameras] = useState([]);
    const [tab, setTab] = useState(0);

    const handleSelect = (eventKey) => {
        console.log(eventKey)
        setTab(eventKey)
    }
    const socket = useContext(SocketContext);

    useEffect(() => {
        socket.on('CONNECTED_CAMERAS', (data) => {
            console.log(data.cameras);
            setCameras(data.cameras);
        });

    }, [])

    return (
        <div>
            <h2>{cameras.length === 0 ? 'No camera connected ' : 'Settings'}</h2>
            <Nav variant="tabs" onSelect={handleSelect} defaultActiveKey={0}>
                {cameras.map((camera, index) => {
                    return <Nav.Item key={index}>
                        <Nav.Link eventKey={index}>Camera{index + 1}</Nav.Link>
                    </Nav.Item>
                }
                )}

            </Nav>
            {cameras.length > 0 &&
                <CameraSettings camera={cameras[tab]} />
            }
        </div>
    )
}
