
export const LIVE_PARAMETERS = {
    'exposure_speed':{
        'default_value':'unknown',
        'type':'display',
    },
    'analog_gain':{
        'default_value':'unknown',
        'type':'display',
    },
    'digital_gain':{
        'default_value':'unknown',
        'type':'display',
    },
    
    'awb_mode':{
        'default_value':'auto',
        'options':['auto','off','sunlight','cloudy','shade','tungsten','fluorescent','incandescent','flash','horizon'],
        'type':'option',
    },
    'exposure_mode':{
        'default_value':'auto',
        'options':['auto','off','night','nightpreview','backlight','spotlight','sports','snow','beach','verylong','fixedfps','antishake','fireworks'],
        'type':'option',
    },
    'image_effect':{
        'default_value':'none',
        'options':['none','negative','solarize','sketch','denoise','emboss','oilpaint','hatch','gpen',
                    'pastel','watercolour','film','blur','saturation','colourswap','washedout',
                    'posterise','colourpoint','colourbalance','cartoon','deinterlace1','deinterlace2'],
        'type':'option',
    },
    'meter_mode':{
        'default_value':'average',
        'options':['average','spot','backlit','matrix'],
        'type':'option',
    },
    'hflip':{
        'default_value':false,
        'type':'boolean',
    },
    'vflip':{
        'default_value':false,
        'type':'boolean',
    },
    'video_denoise':{
        'default_value':true,
        'type':'boolean',
    },
    'video_stabilization':{
        'default_value':false,
        'type':'boolean',
    },
    'image_denoise':{
        'default_value':true,
        'type':'boolean',
    },

    'iso':{
        'default_value':0,
        'range':[0,800],
        'type':'range',
    },
    'brightness':{
        'default_value':50,
        'range': [0, 100],
        'type': 'range',
    },
    'contrast':{
        'default_value':0,
        'range':[-100,100],
        'type':'range',
    },
    'saturation':{
        'default_value':0,
        'range':[-100,100],
        'type':'range',
    },
    'sharpness':{
        'default_value':0,
        'range':[-100,100],
        'type':'range',
    },
    'shutter_speed':{
        'default_value':0,
        'range':[0,60000],
        'type':'range',
    },
    'exposure_compensation':{
        'default_value':0,
        'range':[-25,25],
        'type':'range',
    },


}

