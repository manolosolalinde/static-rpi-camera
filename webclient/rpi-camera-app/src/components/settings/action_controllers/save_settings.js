import React, { useContext } from 'react'
import { SocketContext } from '../../../context/socket';
import { ControllerWrapper } from '../controllers/base_controller'

function SaveSettings(props) {
    const { camera_id } = props;
    const socket = useContext(SocketContext);
    const sendAction = (action) => {
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
                <label className="form-label">Save/Load/Reset Settings:</label>
                <div className='ml-3'>
                    <button className="btn btn-primary" onClick={() => sendAction('save_settings')}>Save</button>
                    <button className="btn btn-primary ml-2" onClick={() => sendAction('load_settings')}>Load</button>
                    <button className="btn btn-primary ml-2" onClick={() => sendAction('reset_settings')}>Reset</button>
                </div>

            </div>

        </ControllerWrapper>
    )
}

export default SaveSettings