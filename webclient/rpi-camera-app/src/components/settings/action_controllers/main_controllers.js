import React, { useEffect } from 'react'
import BaseController, { ControllerWrapper } from '../controllers/base_controller'
import Controller from '../controllers/controller'

const modes_v1 = [
    { resolution: '1920x1080', aspect_ratio: '16:9', framerate_range: [1, 30], fov: 'partial', binning: 'none' },
    { resolution: '2592x1944', aspect_ratio: '4:3', framerate_range: [1, 15], fov: 'full', binning: 'none' },
    { resolution: '1296x972', aspect_ratio: '4:3', framerate_range: [1, 42], fov: 'full', binning: 'none' },
    { resolution: '1296x730', aspect_ratio: '16:9', framerate_range: [1, 49], fov: 'full', binning: '2x2' },
    { resolution: '640x480', aspect_ratio: '4:3', framerate_range: [42, 90], fov: 'full', binning: '4x4' },
]

const modes_v2 = [
    { resolution: '1920x1080', aspect_ratio: '16:9', framerate_range: [1, 30], fov: 'partial', binning: 'none' },
    { resolution: '3280x2464', aspect_ratio: '4:3', framerate_range: [1, 15], fov: 'full', binning: 'none' },
    { resolution: '1640x1232', aspect_ratio: '4:3', framerate_range: [1, 40], fov: 'full', binning: '2x2' },
    { resolution: '1640x922', aspect_ratio: '16:9', framerate_range: [1, 40], fov: 'full', binning: '2x2' },
    { resolution: '1280x720', aspect_ratio: '16:9', framerate_range: [40, 90], fov: 'partial', binning: '2x2' },
    { resolution: '640x480', aspect_ratio: '4:3', framerate_range: [40, 90], fov: 'partial', binning: '2x2' },
]

export const MAIN_PARAMETERS = {
    'resolution': {
        'default_value': '1280x720',
    },
    'streaming_resolution': {
        'default_value': '1280x720',
    },
    'framerate': {
        'default_value': 30,
    },
}

const streaming_resolutions_43 = [[3280, 2464], [2592, 1944], [1640, 1232], [1296, 972], [640, 480], [320, 240]]
const streaming_resolutions_169 = [[1920, 1080], [1640, 922], [1296, 730], [1280, 720], [640, 480], [320, 240]]




function MainControllers(props) {
    /**
     * 'info':'https://picamera.readthedocs.io/en/release-1.13/fov.html#camera-modes',
     */
    const { camera_readings } = props
    const { revision, resolution, framerate, streaming_resolution } = camera_readings


    const baseController_resolution = BaseController({
        controller_key: 'resolution',
        settings: MAIN_PARAMETERS['resolution']
    });
    const baseController_streaming_resolution = BaseController({
        controller_key: 'streaming_resolution',
        settings: MAIN_PARAMETERS['streaming_resolution']
    });
    const baseController_framerate = BaseController({
        controller_key: 'framerate',
        settings: MAIN_PARAMETERS['framerate']
    });
    
    const changeResolutionValue = baseController_resolution.changeValue;
    const changeStreamingResolutionValue = baseController_streaming_resolution.changeValue;
    const changeFramerateValue = baseController_framerate.changeValue;
    


    //set modes base on revision
    var modes;
    if (revision === 'ov5647') {
        modes = modes_v1;
    } else if (revision === 'imx219') {
        modes = modes_v2;
    } else {
        modes = [];
        console.log('unknown camera revision: ' + revision);
    }

    const aspect_ratio = modes.filter(mode => mode.resolution === resolution)[0].aspect_ratio;

    var streaming_resolutions = aspect_ratio === '4:3' ? streaming_resolutions_43 : streaming_resolutions_169;

    //filter only streaming_resolutions that are lower or equal than the current resolution
    streaming_resolutions = streaming_resolutions.filter(streaming_resolution => {
        const [width, height] = streaming_resolution;
        const [current_width, current_height] = resolution.split('x').map((el) => parseInt(el))
        if (width <= current_width && height <= current_height) {
            return true;
        } else {
            return false;
        }
    });

    const framerate_range = modes.filter(mode => mode.resolution === resolution)[0].framerate_range;

    const framerate_settings = {
        'default_value': 25,
        'range': framerate_range,
        'type': 'range'
    }

    const show_real_value = true;




    useEffect(() => {
        // check if values are in range
        const streaming_resolutions_str = streaming_resolutions.map(streaming_resolution => streaming_resolution.join('x'));
        if (!(streaming_resolutions_str.includes(streaming_resolution))) {
            changeStreamingResolutionValue(streaming_resolutions_str[0]);
        }
        if (!(framerate <= framerate_range[1] && framerate >= framerate_range[0])) {
            changeFramerateValue(framerate_range[1]);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [resolution])






    return (
        <>
            <ControllerWrapper>
                <div className='prop-group align-items-center d-flex'>
                    <label className='form-label'>Camera type:</label>
                </div>
                <div className="controller-output ml-3 pl-1 pr-1" style={{ width: "110px" }}>
                    <output id='range' className="output-value align-middle">{revision}</output>
                </div>
            </ControllerWrapper>
            <ControllerWrapper>
                <div className="prop-group align-items-center d-flex">
                    <label className="form-label">Resolution:</label>
                </div>
                <div className="prop-group align-items-center d-inline-flex ml-3 option">
                    <select className="form-control form-select" value={resolution} onChange={(e) => changeResolutionValue(e.target.value)}>
                        {modes.map((mode, index) => {
                            return (
                                <option key={index} value={mode.resolution}>{mode.resolution}</option>
                            )
                        })}
                    </select>
                </div>
                {show_real_value &&
                    <div className="controller-output ml-3 pl-1 pr-1" style={{ width: "110px" }}>
                        <output id='range' className="output-value align-middle">{resolution}</output>
                    </div>
                }
            </ControllerWrapper>
            <ControllerWrapper>
                <div className="prop-group align-items-center d-flex">
                    <label className="form-label">Streaming resolution:</label>
                </div>
                <div className="prop-group align-items-center d-inline-flex ml-3 option">
                    <select className="form-control form-select" value={streaming_resolution} onChange={(e) => changeStreamingResolutionValue(e.target.value)}>
                        {streaming_resolutions.map((streaming_res, index) => {
                            return (
                                <option key={index} value={streaming_res.join('x')}>{streaming_res.join('x')}</option>
                            )
                        })}
                    </select>
                </div>
                {show_real_value &&
                    <div className="controller-output ml-3 pl-1 pr-1" style={{ width: "110px" }}>
                        <output id='range' className="output-value align-middle">{streaming_resolution}</output>
                    </div>
                }
            </ControllerWrapper>
            <Controller
                controller_key={'framerate'}
                settings={framerate_settings}
                camera_readings={camera_readings}
                show_real_value={show_real_value}
            />

        </>
    )
}

export default MainControllers