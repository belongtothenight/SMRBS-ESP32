close all; clear all;

waveFile='test.wav';
frameSize=256;
overlap=128;
au=myAudioRead(waveFile);
y=au.signal; 
fs=au.fs;
fprintf('Length of %s is %g sec.\n', waveFile, length(y)/fs);
frameMat= enframe(y, frameSize, overlap);
frameNum=size(frameMat, 2);

% Compute volume using method 1
volume1=zeros(frameNum, 1);
for i=1:frameNum
    frame=frameMat(:,i);
    frame=frame-median(frame);		% zero-justified
    volume1(i)=sum(abs(frame));             % method 1
end
sampleTime=(1:length(y))/fs;
frameTime=((0:frameNum-1)*(frameSize-overlap)+0.5*frameSize)/fs;
subplot(2,1,1); plot(sampleTime, y); ylabel(waveFile);
subplot(2,1,2); plot(frameTime, volume1, '.-'); ylabel('Volume (Abs. sum)');
