function au=myAudioRead(audioFile)
% myAudioRead: Read an audio file to create an audio object
%
%	Usage:
%		au=myAudioRead(audioFile)
%
%	Example:
%		audioFile='atLeastYouAreHere.mp3';
%		au=myAudioRead(audioFile);
%		disp(au);
%
%	See also audio2file.

%	Category: Audio signal processing
%	Roger Jang, 20141214

if nargin<1, selfdemo; return; end

[parentDir, mainName, extName]=fileparts(audioFile);
% Old version of MATLAB which does not support audioread().
if verLessThan('matlab', '8.1')
	switch lower(extName)
		case '.wav'
			[au.signal, au.fs, au.nbits]=wavread(audioFile);
		case '.au'
			[au.signal, au.fs, au.nbits]=auread(audioFile);
		case '.mp3'
			if isempty(which('mp3read'))
				fprintf('Cannot find mp3read.m!\n');
				fprintf('Please download <a href="http://www.mathworks.com/matlabcentral/fileexchange/13852-mp3read-and-mp3write?s_cid=srchtitle">mp3read.m</a> from <a href="http://www.mathworks.com/matlabcentral">MATLAB Central</a>!\n');
				return
			end
			[au.signal, au.fs, au.nbits]=mp3read(audioFile);
		case '.aif'
			if isempty(which('aiffread'))
				fprintf('Cannot find aiffread.m!\n');
				fprintf('Please download <a href="http://www.mathworks.com/matlabcentral/fileexchange/23328-aiffread?s_cid=srchtitle">aiffread.m</a> from <a href="http://www.mathworks.com/matlabcentral">MATLAB Central</a>!\n');
				return
			end
			[au.signal, au.fs]=aiffread(audioFile);
			au.fs=16;		% Sure?
	end
	au.file=audioFile;
	au.amplitudeNormalized=1;		% The amplitude is normalized to [-1, 1] already
	return
end

% New version of MATLAB supports audioread().
[au.signal, au.fs]=audioread(audioFile);
info=audioinfo(audioFile);
if isfield(info, 'BitsPerSample')
	au.nbits=info.BitsPerSample;
else
%	fprintf('Cannot identify BitsPerSample of %s, assuming it is 16 bits\n', audioFile)
	au.nbits=16;
end

au.file=audioFile;
au.amplitudeNormalized=1;		% The amplitude is normalized to [-1, 1] already

% ====== Self demo
function selfdemo
mObj=mFileParse(which(mfilename));
strEval(mObj.example);
