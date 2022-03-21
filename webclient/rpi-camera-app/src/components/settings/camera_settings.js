import React from 'react'
import OnOffSwitch from './action_controllers/on_off_switch'
import Controller from './controllers/controller'
import { LIVE_PARAMETERS } from './parameters'
import SaveSettings from './action_controllers/save_settings'
import MainControllers from './action_controllers/main_controllers'

export default function CameraSettings(props) {

    const {camera_readings,camera_id} = props;

    const streaming = camera_readings ? camera_readings.streaming : false;
    const recording = camera_readings ? camera_readings.recording : false;

    return (
        <div>
            <div className="controller ml-2 p-3">
                Action Controllers
            </div>
            <OnOffSwitch controller_name="Start Streaming"
                        controller_key="streaming"
                        action_on='start_streaming' 
                        action_off='stop_streaming' 
                        onoff_value={streaming}
                        />
            <OnOffSwitch controller_name="Start Recording"
                        controller_key="recording"
                        action_on='start_recording' 
                        action_off='stop_recording' 
                        onoff_value={recording}
                        />
            <SaveSettings />
                        
            <div className="controller ml-2 p-3">
                Main Parameters
            </div>
                <MainControllers camera_readings={camera_readings} camera_id={camera_id} />

            <div className="controller ml-2 p-3">
                Live Parameters
            </div>
            {
                Object.keys(LIVE_PARAMETERS).map((key, index) => {
                    return (
                        <Controller
                            key={index}
                            controller_key={key}
                            settings={LIVE_PARAMETERS[key]}
                            camera_readings={camera_readings}
                            />
                    )
                })
            }
        </div>
    )
}
