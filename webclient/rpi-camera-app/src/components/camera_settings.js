import React from 'react'
import Controller from './controller'

var settings = {
    'iso': {
        'has_auto': true,
        'range': [0, 1600],
        'default_value': 0,
        'auto_value': 0
    }
}

var device_data = {
    'iso': 200,
    'exposure': 30,
}

export default function CameraSettings() {
    return (
        <div>
            <Controller controller_key='iso' 
                        settings={settings['iso']}
                        device_value={device_data['iso']} />
            <Controller controller_key='iso' settings={settings['iso']} />
        </div>
    )
}
