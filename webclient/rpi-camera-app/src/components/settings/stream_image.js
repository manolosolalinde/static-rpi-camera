import React from 'react'

export default function StreamImage(props) {
  const {camera_list,camera_readings} = props;
  const setDefaultImgSrc = (event) => {
    event.target.src = './image.jpg';
  }

  const cam_list = camera_list.map((sid) => {
      return {
                  id:sid,
                  ip:camera_readings[sid].ip,
                  streaming:camera_readings[sid] ? camera_readings[sid].streaming : false,
                }
  })


  return (
    <div className='stream-image'>
      {cam_list.map((camera,index) => {
        const address = camera.streaming ? `http://${camera.ip}:${8000}/stream.mjpg` : './image.jpg';
        return(
        <img id='video_source' key={index} alt='camera1' src={address} onError={(e)=>setDefaultImgSrc(e)} width="400" height="300" />
        )

      })}
      {/* <img id='video_source2' alt='camera2' src="./image.jpg" onError='alert("The image could not be loaded.")' width="400" height="300" /> */}
    </div>
  )
}


