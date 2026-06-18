import React from 'react';
import {Composition} from 'remotion';
import {ProjectAutopilotIntro} from './ProjectAutopilotIntro';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ProjectAutopilotIntro"
      component={ProjectAutopilotIntro}
      durationInFrames={900}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
