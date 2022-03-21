
import React, { useState } from 'react';
import BaseController from './base_controller';


function OptionController(props) {

    const { controller_key, settings,camera_readings, show_real_value, extra_value } = props;
    const device_value = camera_readings[controller_key];


    const {options, default_value,extra_key} = settings;

    const baseController = BaseController({ controller_key, settings });
    const changeValue = baseController.changeValue;
    const value = baseController.value;

    const changeOptionValue = (value) => {
        changeValue(value);
    }


    return (
        <BaseController.ControllerWrapper>
            <div className="prop-group align-items-center d-flex">
                <label className="form-label">{controller_key}:</label>
            </div>
            {/* select option */}
            <div className="prop-group align-items-center d-inline-flex ml-3 option">
                <select className="form-control form-select" value={device_value} onChange={(e) => changeOptionValue(e.target.value)}>
                    {options.map((option, index) => {
                        return (
                            <option key={index} value={option}>{option}</option>
                        )
                    })}
                </select>
            </div>
            {show_real_value &&
                            <div className="controller-output ml-3 pl-1 pr-1" style={{width:"110px"}}>
                            <output id='range' className="output-value align-middle">{device_value}</output>
                        </div>
            }
            {
                extra_value && 
                            <div className="controller-output ml-3 pl-1 pr-1" style={{width:"110px"}}>
                            <output id='range' className="output-value align-middle">{extra_value}</output>
                        </div>
                

            }

            
        </BaseController.ControllerWrapper>
    )
}

export default OptionController