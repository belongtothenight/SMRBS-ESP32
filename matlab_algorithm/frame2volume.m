function volume = frame2volume(frameMat, opt);
% frame2volume: Frame or frame matrix to volume conversion
%
%	Usage:
%		volume=frame2volume(frameMat, opt)
%
%	Description:
%		frame2volume(frameMat, opt) returns the volume of the given frame or frame matrix
%			frameMat: a column vector of a frame, or a matrix where each column is a frame
%			opt: options for volume computation
%				opt.method: method for volume computation
%					'absSum': absolute sum
%					'squaredSum': squared sum
%					'decibel': log of squared sum
%				opt.meanCurvePolyOrder: order for polynomial fit for approximating the mean of each frame
%
%	Example:
%		waveFile='SingaporeIsAFinePlace.wav';
%		[y, fs]=audioread(waveFile);
%		frameSize=640; overlap=480;
%		frameMat=buffer2(y, frameSize, overlap);
%		frameNum=size(frameMat, 2);
%		opt=frame2volume('defaultOpt');
%		opt1=opt; opt1.method='absSum';
%		volume1=frame2volume(frameMat, opt1);
%		opt2=opt; opt2.method='decibel';
%		volume2=frame2volume(frameMat, opt2);
%		time=(1:length(y))/fs;
%		frameTime=((0:frameNum-1)*(frameSize-overlap)+0.5*frameSize)/fs;
%		subplot(3,1,1); plot(time, y); axis tight; ylabel('Amplitude'); title(waveFile);
%		subplot(3,1,2); plot(frameTime, volume1, '.-'); axis tight; ylabel(opt1.method);
%		subplot(3,1,3); plot(frameTime, volume2, '.-'); axis tight; ylabel(opt2.method);
%		xlabel('Time (sec)');

%	Category: Audio volume computation
%	Roger Jang, 20041223, 20070417, 20110818

if nargin<1, selfdemo; return; end
% ====== Set the default options
if ischar(frameMat) & strcmp(lower(frameMat), lower('defaultOpt'))
	volume.method='absSum';
	volume.meanCurvePolyOrder=0;
	return
end
if nargin<2, opt=feval(mfilename, 'defaultOpt'); end

[frameSize, frameNum]=size(frameMat);

% ====== Use polyfit to find the mean curve
if opt.meanCurvePolyOrder==0
	for i=1:frameNum
		frameMat(:,i)=frameMat(:,i)-mean(frameMat(:,i));
	end
else
	frameMat=frameZeroMean(frameMat, opt.meanCurvePolyOrder);
end
% ====== Volume computation
volume=zeros(1, frameNum);
switch lower(opt.method)
	case lower('absSum')
		for i=1:frameNum
			frame=frameMat(:,i);
		%	frame=frame-median(frame);
			volume(i)=sum(abs(frame));
		end
	case lower({'squaredSum', 'decibel'})
		for i=1:frameNum
			frame=frameMat(:,i);
		%	frame=frame-mean(frame);
			volume(i)=sum(frame.^2);
		end
		if strcmp(opt.method, 'decibel')
			volume=10*log10(volume+realmin);	% add realmin to avoid log(0) warning
		end
	otherwise
		error('Unknown method!');
end

% ====== Self demo
function selfdemo
mObj=mFileParse(which(mfilename));
strEval(mObj.example);
