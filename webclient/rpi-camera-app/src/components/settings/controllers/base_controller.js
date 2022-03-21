import { useState, useContext } from 'react';
import { SocketContext } from '../../../context/socket';
import PropTypes from 'prop-types';


// const base_setting = {
//     'has_auto': true,
//     'range': [0,1600],
//     'default_value': 0,
//     'auto_value': 0
// }

var myTimeout = null;


function BaseController(props) {
    /**
     * Send value information to server using 'CHANGE_SETTINGS' socket event
     * @param {string} controller_key
     * @param {object} settings
     * Returns:
     * @type {function} changeValue
     * @type {number} value 
     * 
     */
    const { controller_key, settings } = props;
    const socket = useContext(SocketContext);
    const [value, setValue] = useState(settings.default_value);



    // console.log(controller_key)

    const changeValue = (value,key=undefined) => {
        if (!key) {
            key = controller_key
        } 
        setValue(value);
        //change device state
        const data = {
            camera_id: 'ALL',
            settings: {
                type: 'setting',
                key: key,
                value: value
            }
        }
        clearTimeout(myTimeout) //global variable
        myTimeout = setTimeout(() => {
            // wait 150ms, then CHANGE_SETTINGS only if there are no more changes
            // console.log('CHANGE_SETTINGS',newvalue)
            socket.emit("CHANGE_SETTINGS", data);
            // changeSettings(data);
        }, 150);


    }

    const changeCameraValueOnly = (value,key=undefined) => {
        /**
         * prevents rerendering of the component
         */
        if (!key) {
            key = controller_key
        } 
        const data = {
            camera_id: 'ALL',
            settings: {
                type: 'setting',
                key: key,
                value: value
            }
        }
        socket.emit("CHANGE_SETTINGS", data);
    }

    return {
        changeValue:changeValue,
        changeCameraValueOnly:changeCameraValueOnly,
        changeComponentValueOnly:setValue,
        value:value,
    }
}

export const ControllerWrapper = (props) => {
    const { children } = props;
    return (
        <div className='controller d-flex align-items-center flex-wrap'>
            {children}
        </div>
    )
}

//static function
BaseController.ControllerWrapper = ControllerWrapper;

BaseController.propTypes = {
    controller_key: PropTypes.string.isRequired,
    settings: PropTypes.shape({
        has_auto: PropTypes.bool,
        range: PropTypes.arrayOf(PropTypes.number),
        default_value: PropTypes.number.isRequired,
        auto_value: PropTypes.number
    }).isRequired,
}

export default BaseController