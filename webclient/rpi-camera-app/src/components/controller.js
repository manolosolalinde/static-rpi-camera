/*
var setting_key = 'iso'
var example_setting = {
    'has_auto': true,
    'range': [0,1600],
    'default_value': 0,
    'auto_value': 0
}
*/

import React, { useState, useContext, useCallback, useEffect } from 'react';
import { SocketContext } from '../context/socket';

// const base_setting = {
//     'has_auto': true,
//     'range': [0,1600],
//     'default_value': 0,
//     'auto_value': 0
// }

var myTimeout = null;


function Controller(props) {
    const { settings,device_value } = props;
    // console.log(settings)
    const { controller_key } = props;
    const socket = useContext(SocketContext);
    const [value, setValue] = useState(settings.default_value);
    const [prevValue, setPrevValue] = useState(0);

    const settingsChanged = useCallback((payload, callback) => {
        //   setSetting(true);
        console.log('payload: ', payload);
    }, []);

    const changeSettings = useCallback((data) => {
        socket.emit("CHANGE_SETTINGS", data);
    }, [socket]);

    console.log(controller_key)

    

    const changeValue = (value) => {
        const newvalue = parseInt(value)
        setValue(newvalue);
        var newdict = {};
        newdict[controller_key] = newvalue;
        const data = {
                            camera_id:'ALL',
                            settings:newdict
                        }   
        clearTimeout(myTimeout) //global variable
        myTimeout = setTimeout(() => {
            // wait 150ms, then CHANGE_SETTINGS only if there are no more changes
            // console.log('CHANGE_SETTINGS',newvalue)
            changeSettings(data);
        }, 150);


    }


    useEffect(() => {
        // as soon as the component is mounted, do the following tasks:


        // subscribe to socket events
        socket.on("READ_SETTINGS", settingsChanged);

        return () => {
            // before the component is destroyed
            // unbind all event handlers used in this component
            socket.off("READ_SETTINGS", settingsChanged);
        };
    }, [socket, settingsChanged]);


    // control auto button
    const toggleAuto = (e) => {
        if (value !== settings.auto_value) {
            setPrevValue(value);
            changeValue(settings.auto_value);
        } else {
            if (prevValue !== settings.auto_value) {
                changeValue(prevValue);
            }
        }
    }
    const auto_checked = value === settings.auto_value;

    return (
        <div className="prop-group align-items-center d-flex">
            <label htmlFor="onoff" className="form-label">{controller_key}:</label>
            { settings.has_auto && 
            <div className="auto-switch d-inline-block ml-3 align-items-center d-flex">
                <label className="sub-form-label align-middle mr-1">auto</label>
                <label className="switch">
                    <input id="onoff" type="checkbox" checked={auto_checked} onChange={(e) => toggleAuto(e)} />
                    <span className="slider round"></span>
                </label>
            </div>}
            <div className="rangeclass">
                <div className="range range-primary d-inline-flex ml-3">
                    <span className="lower-limit align-content-center text-center">0</span>
                    <input type="range" name="range" min={settings.range[0]} max={settings.range[1]} value={value} onChange={(e) => changeValue(e.currentTarget.value)} />
                    <span className="upper-limit">1600</span>
                </div>
            </div>
            <div className="output ml-3 pl-1 pr-1">
                <output id='range' className="output-value align-middle">{value}</output>
            </div>
            {device_value && 
            <div className="output ml-3 pl-1 pr-1">
                <output id='range' className="output-value align-middle">{device_value}</output>
            </div>
            }

        </div>
    )
}

export default Controller