
import React, { useState } from 'react';
import BooleanController from './boolean_controller';
import DisplayController from './display_only';
import OptionController from './option_controller';
import RangeController from './range_controller';

function Controller(props) {

    const {  settings } = props;

    const {type} = settings

    if (type === 'range') {
        return <RangeController {...props} />
    } else if (type === 'boolean') {
        return <BooleanController {...props} />
    } else if (type === 'option') {
        return <OptionController {...props} />
    } else if (type === 'display') {
        return <DisplayController {...props} />
    }

}

export default Controller