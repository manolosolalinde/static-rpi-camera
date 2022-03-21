
import React, { useState } from 'react';
import BaseController from './base_controller';


function DisplayController(props) {

    const { controller_key, settings, camera_readings } = props;

    const device_value = camera_readings ? camera_readings[controller_key] : settings.default_value;


    return (
        <BaseController.ControllerWrapper>
            <div className="prop-group align-items-center d-flex">
                <label className="form-label">{controller_key}:</label>
            </div>
            <div className="controller-output ml-3 pl-1 pr-1" style={{width:"110px"}}>
                <output id='range' className="output-value align-middle" >{device_value}</output>
            </div>

        </BaseController.ControllerWrapper>
    )
}

export default DisplayController