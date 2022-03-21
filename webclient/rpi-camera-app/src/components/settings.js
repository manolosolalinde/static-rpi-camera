import React, { useContext, useEffect, useState } from 'react'
import CameraSettings from './settings/camera_settings'
import { Nav } from 'react-bootstrap'
import { SocketContext } from '../context/socket'
import StreamImage from './settings/stream_image';

// var cameras = ['asdf1235', 'asdfafvs']

const initial_fake_readings = {
    resolution: '1920x1080',
    framerate: 30,
    revision: 'imx219',
    streaming_resolution: '640x480',

}


export default function Settings() {

    const [tab, setTab] = useState(0);
    const [all_camera_readings, setAllCamReadings] = useState({});
    const [image_key, setImageKey] = useState(0);

    const socket = useContext(SocketContext);
    // const handleSelect = (eventKey) => {
    //     console.log(eventKey)
    //     setTab(eventKey)
    // }




    useEffect(() => {
        const readSettings = (read_settings) => {
            const { camera_id, settings } = read_settings;
            var new_readings = {}
            new_readings[camera_id] = { ...all_camera_readings[camera_id], ...settings };
            setAllCamReadings(new_readings);
            //set random image key
            setImageKey(Math.floor(Math.random() * 100000));
        }

        // console.log('useEffect redefined')
        socket.on('CONNECTED_CAMERAS', (data) => {
            // Example of data.cameras == camera_list:
            // [
            //     {
            //         "sid": "-UpNZAF4ZIwz_J6zAAAF",
            //         "ip": "192.168.0.3"
            //     }
            // ]
            // setCameras(data.cameras);
            const camera_list = data.cameras;
            var new_all_camera_readings = {};
            // all_camera_readings = {<camera_id>: {resolution:bla,revision:bla}}
            for (const camera of camera_list) {
                const camera_reading = all_camera_readings[camera.sid] || initial_fake_readings;
                new_all_camera_readings[camera.sid] = { ...camera_reading, ip: camera.ip };
            }
            setAllCamReadings(new_all_camera_readings);
        });
        socket.on("READ_SETTINGS", readSettings);
        return () => {
            // before the component is destroyed
            // unbind all event handlers used in this component
            socket.off("READ_SETTINGS", readSettings);
            // socket.off("CONNECTED_CAMERAS",
        };

    }, [all_camera_readings, socket])

    const camera_list = Object.keys(all_camera_readings);


    const current_camera_sid = camera_list[tab];
    const current_camera_readings = all_camera_readings[current_camera_sid];


    // console.log(camera_list);
    // console.log(current_camera_readings);

    return (
        <div>
            <StreamImage key={image_key}
                camera_list={camera_list}
                camera_readings={all_camera_readings} />
            <h2>{camera_list.length === 0 ? 'No camera connected ' : 'Settings'}</h2>
            <Nav variant="tabs" onSelect={e => setTab(e)} defaultActiveKey={0}>
                {camera_list.map((camera, index) => {
                    return <Nav.Item key={index}>
                        <Nav.Link eventKey={index}>Camera{index + 1}</Nav.Link>
                    </Nav.Item>
                }
                )}

            </Nav>
            {camera_list.length > 0 &&
                <>
                    <CameraSettings camera_id={current_camera_sid}
                        camera_ip={current_camera_readings.ip}
                        camera_readings={current_camera_readings} />
                </>
            }
        </div>
    )
}
