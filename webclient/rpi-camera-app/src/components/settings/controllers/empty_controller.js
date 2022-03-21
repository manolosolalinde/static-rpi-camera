
import React, { useState } from 'react';
import BaseController from './base_controller';


function EmptyController(props) {

    const { controller_key, settings, camera_readings } = props;

    const baseController = BaseController({ controller_key, settings });
    const changeValue = baseController.changeValue;
    const value = baseController.value;


    return (
        <BaseController.ControllerWrapper>
            <div className="prop-group align-items-center d-flex">
                <label className="form-label">{controller_key}:</label>
            </div>
            
        </BaseController.ControllerWrapper>
    )
}

export default EmptyController