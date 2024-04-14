"use client";
import React from "react";
import Webcam from "react-webcam";

import Image from "next/image";

const videoConstraints: any = {
  width: 1400,
  height: 720,
  facingMode: "user",
};

const WebcamCapture = (): JSX.Element => {
  const webcamRef: React.RefObject<Webcam> = React.useRef<Webcam>(null);

  const capture: () => void = React.useCallback(() => {
    const imageSrc: string | null | undefined =
      webcamRef.current?.getScreenshot();
    console.log(imageSrc);
  }, [webcamRef]);

  return (
    <>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        videoConstraints={videoConstraints}
        className="absolute z-0 h-full w-full"
      />
      <Image
        src={"/vercel.svg"}
        alt=""
        width={500}
        height={500}
        className="absolute h-full w-full"
      ></Image>
      <button
        onClick={capture}
        className="absolute w-full p-4 text-center font-mono text-3xl text-white"
      >
        Capture
      </button>
    </>
  );
};

export default function CameraPage() {
  return (
    <>
      <WebcamCapture />
    </>
  );
}
