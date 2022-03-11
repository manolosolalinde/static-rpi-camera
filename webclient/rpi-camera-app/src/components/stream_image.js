import React from 'react'

export default function StreamImage() {
  return (
    <div className='stream-image'>
      <img id='video_source' alt='camera1' src="./image.jpg" onError='alert("The image could not be loaded.")' width="400" height="300" />
      <img id='video_source2' alt='camera2' src="./image.jpg" onError='alert("The image could not be loaded.")' width="400" height="300" />
    </div>
  )
}


