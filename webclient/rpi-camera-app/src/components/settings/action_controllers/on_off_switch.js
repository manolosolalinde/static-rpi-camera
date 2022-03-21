import React, { useCallback, useEffect } from 'react'
import { useContext, useState } from 'react'
import { SocketContext } from '../../../context/socket';
import { ControllerWrapper } from '../controllers/base_controller';

function OnOffSwitch(props) {
    const { controller_name, controller_key, action_on, action_off, onoff_value } = props;
    var value = false;
    if (onoff_value !== undefined) {
        value = onoff_value;
    }
    const socket = useContext(SocketContext);
    const toggleSwitch = (e) => {
        e.preventDefault()
        const action = value ? action_off : action_on
        const data = {
            camera_id: 'ALL',
            settings: {
                type: 'control',
                action: action,
            }
        }
        socket.emit("CHANGE_SETTINGS", data);

    }

    return (
        <ControllerWrapper>
        <div className="prop-group align-items-center d-flex">
            <label htmlFor="onoff" className="form-label">{controller_name}:</label>
            <div className="auto-switch d-inline-block ml-3 align-items-center d-flex">
                <label className="switch">
                    <input id="onoff" type="checkbox" checked={value} onChange={(e) => toggleSwitch(e)} />
                    <span className="slider round"></span>
                </label>
            </div>
        </div>
        </ControllerWrapper>
    )
}

export default OnOffSwitch
