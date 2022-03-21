/*
var setting_key = 'iso'
var example_setting = {
    'has_auto': true,
    'range': [0,1600],
    'default_value': 0,
    'auto_value': 0
}
*/

import React, { useEffect, useState } from 'react';
import BaseController, { ControllerWrapper } from './base_controller';



function RangeController(props) {
    const { controller_key, settings, camera_readings } = props;
    const device_value = camera_readings?camera_readings[controller_key]:0;
    const [prevValue, setPrevValue] = useState(0);

    const baseController = BaseController({ controller_key, settings });
    const changeValue = baseController.changeValue;
    const value = baseController.value || 0;

    const changeRangeValue = (value) => {
        if (!value) {
            value = 0
        }
        const newvalue = parseInt(value)
        changeValue(newvalue);
    }


    // control auto button
    const toggleAuto = (e) => {
        if (value !== settings.auto_value) {
            setPrevValue(value);
            changeRangeValue(settings.auto_value);
        } else {
            if (prevValue !== settings.auto_value) {
                changeRangeValue(prevValue);
            }
        }
    }
    const auto_checked = value === settings.auto_value;

    useEffect(() => {
        if (value !== device_value) {
            baseController.changeComponentValueOnly(device_value)
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [device_value])



    return (
        <ControllerWrapper>
            <div className="prop-group align-items-center d-flex">
                <label className="form-label">{controller_key}:</label>
            </div>
            <div className="prop-group align-items-center d-flex">
                {settings.has_auto &&
                    <div className="auto-switch d-inline-block ml-3 align-items-center d-flex">
                        <label className="sub-form-label align-middle mr-1">auto</label>
                        <label className="switch">
                            <input id="onoff" type="checkbox" checked={auto_checked} onChange={(e) => toggleAuto(e)} />
                            <span className="slider round"></span>
                        </label>
                    </div>}
                <div className="rangeclass">
                    <div className="range range-primary d-inline-flex ml-3">
                        <span className="lower-limit align-content-center text-center">{settings.range[0]}</span>
                        <input type="range" name="range" min={settings.range[0]} max={settings.range[1]} value={value} onChange={(e) => changeRangeValue(e.currentTarget.value)} />
                        <span className="upper-limit">{settings.range[1]}</span>
                    </div>
                </div>
                <div className="controller-input ml-3 pl-1 pr-1">
                    <input value={value} onChange={(e) => changeRangeValue(e.currentTarget.value)} className="input-value align-middle"></input>
                </div>
                {/* <div className="controller-output ml-3 pl-1 pr-1">
                <output id='range' className="output-value align-middle">{value}</output>
            </div> */}
                <div className="controller-output ml-3 pl-1 pr-1">
                    <output id='range' className="output-value align-middle">{device_value}</output>
                </div>

            </div>

        </ControllerWrapper>
    )
}

export default RangeController