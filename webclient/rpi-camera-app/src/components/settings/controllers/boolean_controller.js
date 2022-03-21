
import React, { useState } from 'react';
import BaseController from './base_controller';


function BooleanController(props) {

    const { controller_key, settings, camera_readings } = props;
    const device_value = camera_readings[controller_key];

    var value = false;
    if (device_value !== undefined) {
        value = device_value;
    }

    const baseController = BaseController({ controller_key, settings });
    const changeValue = baseController.changeValue;
    // const value = baseController.value;

    const toggleSwitch = (e) => {
        e.preventDefault();
        const newvalue = value? 0: 1;
        changeValue(newvalue);
    }

    // console.log(value)


    return (
        <BaseController.ControllerWrapper>
            <div className="prop-group align-items-center d-flex">
                <label className="form-label">{controller_key}:</label>
            </div>
            <div className="prop-group align-items-center d-inline-flex ml-3 boolean">
                <div className="auto-switch d-inline-block ml-3 align-items-center d-flex">
                    <label className="switch">
                        <input id="onoff" type="checkbox" checked={value} onChange={(e) => toggleSwitch(e)} />
                        <span className="slider round"></span>
                    </label>
                </div>
            </div>


        </BaseController.ControllerWrapper>
    )
}

export default BooleanController